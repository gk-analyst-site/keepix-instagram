import { readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { renderCard } from "./card.js";
const m = JSON.parse(readFileSync(new URL("../content/module-01.json", import.meta.url)));
mkdirSync(new URL("../out/_preview/", import.meta.url), { recursive: true });
const days = process.argv.slice(2).map(Number);
const pick = days.length ? m.lessons.filter(l => days.includes(l.day)) : m.lessons;
for (const l of pick) {
  const buf = renderCard({ ...l, module: m.module, moduleTitle: m.moduleTitle, moduleTitleEn: m.moduleTitleEn });
  const name = `day-${String(l.day).padStart(2,"0")}.png`;
  writeFileSync(new URL(`../out/_preview/${name}`, import.meta.url), buf);
  console.log("wrote", name);
}
