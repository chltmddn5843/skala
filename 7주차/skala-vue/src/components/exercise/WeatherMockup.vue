<script setup>
import { ref } from 'vue'
const weatherList = ref([
  { id: 'city_01', name: '인천', temp: 19, status: '흐림' , moisture: 80},
  { id: 'city_02', name: '부산', temp: 25, status: '맑음' , moisture: 60},
  { id: 'city_03', name: '대전', temp: 24, status: '비' , moisture: 90},
  { id: 'city_04', name: '광주', temp: 27, status: '맑음' , moisture: 50},
  { id: 'city_05', name: '대구', temp: 23, status: '흐림' , moisture: 70},
])

const searchQuery = ref('')
const selectedCityInfo = ref('카드를 클릭하거나 검색해 보세요.')

const showDetail = (cityName, status, moisture) => {
  window.alert(`${cityName}의 현재 날씨는 [${status}] 상태입니다. 습도는 ${moisture}%입니다.`)
}
</script>




<template>
  <div class="dashboard-wrapper">
    <section class="search-box">
      <h3>🔍 도시 검색</h3>
      <input type="text" :value="searchQuery" @input="(e) => (searchQuery = e.target.value)" placeholder="도시 이름 입력" />
    <p>검색 중인 도시: <strong>{{ searchQuery }}</strong></p>
    </section>

    <section class="list-box">
      <h3>🏙️ 지역별 날씨 현황</h3>
      <div v-for="item in weatherList" :key="item.id" class="weather-card" @click="selectedCityInfo = `${item.name}이 선택되었습니다.`">
        <h4>{{ item.name }} ({{ item.status }})</h4>
        <p>현재 기온: {{ item.temp }}°C</p>
        <p>현재 습도: {{ item.moisture }}%</p>

        <span v-if="item.temp >= 25" class="badge hot">🔥 더움 (25도 이상)</span>
        <span v-else-if="item.temp >= 21" class="badge warm">🌤️ 따뜻함 (21~24도)</span>
        <span v-else class="badge cool">❄️ 선선함 (20도 미만)</span>

        <button class="btn-detail" @click.stop="showDetail(item.name, item.status, item.moisture)">상세보기</button>
      </div>
    </section>

    <div class="status-bar">
      {{ selectedCityInfo }}
    </div>
  </div>
</template>
