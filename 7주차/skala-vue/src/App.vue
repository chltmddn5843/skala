<script setup>
import Test from './components/practices/basic/test.vue'
import VueHtml from './components/practices/basic/VueHtml.vue'
import VueHtmlXss from './components/practices/basic/VueHtmlXss.vue'
import VueText from './components/practices/basic/VueText.vue'
import VueBind from './components/practices/basic/VueBind.vue'
import VueBindClass from './components/practices/basic/VueBindClass.vue'
import VueBindStyle from './components/practices/basic/VueBindStyle.vue'
import VueBindShorthand from './components/practices/basic/VueBindShorthand.vue'
import VueIf from './components/practices/basic/VueIf.vue'
import VueShow from './components/practices/basic/VueShow.vue'
import VueFor from './components/practices/basic/VueFor.vue'
import VuePre from './components/practices/basic/VuePre.vue'
import VueCloak from './components/practices/basic/VueCloak.vue'
import VueOnce from './components/practices/basic/VueOnce.vue'
import VueMemo from './components/practices/basic/VueMemo.vue'
</script>

<template>
  <div class="practice-container">
    <h1>1. 테스트 실습</h1>
    <hr />
    <Test />

    <h1>2. Vue HTML</h1>
    <hr />
    <VueHtml />

    <h1>3. Vue HTML XSS</h1>
    <hr />
    <VueHtmlXss />

    <h1>4. Vue Text</h1>
    <hr />
    <VueText />

    <h1>5. Vue Bind</h1>
    <hr />
    <VueBind />

    <h1>6. Vue Bind Class</h1>
    <hr />
    <VueBindClass />

    <h1>7. Vue Bind Style</h1>
    <hr />
    <VueBindStyle />

    <h1>8. Vue Bind Shorthand</h1>
    <hr />
    <VueBindShorthand />

    <h1>9. Vue If</h1>
    <hr />
    <VueIf />

    <h1>10. Vue Show</h1>
    <hr />
    <VueShow />

    <h1>11. Vue For</h1>
    <hr />
    <VueFor />

    <h1>12. Vue Pre</h1>
    <hr />
    <VuePre />

    <h1>13. Vue Cloak</h1>
    <hr />
    <VueCloak />

    <h1>14. Vue Once</h1>
    <hr />
    <VueOnce />

    <h1>15. Vue Memo</h1>
    <hr />
    <VueMemo />
  </div>
</template>

<style>
@import '@/assets/practice.css';
</style>
