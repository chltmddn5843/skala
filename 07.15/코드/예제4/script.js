// 1. HTML에서 토글 버튼과 네비게이션 메뉴 요소를 가져옵니다.
const menuToggle = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('.main-navigation');

// 2. 버튼 클릭 시 동작할 이벤트를 추가합니다.
menuToggle.addEventListener('click', () => {
  // main-navigation 요소에 'active' 클래스가 있으면 제거하고, 없으면 추가합니다.
  mainNav.classList.toggle('active');
  
  // 버튼 클릭 시 햄버거 모양이 가볍게 변하도록 효과를 줍니다.
  menuToggle.classList.toggle('is-open');
});