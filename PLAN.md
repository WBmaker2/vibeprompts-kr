# VibePrompt KR 단계별 개선 및 고도화 구현 계획서

본 문서는 **VibePrompt KR** 프로젝트의 데이터 결함 해결, 286개 프롬프트 전수 자연스러운 한국어 현지화, 그리고 바이브 코더를 위한 핵심 생산성 기능 추가를 **3단계(Phase 1 → Phase 2 → Phase 3)**로 나누어 순차적으로 구현하기 위한 실행 계획입니다.

---

## 📋 전체 로드맵 요약

1. **1단계: 버그 픽스 & 데이터 정제 (Foundation & Bug Fixes)**
   - Cloudflare 이메일 난독화 마크업 오염 복구 (51개 항목)
   - 인터랙티브 JS 분리 및 `data/prompts.json` 용량 최적화 (`3.75MB` → `~1.1MB`)
   - 라이브 프리뷰 JS 실행 정상화(143개 항목) 및 `iframe` 자동 높이 조절 연동
   - 모달 브레드크럼 새로고침 버그 수정, 미사용 에셋(`domi.jpg`) 정리 및 단일 소스 빌드 스크립트(`scripts/build.py`) 구축
2. **2단계: 286개 프롬프트 완벽 한글화 (Full Korean Localization)**
   - 미번역 제목(`titleKo`, 85개) 및 설명(`descKo`, 187개) 전수 자연스러운 한국어 번역
   - 한영 혼용 프롬프트 본문(`promptKo`, 248개) 전면 고품질 재번역 (Tailwind 클래스 및 핵심 스펙 보존)
   - `index.html` 카드 그리드 및 검색 인덱스(`data-search`) 100% 동기화
3. **3단계: 신규 UX 및 바이브 코딩 특화 기능 추가 (Feature Evolution)**
   - 카드 퀵 복사 버튼 & 모달 내 이전/다음 컴포넌트 탐색(`←`/`→` 방향키 및 버튼)
   - 프롬프트 옵션 빌더 (React/Next.js/Vue 변환, 한국어 더미 텍스트 생성 지시, 다크 모드 지시어 자동 조합)
   - `localStorage` 기반 즐겨찾기(`★`) 및 다중 섹션 조합 '랜딩페이지 프롬프트 장바구니' 구현

---

## 🛠️ 1단계: 버그 픽스 & 데이터 정제 (Foundation & Bug Fixes)

### 1.1 Cloudflare 이메일 난독화 마크업 복구 (51개 항목)
- **대상 파일**: `data/prompts.json`
- **현상**: `code` 필드 내 51개 스니펫에 `<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="...">[email protected]</a>`가 삽입되어 `<input placeholder="...">` 등의 HTML 속성이 깨짐.
- **구현 방법**:
  - 동일 항목의 `srcdoc` 필드에는 원본 이메일(`you@example.com`, `sam@northwind.co` 등)이 정상 보존되어 있음.
  - 정제 스크립트를 작성하여 `srcdoc`의 `<body>` 내부 마크업에서 정상 이메일 텍스트를 추출해 `code` 필드의 오염 구간을 100% 원상 복구.

### 1.2 인터랙티브 JS 추출 및 JSON 용량 최적화 (`3.75MB` → `~1.1MB`)
- **대상 파일**: `data/prompts.json`
- **현상**: 전체 286개 중 **143개 스니펫**의 `srcdoc`에 실제 동작하는 `<script>`(OTP 입력 제어, 비밀번호 강도 체크, 탭 전환, 계산기 등)가 들어있으나, `code`와 중복된 HTML 때문에 파일 용량이 3.75MB에 달함.
- **구현 방법**:
  - `srcdoc`에서 공통 리사이즈 스크립트(`vp-height`)를 제외한 **컴포넌트 고유 인터랙티브 스크립트**를 추출하여 각 항목의 `script` 필드로 분리 저장.
  - 중복된 `srcdoc` 필드를 제거하고 런타임(`js/app.js`)에서 `code` + `script`를 결합하도록 구조를 개선하여 초기 JSON 로드 크기를 약 70% 절감.

### 1.3 라이브 프리뷰 정상화 및 iframe 자동 높이 조절 연동
- **대상 파일**: `js/app.js`, `index.html`
- **구현 방법**:
  - `openModal()`에서 `modalPreviewFrame.srcdoc` 생성 시 `item.script`와 `ResizeObserver` 높이 알림 스크립트(`parent.postMessage({ type: "vp-height", height }, "*")`)를 함께 주입.
  - `js/app.js`에 `window.addEventListener("message", ...)` 리스너를 추가해 컴포넌트 실제 렌더링 높이에 맞춰 iframe 높이가 자연스럽게 조절되도록 수정.
  - `script`가 존재하는 143개 컴포넌트의 경우, 코드 탭에서 **HTML + JS 전체 코드**를 확인 및 복사할 수 있도록 지원.

### 1.4 UI 버그 수정 및 빌드 스크립트(`scripts/build.py`) 구성
- **대상 파일**: `index.html`, `scripts/build.py` (신규), `domi.jpg` (삭제)
- **구현 방법**:
  - 모달 내부 브레드크럼의 `<a href="./">‹ 라이브러리</a>` 클릭 시 페이지가 새로고침되는 현상을 방지하고 모달이 닫히도록 `data-close` 처리.
  - 미사용 이미지 파일 `domi.jpg` 제거.
  - `data/prompts.json` 데이터가 변경되면 `index.html`의 카드 그리드 영역(`#grid`)과 카테고리별 카운트를 자동으로 리빌드하는 `scripts/build.py` 작성.

---

## 🇰🇷 2단계: 286개 프롬프트 완벽 한글화 (Full Korean Localization)

### 2.1 미번역 제목(`titleKo`) 85개 및 설명(`descKo`) 187개 전수 번역
- **대상 현황**:
  - 제목 미번역 85개 (예: `Fluid type scale calculator` → `유동적 타이포그래피 스케일 계산기`, `Choose-your-path field guide` → `독자 맞춤형 경로 선택 가이드`)
  - 설명 미번역/부분 번역 187개 (예: `Generate 반응형 clamp values with a live hierarchy` → `실시간 계층 구조 미리보기로 반응형 clamp() 값을 생성하는 계산기`)
- **구현 방법**:
  - 15개 카테고리 문맥에 맞춰 286개 전체 항목의 `titleKo`, `descKo`를 검수 및 자연스러운 한국어로 완성.

### 2.2 한영 혼용 프롬프트 본문(`promptKo`) 248개 고품질 재번역
- **대상 현황**:
  - 현재 `"제작하세요: 가운데 정렬된 sign-up 카드 Tailwind CSS를 사용하여 on a soft neutral background..."` 형태로 영문 문장 중간에 한글 단어만 끼워 넣은 248개 항목.
- **번역 원칙**:
  1. **완전한 한국어 문장 구조**: AI에게 지시하는 명확하고 자연스러운 한국어 프롬프트 문체(`"Tailwind CSS를 사용하여 부드러운 중립 톤 배경 위에 중앙 정렬된 회원가입 카드를 제작하세요..."`)로 재작성.
  2. **핵심 스펙 및 Tailwind 클래스 보존**: `max-w-sm`, `rounded-xl`, `size-12`, `data-rule` 등 코드 구조와 직결되는 기술 용어는 원문 그대로 병기하여 Claude, Cursor, v0 등에 입력했을 때 원본과 동일한 수준의 결과물이 나오도록 보장.
  3. **인터랙티브 동작 명세 한글화**: 143개 인터랙티브 스니펫에 포함된 JavaScript 동작 요구사항(`Then add JavaScript that...`)도 누락 없이 명확한 한국어로 번역.

### 2.3 `index.html` 프리렌더링 및 검색 인덱스(`data-search`) 재생성
- `scripts/build.py`를 실행하여 새로 번역된 `titleKo`, `descKo`, `promptKo`를 `index.html`의 286개 카드 DOM과 `data-search` 속성에 일괄 반영.

---

## 🚀 3단계: 신규 UX 및 바이브 코딩 특화 기능 추가 (Feature Evolution)

### 3.1 카드 퀵 복사 버튼 & 모달 키보드 내비게이션
- **카드 퀵 액션 (Quick Copy)**:
  - 메인 그리드의 각 카드 푸터에 모달을 열지 않고도 즉시 클릭할 수 있는 **`프롬프트 복사`** 버튼 추가.
- **모달 내 이전/다음 탐색 (`←` / `→`)**:
  - 모달 헤더에 `[‹ 이전]` / `[다음 ›]` 버튼을 배치하고, 키보드 좌우 화살표(`ArrowLeft`, `ArrowRight`) 입력 시 현재 활성화된 카테고리/검색 결과 목록 내에서 즉시 이전·다음 컴포넌트로 전환.

### 3.2 프롬프트 옵션 빌더 (Vibe Prompt Customizer)
모달의 프롬프트 탭 상단에 **원클릭 프롬프트 보강 옵션 바**를 추가하여, 선택된 옵션에 따라 프롬프트 하단에 맞춤형 지시문이 실시간으로 조합·복사되도록 구현합니다.
- **프레임워크 선택**: `기본 (Tailwind HTML)` | `React + TypeScript` | `Next.js (App Router)` | `Vue 3 (SFC)`
- **추가 지시어 토글**:
  - `🇰🇷 한국어 UI 텍스트로 생성`: *"컴포넌트 내 모든 제목, 버튼, 안내 문구, 플레이스홀더를 자연스러운 한국어로 작성하세요."* 자동 추가
  - `🌙 다크 모드 포함`: *"Tailwind의 `dark:` 프리픽스를 활용해 라이트/다크 모드를 모두 지원하도록 작성하세요."* 자동 추가
- **프리뷰 한국어 폰트 토글**: 라이브 프리뷰 iframe 내부에도 `Pretendard` 폰트를 적용해 볼 수 있는 스위치 제공.

### 3.3 즐겨찾기(`★`) 및 랜딩페이지 프롬프트 장바구니 (Prompt Cart)
- **즐겨찾기 (Bookmarks)**:
  - 각 카드 및 모달에 `★` 북마크 토글 버튼을 추가하고 `localStorage`에 저장.
  - 사이드바 상단에 **`★ 즐겨찾기`** 필터 메뉴를 추가하여 자주 쓰는 스니펫만 모아보기 지원.
- **프롬프트 장바구니 (Multi-Section Prompt Builder)**:
  - 원하는 섹션 여러 개(예: `내비게이션 바` + `히어로 섹션` + `벤토 그리드` + `요금제` + `푸터`)를 담으면 화면 하단 플로팅 바가 활성화됨.
  - **`[통합 프롬프트 복사]`** 클릭 시, 선택된 섹션들의 프롬프트를 순서대로 묶어 전체 랜딩페이지 제작 마스터 프롬프트로 한 번에 복사하거나 `.md` 파일로 다운로드하는 기능 제공.

---

## ✅ 단계별 검증 계획 (Verification Plan)

| 단계 | 검증 항목 | 검증 방법 |
| :--- | :--- | :--- |
| **1단계** | Cloudflare 오염 0건, 143개 JS 동작, iframe 리사이징 | 스크립트로 JSON 무결성 검사 + 브라우저에서 OTP/비밀번호 강도/계산기 프리뷰 실제 동작 확인 |
| **2단계** | 미번역(`titleKo == titleEn`, `descKo == descEn`) 0건, 한영혼용 정규식 패턴 0건 | Python 검증 스크립트로 286개 전수 스캔 및 한글 키워드 검색 테스트 |
| **3단계** | 퀵 복사, `←`/`→` 전환, 프롬프트 빌더, 즐겨찾기/장바구니 | 데스크톱 및 모바일 뷰포트에서 UI 인터랙션, 클립보드 복사 결과물, `localStorage` 유지 여부 확인 |
