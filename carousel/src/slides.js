import { createCanvas, GlobalFonts, loadImage } from "@napi-rs/canvas";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { existsSync } from "node:fs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ASSETS = path.join(HERE, "..", "assets");
const FONTS = path.join(ASSETS, "fonts");

function firstExisting(paths) {
  return paths.find((p) => existsSync(p));
}

// Latin: prefer bundled, else system Liberation Sans (present on the CI runner).
const LIB = "/usr/share/fonts/truetype/liberation";
GlobalFonts.registerFromPath(
  firstExisting([path.join(FONTS, "Head.ttf"), `${LIB}/LiberationSans-Bold.ttf`]),
  "J4KHead",
);
GlobalFonts.registerFromPath(
  firstExisting([path.join(FONTS, "Body.ttf"), `${LIB}/LiberationSans-Regular.ttf`]),
  "J4KBody",
);
// Japanese: bundled JP font, else system Noto CJK (workflow installs fonts-noto-cjk).
const jp = firstExisting([
  path.join(FONTS, "JP.ttf"),
  path.join(FONTS, "JP.otf"),
  "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
  "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
  "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
]);
if (jp) GlobalFonts.registerFromPath(jp, "J4KJP");

// --- KEEPIX brand tokens (dark + mint green, matching the logo) ---
const W = 1080;
const H = 1350;
const M = 96;
const BG = "#0B1512"; // near-black green
const ACCENT = "#5FE3A1"; // KEEPIX mint green
const WHITE = "#FFFFFF";
const GRAY = "#93A29B";
const BODYCOL = "#D7DEDA";
const INK = "#08110D"; // dark text on green
const INK_MUTED = "#123227"; // muted dark text on green
const HEAD = jp ? "J4KHead, J4KJP" : "J4KHead";
const BODY = jp ? "J4KBody, J4KJP" : "J4KBody";
const HANDLE = "@KEEPIX.GK_OFFICIAL";

const LOGO_PATH = firstExisting([
  path.join(ASSETS, "keepix-logo.png"),
  path.join(ASSETS, "logo.png"),
]);

function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}

function wrapLines(ctx, text, maxWidth) {
  // Word-based for Latin; falls back to char-based when a token is too wide (CJK).
  const out = [];
  for (const rawWord of text.split(/\s+/).filter(Boolean)) {
    let word = rawWord;
    while (ctx.measureText(word).width > maxWidth) {
      let i = 1;
      while (i < word.length && ctx.measureText(word.slice(0, i + 1)).width <= maxWidth) i++;
      out.push({ w: word.slice(0, i), space: false });
      word = word.slice(i);
    }
    out.push({ w: word, space: true });
  }
  const lines = [];
  let line = "";
  for (const tok of out) {
    const test = line ? `${line}${tok.space ? " " : ""}${tok.w}` : tok.w;
    if (ctx.measureText(test).width > maxWidth && line) {
      lines.push(line);
      line = tok.w;
    } else {
      line = test;
    }
  }
  if (line) lines.push(line);
  return lines;
}

function drawBody(ctx, text, x, y, maxWidth, { size = 40, lineHeight = 1.45, color = BODYCOL } = {}) {
  ctx.font = `${size}px ${BODY}`;
  ctx.fillStyle = color;
  ctx.textBaseline = "alphabetic";
  const lh = size * lineHeight;
  let cursor = y;
  const paragraphs = text.split(/\n+/).map((p) => p.trim()).filter(Boolean);
  paragraphs.forEach((para, pi) => {
    const bullet = /^[-*]\s+/.test(para);
    const content = bullet ? para.replace(/^[-*]\s+/, "") : para;
    const indent = bullet ? 44 : 0;
    const lines = wrapLines(ctx, content, maxWidth - indent);
    lines.forEach((ln, li) => {
      cursor += lh;
      if (bullet && li === 0) {
        ctx.fillStyle = ACCENT;
        ctx.fillText("•", x, cursor);
        ctx.fillStyle = color;
      }
      ctx.fillText(ln, x + indent, cursor);
    });
    if (pi < paragraphs.length - 1) cursor += lh * 0.45;
  });
  return cursor;
}

function measureBodyHeight(ctx, text, maxWidth, size, lineHeight = 1.45) {
  ctx.font = `${size}px ${BODY}`;
  const lh = size * lineHeight;
  let h = 0;
  const paragraphs = text.split(/\n+/).map((p) => p.trim()).filter(Boolean);
  paragraphs.forEach((para, pi) => {
    const bullet = /^[-*]\s+/.test(para);
    const content = bullet ? para.replace(/^[-*]\s+/, "") : para;
    const indent = bullet ? 44 : 0;
    h += wrapLines(ctx, content, maxWidth - indent).length * lh;
    if (pi < paragraphs.length - 1) h += lh * 0.45;
  });
  return h;
}

function drawLogo(ctx, logo, x, y, size, onAccent) {
  if (logo) {
    ctx.drawImage(logo, x, y, size, size);
    return size;
  }
  // Fallback wordmark
  ctx.font = `bold ${Math.round(size * 0.5)}px ${HEAD}`;
  ctx.fillStyle = onAccent ? INK : ACCENT;
  ctx.textBaseline = "alphabetic";
  ctx.fillText("KEEPIX", x, y + size * 0.62);
  return size;
}

function footer(ctx, rightText, { onAccent = false } = {}) {
  const y = H - M;
  ctx.strokeStyle = onAccent ? "rgba(8,17,13,0.25)" : "rgba(255,255,255,0.14)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(M, y - 46);
  ctx.lineTo(W - M, y - 46);
  ctx.stroke();
  ctx.font = `24px ${BODY}`;
  ctx.textBaseline = "alphabetic";
  ctx.fillStyle = onAccent ? "rgba(8,17,13,0.75)" : GRAY;
  ctx.textAlign = "left";
  ctx.fillText(HANDLE, M, y);
  if (rightText) {
    ctx.textAlign = "right";
    ctx.fillStyle = onAccent ? INK : ACCENT;
    ctx.font = `bold 24px ${HEAD}`;
    ctx.fillText(rightText, W - M, y);
  }
  ctx.textAlign = "left";
}

function spaced(str) {
  return str.split("").join(" ");
}

// --- Bilingual slides (Japanese primary + English secondary) ---

function drawCover(ctx, s, logo) {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);

  if (logo) drawLogo(ctx, logo, M, 150, 132, false);

  const kicker = (s.kicker || "GK COACHING").toUpperCase();
  ctx.fillStyle = ACCENT;
  ctx.fillRect(M, 372, 64, 8);
  ctx.font = `bold 30px ${HEAD}`;
  ctx.fillStyle = ACCENT;
  ctx.textBaseline = "alphabetic";
  ctx.fillText(spaced(kicker), M, 354);

  // Japanese title (primary)
  ctx.font = `82px ${HEAD}`;
  ctx.fillStyle = WHITE;
  let y = 470;
  for (const ln of wrapLines(ctx, s.title || "", W - M * 2)) {
    y += 90;
    ctx.fillText(ln, M, y);
  }

  // English title (secondary, mint)
  if (s.titleEn) {
    ctx.font = `44px ${HEAD}`;
    ctx.fillStyle = ACCENT;
    y += 24;
    for (const ln of wrapLines(ctx, s.titleEn, W - M * 2)) {
      y += 54;
      ctx.fillText(ln, M, y);
    }
  }

  // Subtitles (JP then EN, both muted)
  if (s.subtitle) {
    ctx.font = `38px ${BODY}`;
    ctx.fillStyle = GRAY;
    y += 34;
    for (const ln of wrapLines(ctx, s.subtitle, W - M * 2)) {
      y += 50;
      ctx.fillText(ln, M, y);
    }
  }
  if (s.subtitleEn) {
    ctx.font = `30px ${BODY}`;
    ctx.fillStyle = GRAY;
    y += 14;
    for (const ln of wrapLines(ctx, s.subtitleEn, W - M * 2)) {
      y += 42;
      ctx.fillText(ln, M, y);
    }
  }

  footer(ctx, "SWIPE →");
}

function drawContent(ctx, s, index, total) {
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);

  let y = 200;
  if (s.badge) {
    ctx.fillStyle = ACCENT;
    roundRect(ctx, M, y, 88, 88, 22);
    ctx.fill();
    ctx.fillStyle = INK;
    ctx.font = `52px ${HEAD}`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(String(s.badge), M + 44, y + 48);
    ctx.textAlign = "left";
    ctx.textBaseline = "alphabetic";
    y += 132;
  } else {
    ctx.fillStyle = ACCENT;
    ctx.fillRect(M, y, 64, 8);
    y += 36;
  }

  // Japanese heading (primary)
  ctx.font = `54px ${HEAD}`;
  ctx.fillStyle = WHITE;
  for (const ln of wrapLines(ctx, s.heading || "", W - M * 2)) {
    y += 62;
    ctx.fillText(ln, M, y);
  }
  // English heading (secondary, mint)
  if (s.headingEn) {
    ctx.font = `30px ${HEAD}`;
    ctx.fillStyle = ACCENT;
    y += 12;
    for (const ln of wrapLines(ctx, s.headingEn, W - M * 2)) {
      y += 38;
      ctx.fillText(ln, M, y);
    }
  }

  y += 20;
  const maxWidth = W - M * 2;
  const available = H - M - 70 - y;
  const jp = s.body || "";
  const en = s.bodyEn || "";

  // Pick one size so JP body + divider + EN body all fit.
  let size = 36;
  for (const t of [36, 33, 30, 28, 26, 24, 22]) {
    size = t;
    const hJp = measureBodyHeight(ctx, jp, maxWidth, t);
    const hEn = en ? measureBodyHeight(ctx, en, maxWidth, Math.max(t - 3, 20)) : 0;
    const gap = en ? 44 : 0;
    if (hJp + gap + hEn <= available) break;
  }

  let cy = drawBody(ctx, jp, M, y, maxWidth, { size, color: BODYCOL });
  if (en) {
    cy += 22;
    ctx.strokeStyle = "rgba(95,227,161,0.35)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(M, cy);
    ctx.lineTo(M + 120, cy);
    ctx.stroke();
    cy += 6;
    drawBody(ctx, en, M, cy, maxWidth, { size: Math.max(size - 3, 20), color: GRAY });
  }

  footer(ctx, `${index} / ${total}`);
}

function drawCta(ctx, s, logo) {
  ctx.fillStyle = ACCENT;
  ctx.fillRect(0, 0, W, H);

  if (logo) drawLogo(ctx, logo, M, 150, 132, true);

  ctx.fillStyle = INK;
  ctx.font = `bold 30px ${HEAD}`;
  ctx.fillText(spaced((s.kicker || "KEEPIX").toUpperCase()), M, 360);

  // Japanese title (primary)
  ctx.font = `74px ${HEAD}`;
  ctx.fillStyle = INK;
  let y = 420;
  for (const ln of wrapLines(ctx, s.title || "", W - M * 2)) {
    y += 82;
    ctx.fillText(ln, M, y);
  }
  // English title (secondary)
  if (s.titleEn) {
    ctx.font = `40px ${HEAD}`;
    ctx.fillStyle = INK_MUTED;
    y += 16;
    for (const ln of wrapLines(ctx, s.titleEn, W - M * 2)) {
      y += 48;
      ctx.fillText(ln, M, y);
    }
  }

  // Body JP then EN
  if (s.body) {
    y += 28;
    ctx.font = `38px ${BODY}`;
    ctx.fillStyle = INK_MUTED;
    for (const ln of wrapLines(ctx, s.body, W - M * 2)) {
      y += 52;
      ctx.fillText(ln, M, y);
    }
  }
  if (s.bodyEn) {
    y += 12;
    ctx.font = `32px ${BODY}`;
    ctx.fillStyle = "rgba(8,17,13,0.62)";
    for (const ln of wrapLines(ctx, s.bodyEn, W - M * 2)) {
      y += 44;
      ctx.fillText(ln, M, y);
    }
  }

  ctx.font = `44px ${HEAD}`;
  ctx.fillStyle = INK;
  ctx.fillText(HANDLE, M, H - M - 90);

  footer(ctx, "FOLLOW", { onAccent: true });
}

function renderSlide(slide, index, total, logo) {
  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext("2d");
  if (slide.type === "cover") drawCover(ctx, slide, logo);
  else if (slide.type === "cta") drawCta(ctx, slide, logo);
  else drawContent(ctx, slide, index, total);
  return canvas.toBuffer("image/png");
}

/**
 * Render a slide plan to an array of { name, buffer } PNG slides.
 */
export async function renderSlides(plan) {
  const logo = LOGO_PATH ? await loadImage(LOGO_PATH) : null;
  const slides = plan.slides || [];
  return slides.map((slide, i) => ({
    name: `${String(i + 1).padStart(2, "0")}.png`,
    buffer: renderSlide(slide, i + 1, slides.length, logo),
  }));
}
