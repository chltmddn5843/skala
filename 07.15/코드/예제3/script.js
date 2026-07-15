let count = 0;
const countEl = document.querySelector("#count");
const likeBtn = document.querySelector("#likeBtn");
const dislikeBtn = document.querySelector("#dislikeBtn");

likeBtn.addEventListener("click", function () {
  count = count + 2;
  countEl.textContent = count;
});

dislikeBtn.addEventListener("click", function () {
  count = count - 2;
  countEl.textContent = count;
});