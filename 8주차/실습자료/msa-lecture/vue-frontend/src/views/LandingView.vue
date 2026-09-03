<template>
  <div class="landing">
    <AppHeader />

    <!-- 히어로 섹션 -->
    <section class="hero">
      <div class="hero-inner">
        <div class="hero-content fade-in-up">
          <span class="hero-badge">B2B 의료장비 도입 플랫폼</span>
          <h1 class="hero-title">의료장비 탐색부터 도입까지,<br>더 빠르고 투명하게</h1>
          <p class="hero-desc">의료기관과 제조·공급사를 연결해 장비 비교, 구매, 결제와 도입 이력을 한곳에서 관리합니다.</p>
          <div class="hero-actions">
            <router-link to="/login" class="btn btn-primary btn-lg">도입 시작하기</router-link>
            <router-link to="/courses" class="btn btn-outline btn-lg">의료장비 보기</router-link>
          </div>
          <div class="hero-stats">
            <div class="stat"><span class="stat-num">1,200+</span><span class="stat-label">등록 장비</span></div>
            <div class="stat"><span class="stat-num">340+</span><span class="stat-label">제조·공급사</span></div>
            <div class="stat"><span class="stat-num">2,800+</span><span class="stat-label">의료기관</span></div>
          </div>
        </div>
        <div class="hero-visual fade-in">
          <img src="@/assets/images/logo/main_logo.png" alt="MediEquip" class="hero-logo" />
        </div>
      </div>
    </section>

    <!-- 인기 강의 -->
    <section class="popular-section">
      <div class="section-inner">
        <div class="section-header">
          <h2 class="section-title">주요 의료장비</h2>
          <router-link to="/login" class="section-link">전체 보기 →</router-link>
        </div>
        <div class="course-grid">
          <div v-for="course in featuredCourses" :key="course.id" class="course-card-landing">
            <div class="card-thumb" :class="course.thumbBg">
              <img :src="course.thumbSrc" :alt="course.title" class="thumb-img" />
            </div>
            <div class="card-body">
              <span class="badge" :class="course.badgeClass">{{ course.category }}</span>
              <h3 class="card-title">{{ course.title }}</h3>
              <div class="card-meta">
                <span class="instructor">{{ course.instructor }}</span>
                <span class="price">{{ course.price }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 특징 섹션 -->
    <section class="features-section">
      <div class="section-inner">
        <h2 class="section-title center">왜 MediEquip인가요?</h2>
        <div class="features-grid">
          <div v-for="f in features" :key="f.title" class="feature-card">
            <div class="feature-icon">{{ f.icon }}</div>
            <h3 class="feature-title">{{ f.title }}</h3>
            <p class="feature-desc">{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta-section">
      <div class="cta-inner">
        <h2>지금 바로 시작하세요</h2>
        <p>분산된 의료장비 탐색과 구매 업무를 하나의 흐름으로 연결하세요.</p>
        <router-link to="/login" class="btn btn-primary btn-lg">기업 계정 만들기</router-link>
      </div>
    </section>

    <!-- 푸터 -->
    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-logo">
          <img src="@/assets/images/logo/main_logo.png" alt="MediEquip" />
          <span>MediEquip</span>
        </div>
        <p class="footer-copy">© 2026 MediEquip. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import AppHeader from '@/components/AppHeader.vue'

import springImg   from '@/assets/images/courses/spring_boot.png'
import vueImg      from '@/assets/images/courses/vue_js.png'
import k8sImg      from '@/assets/images/courses/kubernetes.png'
import dockerImg   from '@/assets/images/courses/docker.png'
import pythonImg   from '@/assets/images/courses/python.png'
import genaiImg    from '@/assets/images/courses/generative_ai.png'

const featuredCourses = [
  { id:1, title:'환자감시장치 PM-100', category:'환자 모니터링', instructor:'메디서플라이', price:'₩8,900,000', thumbSrc: springImg, thumbBg:'thumb-teal', badgeClass:'badge-teal' },
  { id:2, title:'이동형 초음파 진단기', category:'진단장비', instructor:'케어메디', price:'₩16,900,000', thumbSrc: vueImg, thumbBg:'thumb-teal', badgeClass:'badge-teal' },
  { id:3, title:'자동 생화학 분석기', category:'검사장비', instructor:'바이오헬스', price:'₩29,900,000', thumbSrc: k8sImg, thumbBg:'thumb-blue', badgeClass:'badge-blue' },
  { id:4, title:'전동 수술대 ST-20', category:'수술장비', instructor:'헬스테크', price:'₩17,900,000', thumbSrc: dockerImg, thumbBg:'thumb-blue', badgeClass:'badge-blue' },
  { id:5, title:'디지털 심전도계', category:'진단장비', instructor:'대한메디칼', price:'₩5,900,000', thumbSrc: pythonImg, thumbBg:'thumb-purple', badgeClass:'badge-purple' },
  { id:6, title:'원격 환자 모니터링 허브', category:'디지털 헬스', instructor:'그린바이오', price:'₩7,500,000', thumbSrc: genaiImg, thumbBg:'thumb-pink', badgeClass:'badge-pink' },
]

const features = [
  { icon:'🏥', title:'의료장비 통합 비교', desc:'여러 제조·공급사의 의료장비를 분류별로 빠르게 확인합니다.' },
  { icon:'🎯', title:'맞춤 장비 추천', desc:'도입 이력을 분석해 의료기관에 적합한 미도입 장비를 추천합니다.' },
  { icon:'💳', title:'간편한 구매 처리', desc:'장비 확인부터 결제와 도입 확정까지 한 번에 진행합니다.' },
  { icon:'🔄', title:'실시간 상태 연동', desc:'결제 완료 이벤트를 기반으로 장비 도입 상태를 자동 반영합니다.' },
]
</script>

<style scoped>
.landing { background: var(--color-bg-secondary); }

/* 히어로 */
.hero {
  background: linear-gradient(135deg, #f0f7ff 0%, #e8f4fd 50%, #f0f9ff 100%);
  border-bottom: 1px solid var(--color-border);
  padding: 80px 0 64px;
}
.hero-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 48px;
  align-items: center;
}
.hero-badge {
  display: inline-block;
  padding: 5px 14px;
  background: var(--color-primary-light);
  color: var(--color-primary);
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 16px;
}
.hero-title {
  font-size: 42px;
  font-weight: 700;
  line-height: 1.25;
  letter-spacing: -0.5px;
  color: var(--color-text-primary);
  margin-bottom: 16px;
}
.hero-desc {
  font-size: 16px;
  color: var(--color-text-secondary);
  line-height: 1.7;
  max-width: 460px;
  margin-bottom: 28px;
}
.hero-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 40px;
}
.btn-lg { padding: 12px 28px; font-size: 15px; }
.hero-stats {
  display: flex;
  gap: 36px;
}
.stat { display: flex; flex-direction: column; gap: 2px; }
.stat-num { font-size: 22px; font-weight: 700; color: var(--color-primary); }
.stat-label { font-size: 12px; color: var(--color-text-secondary); }
.hero-visual {
  display: flex;
  align-items: center;
  justify-content: center;
}
.hero-logo {
  width: 200px;
  height: 200px;
  object-fit: contain;
  border-radius: 24px;
  box-shadow: var(--shadow-lg);
}

/* 강의 섹션 */
.popular-section { padding: 64px 0; }
.section-inner { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.section-title { font-size: 22px; font-weight: 700; color: var(--color-text-primary); }
.section-title.center { text-align: center; margin-bottom: 40px; }
.section-link { font-size: 14px; color: var(--color-primary); font-weight: 500; }
.section-link:hover { text-decoration: underline; }

.course-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.course-card-landing {
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: var(--transition);
}
.course-card-landing:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}
.card-thumb {
  height: 110px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.thumb-teal   { background: #E1F5EE; }
.thumb-blue   { background: #E6F1FB; }
.thumb-purple { background: #EEEDFE; }
.thumb-pink   { background: #FBEAF0; }
.thumb-img { width: 100%; height: 100%; object-fit: contain; padding: 14px; }
.card-body { padding: 14px 16px; display: flex; flex-direction: column; gap: 6px; }
.card-title { font-size: 14px; font-weight: 600; color: var(--color-text-primary); line-height: 1.4; }
.card-meta { display: flex; justify-content: space-between; align-items: center; }
.instructor { font-size: 12px; color: var(--color-text-secondary); }
.price { font-size: 14px; font-weight: 600; color: var(--color-primary); }

/* 특징 */
.features-section { padding: 64px 0; background: var(--color-bg-primary); }
.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}
.feature-card {
  padding: 28px 24px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  text-align: center;
  transition: var(--transition);
}
.feature-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.feature-icon { font-size: 32px; margin-bottom: 12px; }
.feature-title { font-size: 15px; font-weight: 600; margin-bottom: 8px; }
.feature-desc { font-size: 13px; color: var(--color-text-secondary); line-height: 1.6; }

/* CTA */
.cta-section {
  padding: 80px 0;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  text-align: center;
}
.cta-inner { max-width: 600px; margin: 0 auto; padding: 0 24px; }
.cta-inner h2 { font-size: 32px; font-weight: 700; color: #fff; margin-bottom: 12px; }
.cta-inner p { font-size: 16px; color: rgba(255,255,255,0.8); margin-bottom: 32px; }
.cta-inner .btn-primary {
  background: #fff;
  color: var(--color-primary);
  border-color: #fff;
  font-weight: 600;
}
.cta-inner .btn-primary:hover { background: #f0f7ff; }

/* 푸터 */
.footer {
  background: var(--color-text-primary);
  padding: 32px 0;
}
.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.footer-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fff;
  font-size: 15px;
  font-weight: 600;
}
.footer-logo img { width: 28px; height: 28px; border-radius: 6px; }
.footer-copy { font-size: 13px; color: rgba(255,255,255,0.5); }
</style>
