// 전역 변수로 선언하여 화면 너비의 50% 값을 저장
var screenWidth80Percent = window.innerWidth * 0.5;

let isFirstAnimationPlaying = false;

function createObserver() {
  let observer;

  let options = {
    root: null, // 뷰포트를 루트로 사용
    rootMargin: '0px',
    threshold: 0.5, // 50%가 보일 때 트리거
  };

  observer = new IntersectionObserver(handleIntersect, options);

  // 요소가 존재하는지 확인하고 옵저버로 감시
  const animationText = document.querySelector('#animation-text');
  const wave = document.querySelector('#wave');
  const section2 = document.querySelector('.section-2');

  if (animationText) observer.observe(animationText); // 첫 번째 텍스트 애니메이션 요소 관찰
  if (wave) observer.observe(wave); // 두 번째 텍스트 애니메이션 요소 관찰
  if (section2) observer.observe(section2); // 섹션 2 관찰
}

function handleIntersect(entries, observer) {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      if (entry.target.id === 'animation-text') {
        startFirstAnimation(); // 첫 번째 텍스트 애니메이션 시작
      } else if (entry.target.id === 'wave') {
        startSecondAnimation(); // 두 번째 텍스트 애니메이션 시작
      } else if (entry.target.classList.contains('section-2')) {
        commitAnimation(); // 커밋 애니메이션 시작
      }
    }
  });
}

function startFirstAnimation() {
  if (isFirstAnimationPlaying) return; // 애니메이션이 이미 진행 중이라면 중복 실행 방지

  isFirstAnimationPlaying = true;
  const content = '정글러들의 Github';
  let i = 0;
  const text = document.querySelector('#animation-text');
  text.classList.remove('hidden');

  function typing() {
    const wave = document.querySelector('#wave');
    wave.classList.add('hidden');

    if (i < content.length) {
      let txt = content.charAt(i);
      text.innerHTML += txt;
      i++;
    } else {
      clearInterval(typingInterval); // 타이핑 애니메이션이 완료되면 멈춤
      setTimeout(showSecondText, 1000); // 1초 후에 두 번째 텍스트 표시
    }
  }

  let typingInterval = setInterval(typing, 200);
}

// 두 번째 텍스트 애니메이션 함수
function startSecondAnimation() {
  const wave = document.querySelector('#wave');
  wave.classList.remove('hidden');

  wave.innerHTML = wave.textContent
    .split('')
    .map((letter, idx) => {
      if (letter === ' ') return ' '; // 공백은 그대로 반환
      return `<span style="animation-delay:${
        idx * 15
      }ms" class="letter">${letter}</span>`; // 문자열 템플릿으로 HTML 생성
    })
    .join('');
}

// 두 번째 텍스트 애니메이션 함수
function showSecondText() {
  const text = document.querySelector('#animation-text');
  text.classList.add('hidden');
  startSecondAnimation();
}

function commitAnimation() {
  let countBox = document.querySelector('#animation-commit');
  let count = 0;
  let num = parseInt(countBox.textContent); // 템플릿에서 받은 커밋 수를 가져옴

  let counting = setInterval(function () {
    if (count >= num) {
      count = num;
      clearInterval(counting);
    } else {
      count += Math.ceil(num / 40); // 조금씩 커밋 수 증가
    }
    countBox.innerHTML = new Intl.NumberFormat().format(count);
  }, 10);

  // 커밋 애니메이션 텍스트 보이기
  countBox.hidden = false;
}

// 현재 날짜를 기준으로 DAY를 계산하는 함수
function calculateDay() {
  const now = new Date();
  const startDay = new Date('2024-09-02T00:00:00');
  const oneDay = 24 * 60 * 60 * 1000;

  if (now.getHours() < 6) {
    now.setDate(now.getDate() - 1);
  }

  const diffDays = Math.ceil((now - startDay) / oneDay);
  const dayNumber = Math.ceil(diffDays / 1); // 일(day) 기준으로 DAY 계산

  // 표시할 기간을 설정 (예: 9/3~9/4)
  const periodStart = new Date(now);
  const periodText = `${formatDate(periodStart)}`;

  return `${periodText} (Day ${dayNumber})`;
}

// 날짜 형식을 'MM/DD'로 변환하는 함수
function formatDate(date) {
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  return `${month}/${day}`;
}

// 타일 초기화 함수 (API 없이 애니메이션만 처리)
function TilesAnimation() {
  try {
    // 타일 컨테이너 가져오기
    const tileContainer = document.getElementById('tile-container');

    // 타일 컨테이너의 너비 설정
    tileContainer.style.width = screenWidth80Percent + 'px';

    // 임시 이미지 객체를 만들어 원본 크기를 가져옴
    const tempImage = new Image();
    tempImage.src = 'https://picsum.photos/500';

    tempImage.onload = function () {
      // 숨기고자 하는 타일 ID를 지정하는 배열
      var list = JSON.parse(document.getElementById('openList').textContent);
      // 이미지 로드가 완료된 후에 해상도를 사용하여 높이를 계산
      const imageWidth = this.naturalWidth;
      const imageHeight = this.naturalHeight;
      const imageAspectRatio = imageHeight / imageWidth; // 이미지의 가로:세로 비율 계산

      // 이미지 비율에 맞게 높이 설정
      const containerHeight = screenWidth80Percent * imageAspectRatio;
      tileContainer.style.height = containerHeight + 'px';

      // 타일 초기화 및 애니메이션 처리
      for (let i = 0; i <= 34; i++) {
        const tileContainerElement = document.createElement('div');

        if (list.includes(i)) {
          tileContainerElement.className = 'flip-container'; // list에 있는 타일에 애니메이션 적용

          const tile = document.createElement('div');
          tile.style = 'position: relative; width: 100%; height: 100%;';
          tile.id = 'tile-' + i;
          tile.className = 'flip-card';

          const front = document.createElement('div');
          front.className = 'flip-card-front transparent-tile'; // 투명 타일

          const back = document.createElement('div');
          back.className = 'flip-card-back';

          tile.appendChild(front);
          tile.appendChild(back);
          tileContainerElement.appendChild(tile);

          const observer = new IntersectionObserver(
            (entries) => {
              entries.forEach((entry) => {
                if (entry.isIntersecting) {
                  tile.classList.add('flipped'); // 타일에 플립 클래스 추가
                  observer.unobserve(entry.target); // 애니메이션은 한 번만 실행되도록 옵저버 제거
                }
              });
            },
            {
              threshold: 0.5, // 타일이 50% 이상 보일 때 트리거
            }
          );

          observer.observe(tileContainerElement);
        } else {
          tileContainerElement.className = 'tile bg-green-500 rounded-lg'; // list에 없는 타일은 초록색
        }

        tileContainer.appendChild(tileContainerElement);
      }
    };
  } catch (error) {
    console.error('Error initializing tiles:', error);
  }
}

document.addEventListener('DOMContentLoaded', function () {
  createObserver();

  // 날짜 계산
  document.getElementById('day-display').innerText = calculateDay();

  // 타일 애니메이션 실행
  TilesAnimation();

  // 토큰 로직
  let tokenElement = document.getElementById('token');
  let tokenValue = tokenElement ? tokenElement.value : '';

  // 이전 로컬 스토리지에 저장된 토큰 값 가져오기
  let existingToken = localStorage.getItem('key');

  // 새로운 토큰 값이 빈 문자열이거나 유효하지 않으면 기존 토큰을 유지
  if (tokenValue === '' || tokenValue === null) {
  } else {
    let changedToken = tokenValue.replace(/'/g, '"').replace(/None/g, 'null');
    try {
      let tokenObject = JSON.parse(changedToken);

      if (tokenObject && tokenObject.access_token) {
        localStorage.setItem('key', tokenObject.access_token);
      }
    } catch (e) {
      console.error('JSON 파싱 오류 발생:', e);
    }
  }
});
