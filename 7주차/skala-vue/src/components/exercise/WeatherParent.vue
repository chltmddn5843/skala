<script setup>
import { ref, computed, watch, watchEffect } from 'vue'
// 1. 컴포넌트 파일명 국룰 표기법(PascalCase) 매칭 수입
import BaseDashboardCard from './BaseDashboardCard.vue'
import SearchBar from './SearchBar.vue'
import WeatherCard from './WeatherCard.vue'

const weatherList = ref([
  { id: 'city_01', name: '인천', temp: 22, status: '흐림' , moisture: 80},
  { id: 'city_02', name: '부산', temp: 25, status: '맑음' , moisture: 60},
  { id: 'city_03', name: '대전', temp: 24, status: '비' , moisture: 90},
  { id: 'city_04', name: '광주', temp: 27, status: '맑음' , moisture: 50},
  { id: 'city_05', name: '대구', temp: 23, status: '흐림' , moisture: 70},
])

const favoriteCity = ref(null) // 즐겨찾기 도시 목록
const handleFavorite = (city) => {
  favoriteCity.value = city
}


const searchQuery = ref('')
const selectedCityInfo = ref('카드를 클릭하거나 검색해 보세요.')


const filteredWeatherList = computed(() => {
  const query = searchQuery.value.trim()
  if (!query) return weatherList.value
  return weatherList.value.filter((item) => item.name.includes(query))
})

watch(selectedCityInfo, (newInfo) => {
  console.log(`👁️‍🗨️ [watch 감지] 상태 바 문구가 업데이트되었습니다 -> "${newInfo}"`)
})

watchEffect(() => {
  console.log(`🤖 [watchEffect 자동 호출] 현재 검색어 '${searchQuery.value}'에 매칭되는 API 데이터를 필터링합니다.`)
})

const showDetail = (cityName, status) => {
  window.alert(`${cityName}의 현재 날씨는 [${status}] 상태입니다.`)
}
</script>

<template>
  <div class="dashboard-wrapper">
    <BaseDashboardCard>
      <SearchBar :current-query="searchQuery" @update-query="(val) => (searchQuery = val)" />
    </BaseDashboardCard>

    <BaseDashboardCard>
      <h3>🏙️ 지역별 날씨 현황</h3>

      <WeatherCard
        v-for="item in filteredWeatherList"
        :key="item.id"
        :city-item="item"
        @select-card="(msg) => (selectedCityInfo = msg)"
        @click-detail="showDetail"
        @favorite="handleFavorite"
      />

      <p v-if="filteredWeatherList.length === 0" style="text-align: center; color: #e74c3c; padding: 10px 0">😭 검색 결과와 일치하는 도시가 없습니다.</p>
    </BaseDashboardCard>

    <div class="status-bar">
      {{ selectedCityInfo }}
    </div>

    <div v-if="favoriteCity" class="favorite-info">
      <h4>⭐ 즐겨찾기 도시</h4>
      <p>{{ favoriteCity.name }} ({{ favoriteCity.status }})</p>
      <p>현재 기온: {{ favoriteCity.temp }}°C</p>
      <p>현재 습도: {{ favoriteCity.moisture }}%</p>
    </div>
  </div>
</template>

<style scoped>
.dashboard-wrapper {
  width: 600px;
  margin: 0 auto;
}
</style>
