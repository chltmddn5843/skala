<script setup>
import { computed } from 'vue'
import { useConfigStore } from '@/stores/configStore'

const props = defineProps({
  cityItem: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['select-card', 'click-detail', 'favorite'])
const configStore = useConfigStore()
const displayTemp = computed(() =>
  configStore.unit === 'celsius' ? props.cityItem.temp : (props.cityItem.temp * 9) / 5 + 32,
)



</script>

<template>
  <div class="weather-card" @click="emit('select-card', `${cityItem.name}이 선택되었습니다.`)">
    <h4>{{ cityItem.name }} ({{ cityItem.status }})</h4>
    <p>현재 기온: {{ displayTemp }}{{ configStore.unitSymbol }}</p>

    <span v-if="cityItem.temp >= 25" class="badge hot">🔥 더움</span>
    <span v-else class="badge cool">❄️ 선선함</span>

    <button class="btn-detail" @click.stop="emit('click-detail', cityItem.name, cityItem.status)">상세보기</button>

    <button class="btn-favorite" @click.stop="emit('favorite', cityItem)">즐겨찾기</button>
  </div>
</template>


<style scoped>
.weather-card {
  background: #fff;
  border: 2px solid #dee2e6;
  padding: 12px 15px;
  margin-bottom: 8px;
  border-radius: 6px;
  cursor: pointer;

  /* 1. 플렉스박스로 변경하여 내부 요소를 좌우 정렬 */
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-sizing: border-box;
  width: 100%;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  font-size: 12px;
  border-radius: 4px;
  color: #fff;
}

.hot {
  background-color: #ff7675;
}

.cool {
  background-color: #74b9ff;
}

.btn-detail {
  position: static;
  padding: 6px 12px;
  cursor: pointer;
  white-space: nowrap; /* 버튼 글자가 줄바꿈되지 않도록 방지 */
}
</style>
