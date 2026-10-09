// 글로벌 상태 관리
let currentTab = 'home';
let globalDays = [];
let globalStats = null;
let currentDayDetail = null;
let hideKoreanState = false;
let expandedThemes = { 0: true }; // 기본적으로 첫 번째 테마 열어둠
let playingTtsId = null;

// DOM 로딩 완료 후 실행
document.addEventListener('DOMContentLoaded', () => {
  initApp();
});

// 앱 초기 설정
async function initApp() {
  setupTabbar();
  setupEventListeners();
  
  // 첫 진입 시 홈 데이터 로드
  await fetchGlobalData();
  renderView('home');
}

// 탭바 버튼 바인딩
function setupTabbar() {
  const tabButtons = document.querySelectorAll('.tabbar-item');
  tabButtons.forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const targetTab = btn.getAttribute('data-tab');
      if (!targetTab) return;
      
      // 탭 토글
      tabButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      currentTab = targetTab;
      
      // 상세 뷰가 열려 있었다면 목록 뷰로 초기화 (Study 탭 클릭 시)
      if (currentTab === 'study') {
        document.getElementById('study-list-container').style.display = 'flex';
        document.getElementById('study-detail-container').style.display = 'none';
      }

      // 데이터 새로 패치 후 렌더링
      await fetchGlobalData();
      renderView(currentTab);
    });
  });
}

// 공통 데이터 패치
async function fetchGlobalData() {
  showGlobalSpinner(true);
  try {
    const [daysRes, statsRes] = await Promise.all([
      fetch('/api/days'),
      fetch('/api/stats')
    ]);
    
    if (daysRes.ok && statsRes.ok) {
      globalDays = await daysRes.json();
      globalStats = await statsRes.json();
    }
  } catch (error) {
    console.error('Error fetching global data:', error);
  } finally {
    showGlobalSpinner(false);
  }
}

// 뷰 렌더링 분기
function renderView(tabName) {
  // 모든 뷰 숨기기
  document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));
  
  // 타겟 뷰 보이기
  const activeSec = document.getElementById(`${tabName}-view`);
  if (activeSec) activeSec.classList.add('active');
  
  // 헤더 타이틀 매핑
  const headerTitle = document.getElementById('header-title');
  if (headerTitle) {
    switch (tabName) {
      case 'home': headerTitle.innerText = 'Travel English'; break;
      case 'study': headerTitle.innerText = '100일 완성 학습'; break;
      case 'search': headerTitle.innerText = '상황별 긴급 검색'; break;
      case 'stats': headerTitle.innerText = '학습 레포트'; break;
    }
  }

  // 탭별 개별 드로잉
  if (tabName === 'home') drawHome();
  else if (tabName === 'study') drawStudyList();
  else if (tabName === 'search') drawSearch();
  else if (tabName === 'stats') drawStats();
}

// 스피너 토글
function showGlobalSpinner(show) {
  // 바닐라 스피너 구현 (필요시 레이어 팝업)
}

// --- 1. HOME VIEW DRAW ---
function drawHome() {
  if (!globalStats) return;

  // 진척도 정보 바인딩
  document.getElementById('home-completed-days').innerText = globalStats.completed_days;
  document.getElementById('home-total-reviews').innerText = `${globalStats.total_reviews}회`;
  document.getElementById('home-remaining-days').innerText = `${100 - globalStats.completed_days}일`;
  
  // 동그란 프로그레스 링 각도 계산
  const percent = globalStats.completion_rate;
  const progressRing = document.getElementById('home-progress-circle');
  progressRing.style.background = `conic-gradient(var(--accent-blue) ${percent}%, rgba(255,255,255,0.05) 0)`;
  document.getElementById('home-progress-percent').innerText = `${percent}%`;

  // 오늘 학습할 추천 코스 추천
  const todayDay = globalDays.find(d => !d.completed) || globalDays[globalDays.length - 1] || { day_id: 1, title: 'Day 1: 기내 좌석 찾기', theme: '기내 및 공항' };
  document.getElementById('home-recommend-title').innerText = todayDay.title;
  document.getElementById('home-recommend-theme').innerText = todayDay.theme;

  // 추천 카드 클릭 시 해당 Day 학습으로 이동
  const btnStartToday = document.getElementById('btn-start-today');
  btnStartToday.onclick = () => {
    loadDayDetail(todayDay.day_id);
  };

  // 테마별 진행 상태 렌더링
  const themeList = document.getElementById('home-theme-progress-list');
  themeList.innerHTML = '';
  
  // 테마 분할 집계
  const themesData = {};
  globalDays.forEach(d => {
    const mainTheme = d.theme.split(' (')[0];
    if (!themesData[mainTheme]) {
      themesData[mainTheme] = { total: 0, completed: 0 };
    }
    themesData[mainTheme].total += 1;
    if (d.completed) {
      themesData[mainTheme].completed += 1;
    }
  });

  Object.entries(themesData).slice(0, 4).forEach(([name, val], idx) => {
    const rate = Math.round((val.completed / val.total) * 100);
    const accentColors = ['var(--accent-blue)', 'var(--accent-green)', 'var(--accent-purple)', 'var(--accent-blue)'];
    const barColor = accentColors[idx % accentColors.length];

    const card = document.createElement('div');
    card.className = 'glass-card';
    card.style.padding = '12px 16px';
    card.style.display = 'flex';
    card.style.flexDirection = 'column';
    card.style.gap = '6px';
    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; font-size: 13px;">
        <span style="font-weight: 600; color: #eaeaea;">${name}</span>
        <span style="color: var(--text-secondary);">${val.completed}/${val.total}일 (${rate}%)</span>
      </div>
      <div style="height: 6px; background: rgba(255,255,255,0.05); border-radius: 3px; overflow: hidden;">
        <div style="height: 100%; width: ${rate}%; background: ${barColor}; border-radius: 3px; transition: width 0.4s ease-out;"></div>
      </div>
    `;
    themeList.appendChild(card);
  });
}

// --- 2. STUDY VIEW DRAW ---
const themeRanges = [
  { title: "기내 및 공항 (Day 1 - 10)", range: [1, 10] },
  { title: "교통수단 이용 (Day 11 - 20)", range: [11, 20] },
  { title: "호텔 및 숙소 (Day 21 - 30)", range: [21, 30] },
  { title: "식당 및 카페 (Day 31 - 40)", range: [31, 40] },
  { title: "길 찾기 및 위치 (Day 41 - 50)", range: [41, 50] },
  { title: "쇼핑 및 면세점 (Day 51 - 60)", range: [51, 60] },
  { title: "관광 및 매표소 (Day 61 - 70)", range: [61, 70] },
  { title: "문제 및 긴급 상황 (Day 71 - 80)", range: [71, 80] },
  { title: "일상 대화 및 친교 (Day 81 - 90)", range: [81, 90] },
  { title: "귀국 및 면세 신고 (Day 91 - 100)", range: [91, 100] }
];

function drawStudyList() {
  const accordionContainer = document.getElementById('study-accordion-list');
  accordionContainer.innerHTML = '';

  themeRanges.forEach((theme, tIdx) => {
    const isOpen = expandedThemes[tIdx];
    const themeDays = globalDays.filter(d => d.day_id >= theme.range[0] && d.day_id <= theme.range[1]);
    const completedCount = themeDays.filter(d => d.completed).length;

    // 아코디언 헤더
    const header = document.createElement('div');
    header.style.display = 'flex';
    header.style.justifyContent = 'space-between';
    header.style.alignItems = 'center';
    header.style.padding = '14px 16px';
    header.style.background = 'rgba(255,255,255,0.04)';
    header.style.borderRadius = '12px';
    header.style.border = '1px solid rgba(255,255,255,0.05)';
    header.style.cursor = 'pointer';
    
    header.innerHTML = `
      <div>
        <div style="font-size: 13px; font-weight: 700; color: #fff;">${theme.title}</div>
        <div style="font-size: 11px; color: var(--text-secondary); margin-top: 2px;">
          진행도: ${completedCount} / ${themeDays.length} 일 완료
        </div>
      </div>
      <div class="arrow-icon">
        ${isOpen 
          ? `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--text-secondary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>`
          : `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--text-secondary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>`
        }
      </div>
    `;

    header.onclick = () => {
      expandedThemes[tIdx] = !expandedThemes[tIdx];
      drawStudyList(); // 재렌더링
    };

    const wrapper = document.createElement('div');
    wrapper.style.display = 'flex';
    wrapper.style.flexDirection = 'column';
    wrapper.style.gap = '4px';
    wrapper.appendChild(header);

    // 하위 리스트 카드들
    if (isOpen) {
      const daysContainer = document.createElement('div');
      daysContainer.style.display = 'flex';
      daysContainer.style.flexDirection = 'column';
      daysContainer.style.gap = '8px';
      daysContainer.style.padding = '4px 0 10px 8px';

      themeDays.forEach(day => {
        const item = document.createElement('div');
        item.className = 'glass-card';
        item.style.padding = '12px 14px';
        item.style.display = 'flex';
        item.style.justifyContent = 'space-between';
        item.style.alignItems = 'center';
        item.style.cursor = 'pointer';
        
        if (day.completed) {
          item.style.background = 'rgba(52, 199, 89, 0.05)';
          item.style.borderColor = 'rgba(52, 199, 89, 0.15)';
        }

        item.innerHTML = `
          <div style="display: flex; align-items: center; gap: 10px;">
            ${day.completed 
              ? `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--accent-green)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>`
              : `<div style="width: 18px; height: 18px; border-radius: 50%; border: 2px solid var(--text-muted);"></div>`
            }
            <span style="font-size: 13px; font-weight: 700; color: #eaeaea;">${day.title}</span>
          </div>
          <div style="display: flex; align-items: center; gap: 6px;">
            ${day.review_count > 0 
              ? `<span style="font-size: 9px; background: rgba(0,122,255,0.15); color: var(--accent-blue); padding: 2px 6px; border-radius: 8px; font-weight: 700;">${day.review_count}회 복습</span>`
              : ''
            }
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
          </div>
        `;

        item.onclick = () => {
          loadDayDetail(day.day_id);
        };

        daysContainer.appendChild(item);
      });
      wrapper.appendChild(daysContainer);
    }

    accordionContainer.appendChild(wrapper);
  });
}

// 특정 일차 상세 로딩
async function loadDayDetail(dayId) {
  showGlobalSpinner(true);
  try {
    const res = await fetch(`/api/days/${dayId}`);
    if (res.ok) {
      currentDayDetail = await res.json();
      
      // 탭 전환 처리 (홈 탭에서 진입 시 대응)
      currentTab = 'study';
      document.querySelectorAll('.tabbar-item').forEach(btn => {
        if (btn.getAttribute('data-tab') === 'study') {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      });
      renderView('study');
      
      // 아코디언/목록 숨기고 상세 열기
      document.getElementById('study-list-container').style.display = 'none';
      const detailContainer = document.getElementById('study-detail-container');
      detailContainer.style.display = 'flex';
      detailContainer.scrollIntoView({ behavior: 'smooth' });
      
      // 타이틀 및 헤더 설정
      document.getElementById('detail-theme-name').innerText = currentDayDetail.theme;
      document.getElementById('detail-day-title').innerText = `Day ${currentDayDetail.day_id}`;
      
      // 한국어 번역 가리기 상태 동기화
      updateKoreanVisibility();
      
      // 대화창 및 표현 그리기
      drawDetailDialogues();
      drawDetailExpressions();
      updateDetailCompletionCard();
    }
  } catch (error) {
    console.error("Error loading day detail:", error);
  } finally {
    showGlobalSpinner(false);
  }
}

// 한국어 보이기 토글
function updateKoreanVisibility() {
  const eyeBtn = document.getElementById('btn-toggle-korean');
  const eyeIcon = document.getElementById('eye-icon');
  
  if (hideKoreanState) {
    eyeBtn.style.background = 'rgba(0,122,255,0.15)';
    eyeBtn.style.borderColor = 'var(--accent-blue)';
    eyeBtn.style.color = 'var(--accent-blue)';
    eyeIcon.innerHTML = `<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>`;
  } else {
    eyeBtn.style.background = 'rgba(255,255,255,0.06)';
    eyeBtn.style.borderColor = 'var(--border-glass)';
    eyeBtn.style.color = '#fff';
    eyeIcon.innerHTML = `<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>`;
  }
  
  // 말풍선들의 한국어에 hidden 클래스 토글
  document.querySelectorAll('.korean-sub').forEach(sub => {
    if (hideKoreanState) sub.classList.add('hidden');
    else sub.classList.remove('hidden');
  });
}

// 상세 다이얼로그 렌더링
function drawDetailDialogues() {
  const box = document.getElementById('detail-dialogue-box');
  box.innerHTML = '';

  currentDayDetail.dialogues.forEach((dial, idx) => {
    const isEven = idx % 2 === 0;
    const uniqueId = `detail-dial-${dial.id}`;
    
    const row = document.createElement('div');
    row.className = `bubble-row ${isEven ? 'left' : 'right'}`;
    
    row.innerHTML = `
      <span style="font-size: 11px; color: var(--text-secondary); font-weight: 700; ${isEven ? 'margin-left: 8px;' : 'margin-right: 8px;'}">
        ${dial.role}
      </span>
      <div class="bubble-wrapper">
        <div class="bubble-content" id="content-${uniqueId}">
          <p style="font-size: 14px; font-weight: 500; line-height: 1.4;">${dial.english}</p>
          <p class="korean-sub ${hideKoreanState ? 'hidden' : ''}">${dial.korean}</p>
        </div>
        <button class="volume-btn" id="btn-audio-${uniqueId}">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
        </button>
      </div>
    `;

    // 말풍선이나 볼륨버튼 터치 시 음성 재생
    const playAction = () => playTts(dial.english, uniqueId);
    row.querySelector('.bubble-content').onclick = playAction;
    row.querySelector('.volume-btn').onclick = playAction;

    box.appendChild(row);
  });
}

// 상세 핵심 표현 렌더링
function drawDetailExpressions() {
  const box = document.getElementById('detail-expressions-box');
  box.innerHTML = '';

  currentDayDetail.expressions.forEach(exp => {
    const uniqueId = `detail-exp-${exp.id}`;
    const card = document.createElement('div');
    card.className = 'glass-card';
    card.style.display = 'flex';
    card.style.justifyContent = 'space-between';
    card.style.alignItems = 'center';
    card.style.cursor = 'pointer';
    
    card.innerHTML = `
      <div>
        <div style="font-size: 14px; font-weight: 700; color: #fff;" id="eng-text-${uniqueId}">${exp.english}</div>
        <div style="font-size: 12px; color: var(--text-secondary); margin-top: 2px;">${exp.korean}</div>
      </div>
      <div class="volume-btn" id="btn-audio-${uniqueId}" style="color: var(--text-secondary)">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
      </div>
    `;

    card.onclick = () => playTts(exp.english, uniqueId);
    box.appendChild(card);
  });
}

// 학습완료 여부 카드 업데이트
function updateDetailCompletionCard() {
  const statusText = document.getElementById('detail-status-text');
  const reviewCount = document.getElementById('detail-review-count');

  if (currentDayDetail.completed) {
    statusText.innerHTML = `<span style="color: var(--accent-green); font-weight: 700;">학습 완료 🏅</span>`;
  } else {
    statusText.innerText = '미학습';
  }
  reviewCount.innerText = currentDayDetail.review_count;
}

// 학습완료 API 호출 및 Confetti 발동
async function submitCompleteLesson() {
  if (!currentDayDetail) return;
  try {
    const res = await fetch(`/api/days/${currentDayDetail.day_id}/complete`, {
      method: 'POST'
    });
    if (res.ok) {
      triggerConfetti();
      const updated = await res.json();
      
      currentDayDetail.completed = updated.completed;
      currentDayDetail.review_count = updated.review_count;
      
      updateDetailCompletionCard();
      
      // 백그라운드 데이터 갱신
      await fetchGlobalData();
    }
  } catch (error) {
    console.error("Error completing lesson:", error);
  }
}

// Confetti 파티클 애니메이션
function triggerConfetti() {
  const container = document.getElementById('confetti-container');
  container.innerHTML = '';
  const colors = ['#f2d74e', '#95c3de', '#e94a3f', '#3fbf7f', '#af52de', '#007aff'];

  for (let i = 0; i < 40; i++) {
    const size = Math.random() * 8 + 5;
    const left = Math.random() * 100;
    const delay = Math.random() * 1.5;
    const duration = Math.random() * 1.5 + 1.5;
    const color = colors[Math.floor(Math.random() * colors.length)];
    
    const particle = document.createElement('div');
    particle.style.position = 'absolute';
    particle.style.top = '-20px';
    particle.style.left = `${left}%`;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particle.style.backgroundColor = color;
    particle.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
    particle.style.transform = `rotate(${Math.random() * 360}deg)`;
    
    // 키프레임 애니메이션 적용
    particle.style.animation = `fallDown ${duration}s linear ${delay}s infinite`;
    container.appendChild(particle);
  }

  // CSS Fall 애니메이션 삽입
  if (!document.getElementById('confetti-anim-styles')) {
    const styleSheet = document.createElement('style');
    styleSheet.id = 'confetti-anim-styles';
    styleSheet.innerText = `
      @keyframes fallDown {
        0% { top: -20px; transform: translateX(0) rotate(0deg); opacity: 1; }
        100% { top: 100%; transform: translateX(${Math.random() * 80 - 40}px) rotate(720deg); opacity: 0; }
      }
    `;
    document.head.appendChild(styleSheet);
  }
  
  // 2.5초 후 초기화
  setTimeout(() => {
    container.innerHTML = '';
  }, 2500);
}

// --- 3. SEARCH VIEW DRAW ---
const searchTags = ['여권', '식중독', '택시', '체크아웃', '환불', '할인', '화장실', '물건 분실'];

function drawSearch() {
  const tagsBox = document.getElementById('search-popular-tags');
  tagsBox.innerHTML = '';
  
  searchTags.forEach(tag => {
    const btn = document.createElement('button');
    btn.className = 'ripple-btn';
    btn.style.background = 'rgba(255,255,255,0.04)';
    btn.style.border = '1px solid var(--border-glass)';
    btn.style.borderRadius = '10px';
    btn.style.padding = '8px 12px';
    btn.style.fontSize = '12px';
    btn.style.color = 'var(--text-secondary)';
    btn.style.cursor = 'pointer';
    btn.innerText = `#${tag}`;
    
    btn.onclick = () => {
      const input = document.getElementById('search-input-field');
      input.value = tag;
      triggerSearch(tag);
    };
    
    tagsBox.appendChild(btn);
  });
}

let debounceTimer = null;
function handleSearchInput(e) {
  const val = e.target.value;
  
  const clearBtn = document.getElementById('btn-clear-search');
  if (val) clearBtn.style.display = 'block';
  else clearBtn.style.display = 'none';

  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    triggerSearch(val);
  }, 300); // 300ms 디바운스
}

async function triggerSearch(q) {
  const resultsBox = document.getElementById('search-results-box');
  const tagsSection = document.getElementById('search-tag-container');
  
  if (!q.trim()) {
    resultsBox.innerHTML = '';
    tagsSection.style.display = 'block';
    return;
  }
  
  tagsSection.style.display = 'none';
  resultsBox.innerHTML = '<div style="text-align: center; color: var(--text-secondary); font-size: 13px; padding: 20px;">검색 중...</div>';
  
  try {
    const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
    if (res.ok) {
      const data = await res.json();
      renderSearchResults(data);
    }
  } catch (error) {
    console.error("Search error:", error);
    resultsBox.innerHTML = '<div style="text-align: center; color: var(--accent-red); font-size: 13px; padding: 20px;">검색에 실패했습니다.</div>';
  }
}

function renderSearchResults(list) {
  const resultsBox = document.getElementById('search-results-box');
  resultsBox.innerHTML = '';

  const countSpan = document.createElement('span');
  countSpan.style.fontSize = '12px';
  countSpan.style.color = 'var(--text-secondary)';
  countSpan.innerText = `검색 결과 ${list.length}건`;
  resultsBox.appendChild(countSpan);

  if (list.length === 0) {
    const noResult = document.createElement('div');
    noResult.style.textAlign = 'center';
    noResult.style.padding = '40px 20px';
    noResult.style.display = 'flex';
    noResult.style.flexDirection = 'column';
    noResult.style.alignItems = 'center';
    noResult.style.gap = '12px';
    noResult.style.color = 'var(--text-secondary)';
    noResult.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
      <div>
        <div style="font-size: 14px; font-weight: 700; color: #fff;">일치하는 표현이 없습니다</div>
        <div style="font-size: 12px; margin-top: 4px;">다른 단어로 다시 검색해보세요.</div>
      </div>
    `;
    resultsBox.appendChild(noResult);
    return;
  }

  list.forEach((item, idx) => {
    const uniqueId = `search-${item.source}-${idx}`;
    const isEmergency = item.source === 'emergency';

    const card = document.createElement('div');
    card.className = 'glass-card';
    card.id = `card-${uniqueId}`;
    card.style.cursor = 'pointer';
    card.style.display = 'flex';
    card.style.flexDirection = 'column';
    card.style.gap = '8px';
    
    if (isEmergency) {
      card.style.background = 'rgba(255, 59, 48, 0.06)';
      card.style.borderColor = 'rgba(255, 59, 48, 0.2)';
    }

    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 10px; font-weight: 700; text-transform: uppercase; padding: 2px 6px; border-radius: 6px; background: ${isEmergency ? 'rgba(255,59,48,0.15)' : 'rgba(255,255,255,0.06)'}; color: ${isEmergency ? '#ff3b30' : 'var(--text-secondary)'}">
          ${isEmergency ? '긴급 상황' : item.source === 'dialogue' ? '대화' : '핵심 표현'}
        </span>
        <span style="font-size: 11px; color: var(--text-secondary);">${item.context || ''}</span>
      </div>
      <div>
        <h3 style="font-size: 16px; font-weight: 700; color: #fff; line-height: 1.4;">${item.english}</h3>
        <p style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;">${item.korean}</p>
      </div>
      <div style="display: flex; justify-content: flex-end; border-top: 1px solid rgba(255,255,255,0.03); padding-top: 8px; margin-top: 4px;">
        <span style="display: flex; align-items: center; gap: 4px; font-size: 11px; color: var(--text-secondary);" id="audio-lbl-${uniqueId}">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
          터치하여 발음 듣기
        </span>
      </div>
    `;

    card.onclick = () => playTts(item.english, uniqueId);
    resultsBox.appendChild(card);
  });
}

// --- 4. STATS VIEW DRAW ---
function drawStats() {
  if (!globalStats) return;

  // 카드 랭크 판단
  const completed = globalStats.completed_days;
  let rankTitle = '새내기 여행자';
  let rankColor = '#8e8e93';
  let rankDesc = '100일 챌린지의 첫 걸음을 떼셨습니다. 계속 전진하세요!';
  
  if (completed >= 100) {
    rankTitle = '세계 여행 전문가'; rankColor = '#ffb300'; rankDesc = '영어 장벽 없이 세계 어디나 갈 수 있습니다!';
  } else if (completed >= 80) {
    rankTitle = '프로 배낭러'; rankColor = '#af52de'; rankDesc = '여행지에서의 웬만한 상황은 혼자 해결할 수 있습니다!';
  } else if (completed >= 50) {
    rankTitle = '중급 여행자'; rankColor = '#007aff'; rankDesc = '중요한 요구사항을 당당하게 말할 수 있습니다!';
  } else if (completed >= 20) {
    rankTitle = '초보 모험가'; rankColor = '#34c759'; rankDesc = '기본적인 생존 영어는 준비가 끝났습니다!';
  }

  // 랭킹 카드 반영
  document.getElementById('stats-rank-title').innerText = rankTitle;
  document.getElementById('stats-rank-title').style.color = rankColor;
  document.getElementById('stats-rank-desc').innerText = rankDesc;
  document.getElementById('stats-rank-icon').style.color = rankColor;

  // 통계 수치 바인딩
  document.getElementById('stats-completed-days').innerText = `${completed}일`;
  document.getElementById('stats-completion-percent').innerText = `전체 대비 ${globalStats.completion_rate}% 달성`;
  document.getElementById('stats-total-reviews').innerText = `${globalStats.total_reviews}회`;
  
  const avg = completed > 0 ? Math.round((globalStats.total_reviews / completed) * 10) / 10 : 0;
  document.getElementById('stats-average-reviews').innerText = `일 평균 ${avg}회 복습`;

  // 최근 완료 내역 매핑
  const recentList = document.getElementById('stats-recent-list');
  recentList.innerHTML = '';

  if (globalStats.recent_activity && globalStats.recent_activity.length > 0) {
    globalStats.recent_activity.forEach(item => {
      const card = document.createElement('div');
      card.className = 'glass-card';
      card.style.display = 'flex';
      card.style.justifyContent = 'space-between';
      card.style.alignItems = 'center';
      card.style.padding = '12px 16px';
      card.style.background = 'rgba(255,255,255,0.02)';
      
      const dateText = formatDate(item.last_completed_at);

      card.innerHTML = `
        <div>
          <div style="font-size: 13px; font-weight: 700; color: #fff;">${item.title}</div>
          <div style="font-size: 11px; color: var(--text-secondary); margin-top: 2px;">${item.theme}</div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 10px; color: var(--accent-green); font-weight: 700;">${item.review_count}회 학습완료</div>
          <div style="font-size: 9px; color: var(--text-secondary); margin-top: 3px;">${dateText}</div>
        </div>
      `;
      recentList.appendChild(card);
    });
  } else {
    recentList.innerHTML = `<div class="glass-card" style="padding:30px; text-align:center; color:var(--text-secondary); font-size:13px;">아직 완료한 학습 기록이 없습니다.</div>`;
  }
}

// 날짜 포맷 헬퍼
function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hour = String(d.getHours()).padStart(2, '0');
  const min = String(d.getMinutes()).padStart(2, '0');
  return `${year}-${month}-${day} ${hour}:${min}`;
}

// 전체 통계 리셋 API 호출
async function resetStatsData() {
  const confirm = window.confirm("정말 모든 학습 데이터를 초기화하시겠습니까?\n이 작업은 되돌릴 수 없으며, 모든 일일 완료 여부와 반복 복습 횟수가 0으로 리셋됩니다.");
  if (!confirm) return;

  try {
    const res = await fetch('/api/reset', { method: 'POST' });
    if (res.ok) {
      alert("모든 학습 데이터가 초기화되었습니다.");
      
      // 홈 탭으로 강제 이동하고 데이터 갱신
      const homeTabButton = document.querySelector('.tabbar-item[data-tab="home"]');
      if (homeTabButton) homeTabButton.click();
    }
  } catch (error) {
    console.error("Reset failed:", error);
  }
}

// --- 5. WEB SPEECH API (TTS) ENGINE ---
function playTts(text, id) {
  if (!('speechSynthesis' in window)) {
    alert("이 브라우저는 음성 합성(TTS)을 지원하지 않습니다.");
    return;
  }

  // 이미 실행 중인 음성이 있으면 취소
  window.speechSynthesis.cancel();

  // 이전 재생 중 상태 지우기
  clearPlayingTtsStyle();

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'en-US';
  utterance.rate = 0.9; // 살짝 편안한 속도

  utterance.onstart = () => {
    playingTtsId = id;
    setPlayingTtsStyle(id, true);
  };
  
  utterance.onend = () => {
    setPlayingTtsStyle(id, false);
    playingTtsId = null;
  };

  utterance.onerror = () => {
    setPlayingTtsStyle(id, false);
    playingTtsId = null;
  };

  window.speechSynthesis.speak(utterance);
}

// 오디오 재생 중 상태 UI 효과 클래스 토글
function setPlayingTtsStyle(id, isPlaying) {
  // 다이얼로그 말풍선용 스타일 처리
  const bubble = document.getElementById(`content-${id}`);
  const audioBtn = document.getElementById(`btn-audio-${id}`);
  
  if (bubble) {
    if (isPlaying) bubble.classList.add('playing');
    else bubble.classList.remove('playing');
  }
  
  if (audioBtn) {
    if (isPlaying) audioBtn.classList.add('playing');
    else audioBtn.classList.remove('playing');
  }

  // 검색 탭용 라벨 텍스트 스타일 변경
  const searchCard = document.getElementById(`card-${id}`);
  const searchLabel = document.getElementById(`audio-lbl-${id}`);
  if (searchCard && isPlaying) {
    searchCard.style.boxShadow = '0 0 10px rgba(0, 122, 255, 0.2)';
    if (searchLabel) {
      searchLabel.style.color = 'var(--accent-blue)';
      searchLabel.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="playing"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg> 발음 듣는 중...`;
    }
  } else if (searchCard && !isPlaying) {
    searchCard.style.boxShadow = 'none';
    if (searchLabel) {
      searchLabel.style.color = 'var(--text-secondary)';
      searchLabel.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg> 터치하여 발음 듣기`;
    }
  }
}

// 모든 재생 중 UI 스타일 리셋
function clearPlayingTtsStyle() {
  if (playingTtsId) {
    setPlayingTtsStyle(playingTtsId, false);
  }
}

// --- 6. EVENT LISTENERS SETUP ---
function setupEventListeners() {
  // A. Study 상세 백버튼
  document.getElementById('btn-back-to-list').onclick = () => {
    document.getElementById('study-list-container').style.display = 'flex';
    document.getElementById('study-detail-container').style.display = 'none';
    window.speechSynthesis.cancel();
    clearPlayingTtsStyle();
    fetchGlobalData().then(() => drawStudyList()); // 복습 횟수 갱신용 로드
  };

  // B. Study 상세 한국어 토글 버튼
  document.getElementById('btn-toggle-korean').onclick = () => {
    hideKoreanState = !hideKoreanState;
    updateKoreanVisibility();
  };

  // C. Study 상세 완료 버튼
  document.getElementById('btn-complete-lesson').onclick = () => {
    submitCompleteLesson();
  };

  // D. Search 실시간 타이핑 인풋
  const searchInput = document.getElementById('search-input-field');
  searchInput.addEventListener('input', handleSearchInput);

  // E. Search 클리어 버튼
  document.getElementById('btn-clear-search').onclick = () => {
    searchInput.value = '';
    triggerSearch('');
    document.getElementById('btn-clear-search').style.display = 'none';
  };

  // F. Stats 데이터 초기화 버튼
  document.getElementById('btn-reset-data').onclick = () => {
    resetStatsData();
  };
}
