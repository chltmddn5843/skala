import fs from "node:fs/promises";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const [sourcePath, outputDir] = process.argv.slice(2);
const deck = await PresentationFile.importPptx(await FileBlob.load(sourcePath));
await fs.mkdir(outputDir, { recursive: true });
const snapshot = await deck.inspect({
  kind: "deck,slide,textbox,shape,image,table,chart,notes,layout",
  include: "id,slide,name,title,text,textPreview,bbox,bboxUnit,alt,isPlaceholder,placeholders",
  maxChars: 100000,
});
await fs.writeFile(`${outputDir}/inspect.ndjson`, snapshot.ndjson);
const montage = await deck.export({ format: "png", montage: true, scale: 0.6 });
await fs.writeFile(`${outputDir}/montage.png`, new Uint8Array(await montage.arrayBuffer()));
for (let i = 0; i < deck.slides.items.length; i += 1) {
  const slide = deck.slides.getItem(i);
  const preview = await slide.export({ format: "png", scale: 1 });
  await fs.writeFile(`${outputDir}/slide-${String(i + 1).padStart(2, "0")}.png`, new Uint8Array(await preview.arrayBuffer()));
}
console.log(`slides=${deck.slides.items.length}`);
