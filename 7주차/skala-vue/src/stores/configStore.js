import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export const useConfigStore = defineStore('config', () => {
  const unit = ref('celsius')
  const toggleCount = ref(0)

  const unitSymbol = computed(() =>
    unit.value === 'celsius' ? '℃' : '℉',
  )

  const unitLabel = computed(() =>
    unit.value === 'celsius' ? '섭씨' : '화씨',
  )

  function toggleUnit() {
    unit.value =
      unit.value === 'celsius' ? 'fahrenheit' : 'celsius'

    toggleCount.value++
  }

  function resetUnit() {
    unit.value = 'celsius'
    toggleCount.value = 0
  }

  return {
    unit,
    unitSymbol,
    unitLabel,
    toggleCount,
    toggleUnit,
    resetUnit,
  }
})
