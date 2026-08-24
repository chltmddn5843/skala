<script setup>
import { computed, ref } from 'vue'

const newTodo = ref('')
const todos = ref([])
let nextId = 1

const remaining = computed(() => todos.value.filter((todo) => !todo.done).length)

function addTodo() {
  const text = newTodo.value.trim()
  if (!text) return

  todos.value.push({ id: nextId++, text, done: false })
  newTodo.value = ''
}

function removeTodo(id) {
  todos.value = todos.value.filter((todo) => todo.id !== id)
}
</script>

<template>
  <section class="practice-section">
    <h2>할 일 목록</h2>

    <form class="todo-form" @submit.prevent="addTodo">
      <input v-model="newTodo" aria-label="새 할 일" placeholder="할 일을 입력하세요" />
      <button>추가</button>
    </form>

    <p>남은 할 일: {{ remaining }}개</p>

    <ul v-if="todos.length">
      <li v-for="todo in todos" :key="todo.id">
        <label :class="{ done: todo.done }">
          <input v-model="todo.done" type="checkbox" />
          {{ todo.text }}
        </label>
        <button type="button" @click="removeTodo(todo.id)">삭제</button>
      </li>
    </ul>
    <p v-else>등록된 할 일이 없습니다.</p>
  </section>
</template>

<style scoped>
.todo-form,
li {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

li {
  justify-content: space-between;
}

.done {
  color: #888;
  text-decoration: line-through;
}
</style>
