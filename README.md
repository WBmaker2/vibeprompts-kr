# VibePrompt KR (바이브프롬프트 한국어판)

> **바이브 코더(Vibe Coders)를 위한 한국어 UI 레이아웃 프롬프트 & Tailwind CSS 스니펫 라이브러리**  
> 원본 사이트: [https://vibeprompts.dev/](https://vibeprompts.dev/) 분석 및 한국어 클론 프로젝트

---

## 🌟 프로젝트 소개
**VibePrompt KR**은 현대적인 웹 개발과 생성형 AI 코딩(Claude, Cursor, v0, Bolt 등) 환경에 맞춰 엄선된 **15개 카테고리, 286개 UI 레이아웃 프롬프트**를 전수 한국어로 번역하고, 인터랙티브 실시간 미리보기 및 원클릭 복사 기능을 제공하는 웹 애플리케이션입니다.

---

## ✨ 주요 기능
1. **286개 UI 레이아웃 프롬프트 & Tailwind 코드 수집 및 한국어 현지화**
   - 인증 폼(Auth), 요금제(Pricing), 벤토/기능(Features), 히어로(Hero), CTA 배너, 통계 바(Stats), 내비게이션(Nav), 추천사(Testimonials), 푸터(Footer), FAQ, 대시보드(Dashboards), 온보딩(Onboarding), 블로그(Blog), 문의하기(Contact), 보너스(Bonus) 등 총 15개 카테고리.
   - 모든 제목, 설명, AI 프롬프트가 자연스럽고 전문적인 한국어로 번역되었습니다.
2. **실시간 검색 & 카테고리 필터링**
   - 한글/영문 실시간 통합 검색 지원 (단축키 `/`로 검색창 바로 포커스).
   - 카테고리별 원클릭 필터링 및 카운트 실시간 업데이트.
3. **인터랙티브 컴포넌트 뷰어 모달**
   - **실시간 반응형 미리보기**: 전체 화면(Full), 태블릿(Tablet 768px), 모바일(Mobile 375px) 크기 실시간 전환.
   - **3단 탭 뷰**: `한국어 프롬프트`, `영문 원본 프롬프트`, `Tailwind HTML 코드` 탭 분리 제공.
   - **원클릭 클립보드 복사**: 클릭 한 번으로 프롬프트나 코드를 복사하고 피드백 토스트 알림 표시.
4. **해시 기반 딥링킹(Deep Linking)**
   - URL 해시(예: `#auth-split-screen-with-visual`)를 지원하여 특정 프롬프트 공유 및 북마크가 가능합니다.
5. **독립적이고 빠른 정적 사이트 구조**
   - 286개 미리보기 이미지와 자산이 모두 로컬에 번들링되어 오프라인 및 GitHub Pages 환경에서 즉시 로드됩니다.

---

## 🚀 로컬 실행 방법
별도의 빌드 도구 없이 브라우저에서 바로 실행하거나, 로컬 웹 서버로 확인할 수 있습니다.

```bash
# Python 내장 서버로 실행
python3 -m http.server 8000

# 브라우저에서 접속
http://localhost:8000
```

---

## 📦 프로젝트 구조
```
vibeprompts-dev-clone/
├── index.html         # 전체 카드 프리렌더링 및 모달 뷰어가 포함된 메인 페이지
├── css/
│   └── app.css        # 원본 레이아웃 스타일 및 한국어 타이포그래피(Pretendard) 최적화
├── js/
│   └── app.js         # 실시간 검색, 카테고리 필터, 모달 뷰어, 클립보드 복사 로직
├── data/
│   └── prompts.json   # 286개 프롬프트 전수 한국어/영문/코드 통합 데이터셋
├── previews/          # 286개 컴포넌트 미리보기 고화질 이미지 (.avif)
├── favicon.svg        # 파비콘 아이콘
├── og.png             # 오픈그래프(OG) 썸네일 이미지
└── README.md          # 프로젝트 안내 문서
```

---

## 📄 라이선스
원작자 디자인 영감 및 원본 사이트 [VibePrompt](https://vibeprompts.dev/)의 구성에 기반하며, 코드는 MIT 라이선스를 따릅니다.
