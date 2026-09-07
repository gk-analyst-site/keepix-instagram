// preview.js — render a sample carousel locally to carousel/out/_preview/ WITHOUT
// calling Claude or Instagram. Use it to eyeball the design and fonts.
//   node src/preview.js
import { writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { renderSlides } from "./slides.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, "..", "out", "_preview");

const plan = {
  slides: [
    { type: "cover", kicker: "GK COACHING", title: "1対1で角度を切る", subtitle: "飛び込む前に、まず身体の向きで勝つ" },
    { type: "content", badge: "1", heading: "なぜ角度なのか", body: "シューターの選択肢は「コースの幅」で決まる。\n\n前に出て角度を狭めれば、相手が狙える面積そのものが小さくなる。" },
    { type: "content", badge: "2", heading: "出るタイミング", body: "ボールが相手の足を離れる前に、小さく速く前へ。\n\n- 一歩目は短く\n- 上体は起こす\n- 最後は止まって構える" },
    { type: "content", badge: "3", heading: "やりがちなミス", body: "突っ込みすぎると、ループと横パスの両方に遅れる。\n\n「大きく見せて待つ」が基本。" },
    { type: "cta", kicker: "KEEPIX", title: "続きは連載で", body: "保存して次のトレーニングで試そう。" },
  ],
};

async function main() {
  mkdirSync(OUT, { recursive: true });
  const slides = await renderSlides(plan);
  for (const s of slides) {
    writeFileSync(path.join(OUT, s.name), s.buffer);
    console.log("wrote", path.relative(process.cwd(), path.join(OUT, s.name)));
  }
  console.log(`\n${slides.length} slides -> ${OUT}`);
}

main().catch((e) => {
  console.error(e.stack || e.message);
  process.exit(1);
});
