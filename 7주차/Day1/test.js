
function myDisplayer(some) {
  document.getElementById("demo").textContent = some;
}

// 3개 비동기 함수는 순서대로 실행되어야 함.
function step1() {
  return Promise.resolve("A");
}

function step2(value) {
  return Promise.resolve(value + "B");
}

function step3(value) {
  return Promise.resolve(value + "C");
}

// async와 await를 이용해 구현
async function run() {
  const v1 = await step1();
  const v2 = await step2(v1);
  const v3 = await step3(v2);
  myDisplayer(v3);
}

run();
