const input = document.querySelector("#todoInput");
const addBtn = document.querySelector("#addBtn");
const list = document.querySelector("#todoList");

function createTodoItem(text) {
  const li = document.createElement("li");
  const span = document.createElement("span");
  span.textContent = text;
  span.className = "todo-text";
  span.addEventListener("click", function () {
    span.classList.toggle("completed");
  });

  const delBtn = document.createElement("button");
  delBtn.textContent = "삭제";
  delBtn.className = "del-btn";
  delBtn.addEventListener("click", function () {
    li.remove();
  });

  li.appendChild(span);
  li.appendChild(delBtn);
  return li;
}

function addTodo(text) {
  list.appendChild(createTodoItem(text));
}

addBtn.addEventListener("click", function () {
  const text = input.value.trim();
  if (text === "") return;

  addTodo(text);
  input.value = "";
  input.focus();
});