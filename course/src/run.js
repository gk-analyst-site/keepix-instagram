// run.js — 100-day GK course orchestrator. Picks the next unposted day,
// renders its lesson card, commits it for a permanent SHA-pinned raw URL,
// posts the single image, and records progress. Runs once per daily tick.
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
import { renderCard } from "./card.js";
import { postSingle } from "./post.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const COURSE = path.join(HERE, "..");           // course/
const REPO_ROOT = path.join(COURSE, "..");      // repo root
const CONTENT = path.join(COURSE, "content");
const OUT = path.join(COURSE, "out");
const PROGRESS = path.join(CONTENT, "posted-days.json");

const REPO = process.env.GITHUB_REPOSITORY || "gk-analyst-site/keepix-instagram";
const DRY = /^(1|true|yes)$/i.test(process.env.DRY_RUN || "");

function git(args) {
  return execFileSync("git", args, { cwd: REPO_ROOT, stdio: ["ignore", "pipe", "inherit"], encoding: "utf8" }).trim();
}
const rel = (abs) => path.relative(REPO_ROOT, abs).split(path.sep).join("/");

function loadLessons() {
  const files = readdirSync(CONTENT).filter((f) => /^module-\d+\.json$/.test(f)).sort();
  const lessons = [];
  for (const f of files) {
    const m = JSON.parse(readFileSync(path.join(CONTENT, f), "utf8"));
    for (const l of m.lessons) {
      lessons.push({ ...l, module: m.module, moduleTitle: m.moduleTitle, moduleTitleEn: m.moduleTitleEn });
    }
  }
  lessons.sort((a, b) => a.day - b.day);
  return lessons;
}
function loadProgress() {
  if (!existsSync(PROGRESS)) return { postedDays: [], lastPostedAt: null };
  return JSON.parse(readFileSync(PROGRESS, "utf8"));
}
function saveProgress(p) {
  writeFileSync(PROGRESS, JSON.stringify(p, null, 2) + "\n");
}

function buildCaption(L) {
  return [
    `【100日GK講座 Day ${L.day}/100】${L.title}`,
    "",
    `今日のポイント：${L.point}`,
    "",
    `Day ${L.day}/100 — ${L.titleEn}`,
    `Key: ${L.pointEn}`,
    "",
    "毎日1レッスンでGKを体系的に。保存して続けよう。",
    "One GK lesson a day. Save it and keep going.",
    "",
    "#ゴールキーパー #GK #キーパー #goalkeeper #goalkeepertraining #goalkeeping #100日GK講座 #keepix",
  ].join("\n");
}

async function main() {
  mkdirSync(OUT, { recursive: true });
  const lessons = loadLessons();
  const progress = loadProgress();
  const posted = new Set(progress.postedDays || []);
  const next = lessons.find((l) => !posted.has(l.day));
  if (!next) {
    console.log("100日講座は全日投稿済み（完結）。本日はスキップします。");
    return;
  }

  console.log(`Rendering Day ${next.day}/100 — ${next.title} (Module ${next.module})…`);
  const buf = renderCard(next);
  const abs = path.join(OUT, `day-${String(next.day).padStart(3, "0")}.png`);
  writeFileSync(abs, buf);
  console.log(`  wrote ${rel(abs)}`);

  if (DRY) {
    console.log("[dry-run] レンダリングのみ。コミット・投稿はしません。");
    console.log("--- caption ---\n" + buildCaption(next));
    return;
  }

  // Commit the card so it has a permanent, public, SHA-pinned raw URL.
  git(["add", "-f", rel(abs)]);
  git(["commit", "-m", `course: day ${next.day} card [skip ci]`]);
  git(["push", "origin", "HEAD:main"]);
  const sha = git(["rev-parse", "HEAD"]);
  const imageUrl = `https://raw.githubusercontent.com/${REPO}/${sha}/${rel(abs)}`;
  console.log(`  raw URL: ${imageUrl}`);

  console.log("Posting to Instagram…");
  const mediaId = await postSingle({ imageUrl, caption: buildCaption(next) });
  console.log(`✅ Published Day ${next.day}/100 — media id ${mediaId}`);

  progress.postedDays = [...posted, next.day].sort((a, b) => a - b);
  progress.lastPostedAt = new Date().toISOString();
  progress.lastDay = next.day;
  if (progress.postedDays.length >= 100) progress.done = true;
  saveProgress(progress);
  git(["add", rel(PROGRESS)]);
  git(["commit", "-m", `course: day ${next.day} posted [skip ci]`]);
  git(["push", "origin", "HEAD:main"]);
  console.log("進捗を記録しました。");
}

main().catch((e) => {
  console.error("ERROR:", e.stack || e.message);
  process.exit(1);
});
