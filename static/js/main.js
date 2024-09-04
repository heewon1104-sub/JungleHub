// 전역 변수로 선언하여 화면 너비의 50% 값을 저장
var screenWidth80Percent = window.innerWidth * 0.5;

// 숨기고자 하는 타일 ID를 지정하는 배열
var list = [1, 3, 6, 20, 21, 34];

// 페이지 로드 시 DAY 계산 및 업데이트
window.onload = function () {
  document.getElementById('day-display').innerText = calculateDay();
};

// 현재 날짜를 기준으로 DAY를 계산하는 함수
function calculateDay() {
  const now = new Date();
  const startDay = new Date('2024-09-01T06:00:00'); // 기준 시작 날짜와 시간 (9/1 06:00am)
  const oneDay = 24 * 60 * 60 * 1000; // 하루를 밀리초로 변환

  // 현재 시간이 6시 이전이면 어제 날짜를 기준으로 계산
  if (now.getHours() < 6) {
    now.setDate(now.getDate() - 1);
  }

  const diffDays = Math.floor((now - startDay) / oneDay); // 시작일로부터 경과한 일 수 계산
  const dayNumber = Math.floor(diffDays / 1); // 일(day) 기준으로 DAY 계산

  // 표시할 기간을 설정 (예: 9/3~9/4)
  const periodStart = new Date(
    startDay.getTime() + dayNumber * oneDay + oneDay
  );
  const periodEnd = new Date(periodStart.getTime() + oneDay);
  const periodText = `${formatDate(periodStart)} ~ ${formatDate(periodEnd)}`;

  return `DAY${dayNumber + 1} (${periodText})`;
}

// 날짜 형식을 'MM/DD'로 변환하는 함수
function formatDate(date) {
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  return `${month}/${day}`;
}

// 페이지 로드 시 DAY 계산 및 업데이트
window.onload = function () {
  document.getElementById('day-display').innerText = calculateDay();
};
