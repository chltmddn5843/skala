import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const workspaceDir = "/Users/chltmddn5843/Downloads/skala";
const skillDir = "/Users/chltmddn5843/.codex/plugins/cache/openai-primary-runtime/presentations/26.905.11957/skills/presentations";
const tmpDir = path.join(workspaceDir, ".codex-build/partflow-ui-api");
const finalPath = path.join(workspaceDir, "PartFlow-최종제출", "PartFlow_UI_API_매핑_v2.pptx");
const font = "Apple SD Gothic Neo";
const W = 1280;
const H = 720;

const { finalizePresentation } = await import(
  pathToFileURL(path.join(skillDir, "container_tools/artifact_tool_utils.mjs")).href,
);

const slides = [
  {
    title: "UI 기능과 API 매핑 | 01 로그인",
    image: path.join(workspaceDir, "wireframe/01.로그인.jpeg"),
    size: [378, 519],
    markers: [{ n: 1, x: 190, y: 267 }],
    calls: [
      { n: 1, method: "POST", path: "/api/auth/login", text: "아이디·비밀번호를 확인하고 세션과 사용자 역할을 반환한다. 성공 후 MANAGER·OPERATOR·QUALITY에 맞는 첫 화면으로 이동한다." },
    ],
    note: "역할별 데모 로그인 버튼도 동일한 로그인 API를 사용하고 계정만 다르다.",
  },
  {
    title: "UI 기능과 API 매핑 | 02 메인페이지",
    image: path.join(workspaceDir, "wireframe/02.메인페이지.jpeg"),
    size: [994, 486],
    markers: [{ n: 1, x: 900, y: 24 }, { n: 2, x: 500, y: 390 }],
    calls: [
      { n: 1, method: "GET", path: "/api/auth/me", text: "현재 로그인한 사용자의 이름과 역할을 조회해 상단에 표시한다." },
      { n: 2, method: "GET", path: "/api/dashboard", text: "오늘의 작업지시 실적과 품질 확인대기 LOT를 조회해 '오늘의 확인 항목'에 표시한다." },
    ],
    note: "작업지시·생산 기록·품질관리 카드는 화면 이동 기능이며 API를 직접 호출하지 않는다.",
  },
  {
    title: "UI 기능과 API 매핑 | 03 작업지시",
    image: path.join(workspaceDir, "wireframe/03.작업지시.jpeg"),
    size: [1026, 347],
    markers: [{ n: 1, x: 450, y: 145 }, { n: 2, x: 925, y: 75 }, { n: 3, x: 115, y: 208 }],
    calls: [
      { n: 1, method: "GET", path: "/api/work-orders", text: "작업지시 목록과 품목·진행률·납기·상태를 조회한다." },
      { n: 2, method: "POST", path: "/api/work-orders", text: "품목, 목표수량, 예정일을 받아 PLANNED 상태의 작업지시를 생성한다." },
      { n: 3, method: "GET", path: "/api/work-orders/{id}", text: "지시번호를 클릭하면 누적 생산량과 연결 LOT를 포함한 상세를 조회한다." },
    ],
  },
  {
    title: "UI 기능과 API 매핑 | 04 지시 상세",
    image: path.join(workspaceDir, "wireframe/04.지시상세.jpeg"),
    size: [970, 686],
    markers: [{ n: 1, x: 150, y: 66 }, { n: 2, x: 892, y: 70 }, { n: 3, x: 95, y: 385 }, { n: 4, x: 82, y: 612 }],
    calls: [
      { n: 1, method: "GET", path: "/api/work-orders/{id}", text: "목표수량, 누적 실적, 진행률과 연결 LOT 목록을 조회한다." },
      { n: 2, method: "POST", path: "/api/work-orders/{id}/close", text: "진행 중인 작업지시를 종료한다. 목표 미달이면 종료 사유를 함께 저장한다." },
      { n: 3, method: "POST", path: "/api/work-orders/{id}/lots", text: "LOT 번호·설비·수량·생산시간을 저장하고 지시의 누적 실적을 갱신한다." },
      { n: 4, method: "POST", path: "/api/work-orders/{id}/lots/{lotId}/anomalies", text: "이상 유형·발생시각·관찰 메모를 저장해 LOT를 품질 확인대기 대상으로 표시한다." },
    ],
  },
  {
    title: "UI 기능과 API 매핑 | 05 LOT 상세",
    image: path.join(workspaceDir, "wireframe/05.LOT상세.jpeg"),
    size: [963, 607],
    markers: [{ n: 1, x: 140, y: 64 }, { n: 2, x: 190, y: 420 }, { n: 3, x: 105, y: 468 }],
    calls: [
      { n: 1, method: "GET", path: "/api/lots/{id}", text: "LOT의 생산·규격·검사결과·AI 요약 이력을 한 번에 조회한다." },
      { n: 2, method: "GET", path: "/api/lots/{id}/related", text: "같은 품목·설비·생산일을 기준으로 관련 LOT 후보를 조회한다." },
      { n: 3, method: "POST", path: "/api/lots/{id}/ai-summaries", text: "선택한 relatedLotIds와 기준 LOT를 함께 분석해 AI 요약을 생성하고 근거 LOT 스냅샷을 저장한다." },
    ],
    note: "AI 요약은 검사가 확정된 LOT에서만 생성할 수 있다.",
  },
  {
    title: "UI 기능과 API 매핑 | 06 검사 등록",
    image: path.join(workspaceDir, "wireframe/06.검사등록.jpeg"),
    size: [1013, 550],
    markers: [{ n: 1, x: 240, y: 72 }, { n: 2, x: 95, y: 483 }],
    calls: [
      { n: 1, method: "GET", path: "/api/lots/{id}", text: "LOT 수량과 생산 시점의 규격을 조회해 측정값 입력 화면을 구성한다." },
      { n: 2, method: "POST", path: "/api/lots/{id}/inspection", text: "제품 순번별 측정값과 검사 메모를 저장한다. 서버가 9.90~10.10 mm 규격과 비교해 PASS/FAIL을 계산한다." },
    ],
    note: "측정값 개수가 LOT 생산수량과 다르면 확정을 거절하며, LOT당 검사는 1회만 확정한다.",
  },
];

function addShape(slide, geometry, position, fill, line = { fill: "none", width: 0 }) {
  return slide.shapes.add({ geometry, position, fill, line });
}

function addText(slide, text, position, style = {}) {
  const box = addShape(slide, "textbox", position, "none");
  box.text = text;
  box.text.style = {
    typeface: font,
    fontSize: style.fontSize ?? 18,
    bold: style.bold ?? false,
    color: style.color ?? "#20242C",
    autoFit: "shrinkText",
    alignment: style.alignment ?? "left",
    verticalAlignment: style.verticalAlignment ?? "middle",
    padding: style.padding ?? 0,
  };
  return box;
}

function methodColor(method) {
  return method === "GET" ? "#0F766E" : "#EA580C";
}

function fitRect(nativeW, nativeH, frame) {
  const scale = Math.min(frame.width / nativeW, frame.height / nativeH);
  const width = nativeW * scale;
  const height = nativeH * scale;
  return {
    left: frame.left + (frame.width - width) / 2,
    top: frame.top + (frame.height - height) / 2,
    width,
    height,
  };
}

function marker(slide, imageRect, nativeSize, item) {
  const [nativeW, nativeH] = nativeSize;
  const cx = imageRect.left + (item.x / nativeW) * imageRect.width;
  const cy = imageRect.top + (item.y / nativeH) * imageRect.height;
  addShape(slide, "ellipse", { left: cx - 15, top: cy - 15, width: 30, height: 30 }, "#F97316", { fill: "#FFFFFF", width: 2 });
  addText(slide, String(item.n), { left: cx - 15, top: cy - 14, width: 30, height: 28 }, { fontSize: 15, bold: true, color: "#FFFFFF", alignment: "center" });
}

function callout(slide, call, x, y, width, height) {
  addShape(slide, "roundRect", { left: x, top: y, width, height }, "#FFFFFF", { fill: "#D9DEE7", width: 1 });
  addShape(slide, "ellipse", { left: x + 14, top: y + 14, width: 30, height: 30 }, "#F97316", { fill: "#F97316", width: 0 });
  addText(slide, String(call.n), { left: x + 14, top: y + 14, width: 30, height: 29 }, { fontSize: 15, bold: true, color: "#FFFFFF", alignment: "center" });
  const color = methodColor(call.method);
  addShape(slide, "roundRect", { left: x + 54, top: y + 13, width: 56, height: 27 }, color, { fill: color, width: 0 });
  addText(slide, call.method, { left: x + 54, top: y + 13, width: 56, height: 26 }, { fontSize: 13, bold: true, color: "#FFFFFF", alignment: "center" });
  const longPath = call.path.length > 34;
  addText(
    slide,
    call.path,
    longPath
      ? { left: x + 16, top: y + 42, width: width - 32, height: 22 }
      : { left: x + 118, top: y + 10, width: width - 132, height: 34 },
    { fontSize: longPath ? 11 : 16, bold: true, color },
  );
  addText(
    slide,
    call.text,
    { left: x + 16, top: y + (longPath ? 66 : 48), width: width - 32, height: height - (longPath ? 72 : 56) },
    { fontSize: 14, color: "#394150", verticalAlignment: "top", padding: 2 },
  );
}

const presentation = Presentation.create({ slideSize: { width: W, height: H } });

for (let i = 0; i < slides.length; i += 1) {
  const data = slides[i];
  const slide = presentation.slides.add();
  slide.background.fill = "#F5F7FB";
  addShape(slide, "rect", { left: 0, top: 0, width: 18, height: H }, "#F97316");
  addText(slide, data.title, { left: 48, top: 28, width: 920, height: 48 }, { fontSize: 29, bold: true, color: "#20242C" });
  addText(slide, `${String(i + 1).padStart(2, "0")} / ${String(slides.length).padStart(2, "0")}`, { left: 1130, top: 34, width: 100, height: 34 }, { fontSize: 14, bold: true, color: "#8A94A6", alignment: "right" });

  const imageFrame = data.size[1] / data.size[0] > 1.1
    ? { left: 58, top: 103, width: 620, height: 560 }
    : { left: 38, top: 106, width: 820, height: 548 };
  const imageRect = fitRect(data.size[0], data.size[1], imageFrame);
  addShape(slide, "roundRect", { left: imageRect.left - 8, top: imageRect.top - 8, width: imageRect.width + 16, height: imageRect.height + 16 }, "#FFFFFF", { fill: "#D9DEE7", width: 1 });
  const bytes = await fs.readFile(data.image);
  slide.images.add({ blob: bytes, contentType: "image/jpeg", alt: `${data.title} UI`, fit: "contain", position: imageRect });
  for (const item of data.markers) marker(slide, imageRect, data.size, item);

  const callX = data.size[1] / data.size[0] > 1.1 ? 720 : 892;
  const callWidth = data.size[1] / data.size[0] > 1.1 ? 510 : 350;
  const top = 112;
  const available = data.note ? 486 : 540;
  const gap = 12;
  const callHeight = Math.min(148, (available - gap * (data.calls.length - 1)) / data.calls.length);
  data.calls.forEach((call, idx) => callout(slide, call, callX, top + idx * (callHeight + gap), callWidth, callHeight));
  if (data.note) {
    const noteTop = top + data.calls.length * (callHeight + gap) + 8;
    addShape(slide, "roundRect", { left: callX, top: noteTop, width: callWidth, height: 70 }, "#FFF7ED", { fill: "#FDBA74", width: 1 });
    addText(slide, data.note, { left: callX + 16, top: noteTop + 8, width: callWidth - 32, height: 54 }, { fontSize: 14, color: "#9A3412" });
  }
  slide.speakerNotes.textFrame.setText(
    `근거: ${path.join(workspaceDir, "PartFlow-최종제출/PartFlow-API.yml")}; ${path.join(workspaceDir, "PartFlow-최종제출/PartFlow_API_설계.md")}. 화면 원본: ${data.image}`,
  );
}

await fs.mkdir(tmpDir, { recursive: true });
await fs.mkdir(path.dirname(finalPath), { recursive: true });
const stagingDir = path.join(workspaceDir, ".codex-finalizer-partflow-ui-api");
await fs.mkdir(stagingDir, { recursive: true });
const candidatePath = path.join(stagingDir, "candidate.pptx");
await (await PresentationFile.exportPptx(presentation)).save(candidatePath);

await finalizePresentation({
  explicitTotalSlideCount: slides.length,
  requiredNativeTableOwnerSlides: [],
  requiredNativeChartOwnerSlides: [],
  workspaceDir,
  candidatePath,
  finalPath,
  pythonExecutable: "/Users/chltmddn5843/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
  integrityValidatorPath: path.join(skillDir, "container_tools/inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(skillDir, "container_tools/inspect_presentation_layout_geometry.py"),
  layoutArgs: ["--expected-slide-size-emu", "12192000,6858000", "--validate-heading-fit"],
  fontPolicy: { basis: "design", families: [font] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(stagingDir, "PartFlow_UI_API_매핑_v2.validation.json"),
});

console.log(finalPath);
