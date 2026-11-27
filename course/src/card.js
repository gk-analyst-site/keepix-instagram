// 100-day GK course — single "lesson card" renderer (1080x1350, KEEPIX brand).
// Each day = one card: module label + Day X/100 + JP/EN lesson + key point.
import { createCanvas, GlobalFonts } from "@napi-rs/canvas";
import { existsSync } from "node:fs";

const LIB = "/usr/share/fonts/truetype/liberation";
if (existsSync(`${LIB}/LiberationSans-Bold.ttf`)) {
  GlobalFonts.registerFromPath(`${LIB}/LiberationSans-Bold.ttf`, "KXHead");
  GlobalFonts.registerFromPath(`${LIB}/LiberationSans-Regular.ttf`, "KXBody");
}
const JP = [
  "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
  "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
  "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
].find((p) => existsSync(p));
if (JP) GlobalFonts.registerFromPath(JP, "KXJP");
const HEAD = JP ? "KXHead, KXJP" : "KXHead";
const BODY = JP ? "KXBody, KXJP" : "KXBody";

const W = 1080, H = 1350, M = 96;
const BG = "#0B1512", ACCENT = "#5FE3A1", WHITE = "#FFFFFF",
  GRAY = "#93A29B", BODYCOL = "#D7DEDA", INK = "#08110D";

function rr(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}
function spaced(s) { return s.split("").join(" "); }
function wrap(ctx, text, maxW) {
  const out = [];
  for (const para of String(text).split("\n")) {
    if (para === "") { out.push(""); continue; }
    let line = "";
    // char-based wrap works for JP (no spaces) and EN alike
    for (const ch of para) {
      const t = line + ch;
      if (ctx.measureText(t).width > maxW && line) { out.push(line); line = ch; }
      else line = t;
    }
    if (line) out.push(line);
  }
  return out;
}
function drawPara(ctx, text, x, y, maxW, size, lh, color, font) {
  ctx.font = `${size}px ${font}`;
  ctx.fillStyle = color;
  const lines = wrap(ctx, text, maxW);
  let yy = y;
  for (const ln of lines) { ctx.fillText(ln, x, yy); yy += lh; }
  return yy;
}
function measurePara(ctx, text, maxW, size, lh, font) {
  ctx.font = `${size}px ${font}`;
  return wrap(ctx, text, maxW).length * lh;
}

export function renderCard(L) {
  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = BG; ctx.fillRect(0, 0, W, H);
  const colW = W - 2 * M;
  const dd = String(L.day).padStart(2, "0");

  // top: module kicker + accent bar + Day badge
  ctx.font = `bold 26px ${HEAD}`; ctx.fillStyle = ACCENT;
  ctx.fillText(`MODULE ${L.module} · ${L.moduleTitle}`, M, 150);
  ctx.fillStyle = ACCENT; ctx.fillRect(M, 170, 60, 7);

  ctx.font = `bold 30px ${HEAD}`;
  const badge = `DAY ${dd} / 100`;
  const bw = ctx.measureText(badge).width + 48;
  rr(ctx, W - M - bw, 120, bw, 56, 28); ctx.strokeStyle = ACCENT; ctx.lineWidth = 2; ctx.stroke();
  ctx.fillStyle = ACCENT; ctx.textBaseline = "middle";
  ctx.fillText(badge, W - M - bw + 24, 149); ctx.textBaseline = "alphabetic";

  // title JP + EN
  let y = 300;
  y = drawPara(ctx, L.title, M, y, colW, 66, 82, WHITE, HEAD);
  y += 14;
  y = drawPara(ctx, L.titleEn, M, y, colW, 36, 46, ACCENT, HEAD);

  // divider
  y += 30;
  ctx.strokeStyle = "rgba(255,255,255,0.12)"; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(M, y); ctx.lineTo(W - M, y); ctx.stroke();
  y += 50;

  // body JP (auto-fit) + EN under a mint divider
  const pointBoxH = 220;
  const bodyBottom = H - M - pointBoxH - 40;
  let jpSize = 36, enSize = 30;
  for (const s of [36, 34, 32, 30, 28, 26]) {
    const jpH = measurePara(ctx, L.body, colW, s, s + 14, BODY);
    const enH = measurePara(ctx, L.bodyEn, colW, s - 4, s + 8, BODY);
    if (y + jpH + 34 + enH <= bodyBottom) { jpSize = s; enSize = s - 4; break; }
    jpSize = s; enSize = s - 4;
  }
  let by = drawPara(ctx, L.body, M, y, colW, jpSize, jpSize + 14, BODYCOL, BODY);
  by += 18;
  ctx.strokeStyle = "rgba(95,227,161,0.35)"; ctx.lineWidth = 2;
  ctx.beginPath(); ctx.moveTo(M, by); ctx.lineTo(M + 90, by); ctx.stroke();
  by += 30;
  drawPara(ctx, L.bodyEn, M, by, colW, enSize, enSize + 10, GRAY, BODY);

  // key-point box
  const pbY = H - M - pointBoxH;
  rr(ctx, M, pbY, colW, pointBoxH, 24);
  ctx.fillStyle = "rgba(95,227,161,0.10)"; ctx.fill();
  rr(ctx, M, pbY, colW, pointBoxH, 24); ctx.strokeStyle = ACCENT; ctx.lineWidth = 2; ctx.stroke();
  ctx.font = `bold 24px ${HEAD}`; ctx.fillStyle = ACCENT;
  ctx.fillText("今日のポイント / KEY", M + 32, pbY + 48);
  let py = drawPara(ctx, L.point, M + 32, pbY + 92, colW - 64, 32, 40, WHITE, HEAD);
  drawPara(ctx, L.pointEn, M + 32, py + 8, colW - 64, 24, 30, GRAY, BODY);

  // footer
  ctx.font = `22px ${BODY}`; ctx.fillStyle = GRAY;
  ctx.fillText("@KEEPIX.GK_OFFICIAL", M, H - 40);
  ctx.textAlign = "right"; ctx.font = `bold 22px ${HEAD}`; ctx.fillStyle = ACCENT;
  ctx.fillText("100日GK講座", W - M, H - 40); ctx.textAlign = "left";

  return canvas.toBuffer("image/png");
}
