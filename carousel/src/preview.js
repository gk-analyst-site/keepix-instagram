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
    {
      type: "cover", kicker: "GK COACHING",
      title: "1対1で角度を切る", titleEn: "Cutting the angle in 1v1",
      subtitle: "飛び込む前に、まず身体の向きで勝つ", subtitleEn: "Win with your position before you dive",
    },
    {
      type: "content", badge: "1",
      heading: "なぜ角度なのか", headingEn: "Why the angle matters",
      body: "シューターが狙えるコースの幅は、キーパーの位置で決まる。前に出れば、相手の面積は小さくなる。",
      bodyEn: "The width a striker can aim at is set by where you stand. Step out and the target shrinks.",
    },
    {
      type: "content", badge: "2",
      heading: "出るタイミング", headingEn: "When to step out",
      body: "ボールが足を離れる前に、小さく速く前へ。\n\n- 一歩目は短く\n- 上体は起こす\n- 最後は止まって構える",
      bodyEn: "Move before the ball leaves their foot.\n\n- Short first step\n- Stay tall\n- Set before the shot",
    },
    {
      type: "cta", kicker: "KEEPIX",
      title: "続きは連載で", titleEn: "More in the series",
      body: "保存して次の練習で試そう。", bodyEn: "Save it for your next session.",
    },
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
