// run.js — orchestrator. Picks the next unposted article/part, compiles it (once)
// with Claude, renders the slides, commits them for a permanent SHA-pinned raw URL,
// posts the carousel, and records progress. Designed to run once per schedule tick.
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
import { renderSlides } from "./slides.js";
import { compileArticle } from "./build.js";
import { postCarousel } from "./post.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const CAR = path.join(HERE, "..");             // carousel/
const REPO_ROOT = path.join(CAR, "..");        // repo root
const ARTICLES = path.join(CAR, "content", "articles");
const COMPILED = path.join(CAR, "content", "compiled");
const OUT = path.join(CAR, "out");
const PROGRESS = path.join(CAR, "content", "posted-articles.json");

const REPO = process.env.GITHUB_REPOSITORY || "gk-analyst-site/keepix-instagram";
const DRY = /^(1|true|yes)$/i.test(process.env.DRY_RUN || "");

function git(args) {
  return execFileSync("git", args, { cwd: REPO_ROOT, stdio: ["ignore", "pipe", "inherit"], encoding: "utf8" }).trim();
}
function rel(abs) {
  return path.relative(REPO_ROOT, abs).split(path.sep).join("/");
}
function loadProgress() {
  if (!existsSync(PROGRESS)) return { articles: {} };
  return JSON.parse(readFileSync(PROGRESS, "utf8"));
}
function saveProgress(p) {
  writeFileSync(PROGRESS, JSON.stringify(p, null, 2) + "\n");
}
function parseFrontmatter(md) {
  const m = md.match(/^---\n([\s\S]*?)\n---\n?/);
  if (!m) return { meta: {}, body: md.trim() };
  const meta = {};
  for (const line of m[1].split("\n")) {
    const mm = line.match(/^(\w+):\s*(.*)$/);
    if (mm) meta[mm[1]] = mm[2].trim();
  }
  return { meta, body: md.slice(m[0].length).trim() };
}
function articleSlugs() {
  if (!existsSync(ARTICLES)) return [];
  return readdirSync(ARTICLES).filter((f) => f.endsWith(".md")).sort().map((f) => f.replace(/\.md$/, ""));
}
async function getCompiled(slug) {
  mkdirSync(COMPILED, { recursive: true });
  const cp = path.join(COMPILED, `${slug}.json`);
  if (existsSync(cp)) return JSON.parse(readFileSync(cp, "utf8"));
  const { meta, body } = parseFrontmatter(readFileSync(path.join(ARTICLES, `${slug}.md`), "utf8"));
  console.log(`Compiling "${slug}" into parts with Claude…`);
  const data = await compileArticle(body, { title: meta.title });
  writeFileSync(cp, JSON.stringify(data, null, 2) + "\n");
  return data;
}
function pickNext(progress) {
  for (const slug of articleSlugs()) {
    const st = progress.articles[slug];
    if (!st || !st.done) return slug;
  }
  return null;
}

async function main() {
  mkdirSync(OUT, { recursive: true });
  const progress = loadProgress();
  const slug = pickNext(progress);
  if (!slug) {
    console.log("未投稿の記事がありません（すべて連載完了）。本日はスキップします。");
    return;
  }

  const compiled = await getCompiled(slug);
  const st = progress.articles[slug] || { totalParts: compiled.totalParts, postedParts: [], done: false };
  st.totalParts = compiled.totalParts;
  const nextPart = st.postedParts.length + 1;
  if (nextPart > compiled.totalParts) {
    st.done = true;
    progress.articles[slug] = st;
    saveProgress(progress);
    console.log(`"${slug}" は全 ${compiled.totalParts} パート投稿済み。`);
    return;
  }

  const partPlan = compiled.parts.find((p) => p.part === nextPart);
  console.log(`Rendering "${slug}" Part ${nextPart}/${compiled.totalParts} (${partPlan.slides.length} slides)…`);
  const slides = await renderSlides(partPlan);
  const outDir = path.join(OUT, slug, `part-${String(nextPart).padStart(2, "0")}`);
  mkdirSync(outDir, { recursive: true });
  const absPaths = [];
  for (const s of slides) {
    const abs = path.join(outDir, s.name);
    writeFileSync(abs, s.buffer);
    absPaths.push(abs);
  }
  console.log(`  wrote ${slides.length} slides -> ${rel(outDir)}`);

  if (DRY) {
    console.log("[dry-run] レンダリングのみ。コミット・投稿はしません。");
    return;
  }

  // Commit the slides + compiled plan so they have a permanent, public, SHA-pinned raw URL.
  git(["add", "-f", ...absPaths.map(rel), rel(path.join(COMPILED, `${slug}.json`))]);
  git(["commit", "-m", `carousel: ${slug} part ${nextPart} slides [skip ci]`]);
  git(["push", "origin", "HEAD:main"]);
  const sha = git(["rev-parse", "HEAD"]);
  const imageUrls = absPaths.map((abs) => `https://raw.githubusercontent.com/${REPO}/${sha}/${rel(abs)}`);
  console.log("  raw URLs:\n" + imageUrls.map((u) => "   " + u).join("\n"));

  console.log("Posting carousel to Instagram…");
  const mediaId = await postCarousel({ imageUrls, caption: partPlan.caption });
  console.log(`✅ Published Part ${nextPart}/${compiled.totalParts} — media id ${mediaId}`);

  st.postedParts.push(nextPart);
  st.lastPostedAt = new Date().toISOString();
  if (st.postedParts.length >= compiled.totalParts) st.done = true;
  progress.articles[slug] = st;
  saveProgress(progress);
  git(["add", rel(PROGRESS)]);
  git(["commit", "-m", `carousel: ${slug} part ${nextPart} posted [skip ci]`]);
  git(["push", "origin", "HEAD:main"]);
  console.log("進捗を記録しました。");
}

main().catch((e) => {
  console.error("ERROR:", e.stack || e.message);
  process.exit(1);
});
