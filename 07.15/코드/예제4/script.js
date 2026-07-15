const input = document.querySelector("#nameInput");
const btn = document.querySelector("#greetBtn");
const result = document.querySelector("#result");

btn.addEventListener("click", function () {
  const name = input.value;
  if (name === "") {
    result.textContent = "이름을 입력해 주세요! 😅";
  } else {
    result.textContent = `안녕하세요, ${name}님! 환영합니다 🎉`;
  }
});