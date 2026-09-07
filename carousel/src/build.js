// build.js — split one GK article into a SERIES of Instagram carousels ("小出し連載")
// using Claude structured output. Language follows the article. No fact invention.
import Anthropic from "@anthropic-ai/sdk";

const MODEL = process.env.CLAUDE_MODEL || "claude-opus-4-8";
const HANDLE = "@KEEPIX.GK_OFFICIAL";

const SYSTEM = `You design Instagram swipe carousels for ${HANDLE}, a goalkeeping (GK) coaching brand.
You turn ONE long GK coaching article into a SERIES of carousels ("小出し連載") — one carousel per part.

HARD RULES:
- OUTPUT LANGUAGE = the article's language. Japanese article -> every slide field AND the caption in Japanese. English article -> English. Do not translate.
- NEVER invent facts, numbers, prices, product names, specs, or claims that are not in the article. If the article does not say it, do not write it.
- Split the article into 2-4 PARTS along natural topic boundaries. Each part is ONE carousel of 4-6 slides total.
- Slide order per carousel: exactly one "cover" first, then 2-4 "content" slides, then exactly one "cta" last.
- content.body: short and punchy. English <= ~280 chars; Japanese <= ~140 chars. Separate short paragraphs with "\\n\\n". Bullet lines start with "- ". No markdown headings, no emoji.
- content.heading: one short line (JP <= ~24 chars, EN <= ~40 chars).
- content.badge: the content slide's index within its carousel as a string: "1", "2", ... starting at 1.
- cover.kicker: a short uppercase label, e.g. "GK COACHING" (an English label is OK even on Japanese posts). cover.title: the hook. cover.subtitle: one supporting line.
- cta.kicker: "KEEPIX". cta.title: a short call to action. cta.body: one supporting line.
- caption: a natural Instagram caption for THAT part, in the post language, ending with a few relevant hashtags. State it is Part n of N. <= 2200 characters.

Return ONLY valid minified JSON (no code fences, no prose) matching exactly:
{"articleTitle":string,"totalParts":number,"parts":[{"part":number,"caption":string,"slides":[{"type":"cover","kicker":string,"title":string,"subtitle":string},{"type":"content","badge":string,"heading":string,"body":string},{"type":"cta","kicker":string,"title":string,"body":string}]}]}`;

function stripToJson(text) {
  let t = (text || "").trim();
  if (t.startsWith("```")) t = t.replace(/^```[a-z]*\n?/i, "").replace(/```\s*$/, "").trim();
  const s = t.indexOf("{");
  const e = t.lastIndexOf("}");
  if (s === -1 || e === -1) throw new Error("Claude did not return JSON");
  return t.slice(s, e + 1);
}

function validate(data) {
  if (!data || !Array.isArray(data.parts) || data.parts.length === 0) {
    throw new Error("compiled plan has no parts");
  }
  data.parts.forEach((p, i) => {
    p.part = i + 1;
    if (!Array.isArray(p.slides) || p.slides.length < 2 || p.slides.length > 10) {
      throw new Error(`part ${i + 1} must have 2-10 slides, got ${p.slides?.length}`);
    }
  });
  data.totalParts = data.parts.length;
  return data;
}

export async function compileArticle(articleText, { title } = {}) {
  if (!process.env.ANTHROPIC_API_KEY) throw new Error("ANTHROPIC_API_KEY is not set");
  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  const msg = await client.messages.create({
    model: MODEL,
    max_tokens: 8000,
    system: SYSTEM,
    messages: [{
      role: "user",
      content: `Article title: ${title || "(none)"}\n\nArticle:\n${articleText}\n\nSplit into parts now. Return ONLY the JSON.`,
    }],
  });
  const text = msg.content.filter((b) => b.type === "text").map((b) => b.text).join("");
  return validate(JSON.parse(stripToJson(text)));
}
