import json
import re

# Curated high-quality Korean titles and descriptions
CURATED_TRANSLATIONS = {
    # Remaining 23 titles
    "contact-demo-booking-with-time-slots": ("시간대 선택 제품 데모 예약 폼", "날짜와 시간을 선택하고 즉시 확정하는 인터랙티브 예약 캘린더"),
    "contact-support-chat-widget": ("실시간 고객 지원 채팅 위젯", "상용구 답변 스레드와 상담원 연결을 지원하는 플로팅 챗봇"),
    "contact-feedback-rating-widget": ("만족도 평가 및 피드백 위젯", "별점/점수를 먼저 선택하면 상세 의견 작성란이 나타나는 위젯"),
    "auth-recovery-code-sign-in": ("비상 복구 코드로 로그인", "인증기 분실 시 1회성 백업 코드로 긴급 접근하는 로그인 폼"),
    "auth-dual-email-change-verification": ("이메일 변경 양방향 인증 확인", "기존 이메일과 새 이메일 양쪽 수신함에서 모두 승인하는 보안 인증"),
    "pricing-reserved-capacity-planner": ("예약 용량 플래너 및 요금 계산기", "종량제 유연 요금과 사전 약정 용량 할인을 비교하는 계산기"),
    "pricing-outcome-based-fee-simulator": ("성과 기반 수수료 시뮬레이터", "기본 요금에 실적 성과 인센티브를 조합하여 예측하는 모델러"),
    "features-permission-inheritance-explorer": ("권한 상속 탐색기 및 시각화", "조직 레벨부터 개별 리소스까지 권한 흐름을 추적하는 인터페이스"),
    "features-offline-sync-journey": ("오프라인 로컬 우선 동기화 안내", "네트워크 단절 시 로컬 저장 및 재연결 동기화 여정을 보여주는 다이어그램"),
    "hero-live-collaboration-canvas-hero": ("실시간 동시 협업 캔버스 히어로", "팀원들의 움직이는 라이브 커서와 캔버스를 인터랙티브하게 보여주는 히어로"),
    "hero-voice-note-product-hero": ("음성 메모 녹음 제품 히어로", "직관적인 오디오 파형과 터치식 레코더 데모가 돋보이는 히어로 섹션"),
    "cta-seat-limit-collaboration-nudge": ("워크스페이스 멤버 한도 알림 CTA", "팀원이 가득 찼을 때 상위 플랜 확장을 제안하는 상황별 넛지 배너"),
    "cta-maintenance-window-opt-in": ("정기 점검 및 유지보수 시간대 선택", "서비스 무중단 배포를 위해 안전한 점검 시간대를 지정하는 배너"),
    "stats-anomaly-pulse-strip": ("이상 징후 감지 펄스 스트립", "서버나 데이터의 이상 패턴 발생 시 맥락과 함께 즉각 경보를 띄우는 바"),
    "stats-contribution-rhythm-calendar": ("활동 기여도 히트맵 캘린더", "깃허브 스타일의 잔디 심기 잔여 연속 기록과 기여 리듬 통계"),
    "nav-presence-aware-collaboration-nav": ("접속자 상태 표시 협업 내비게이션 바", "현재 문서나 워크스페이스에 함께 접속 중인 팀원 아바타가 표시되는 헤더"),
    "nav-multi-product-launcher-nav": ("멀티 프로덕트 런처 내비게이션 바", "구글 앱 런처 스타일로 여러 패밀리 제품군을 빠르게 오가는 내비게이션"),
    "footer-command-line-product-footer": ("CLI 터미널 스타일 개발자 푸터", "유용한 터미널 세션 인터페이스 형태로 꾸며진 엔지니어링 푸터"),
    "footer-carbon-aware-service-footer": ("친환경 탄소 발자국 투명 푸터", "인프라 전력 소모량과 친환경 리전 선택 내역을 투명하게 공개하는 푸터"),
    "faq-inline-definition-faq": ("용어 인라인 정의 사전형 FAQ", "전문 용어 위에 마우스를 올리면 툴팁으로 해설을 제공하는 FAQ"),
    "faq-release-specific-answer-finder": ("버전별 맞춤 답변 검색 FAQ", "소프트웨어 버전별 변경점 및 호환성 차이를 반영하는 스마트 FAQ"),
    "dashboards-query-performance-workbench": ("SQL 쿼리 성능 분석 워크벤치", "느린 데이터베이스 쿼리의 실행 계획과 병목을 한눈에 진단하는 대시보드"),
    "dashboards-inventory-replenishment-cockpit": ("재고 보충 및 발주 관리 콕핏", "재고 소진 위험 품목을 감지하고 우선순위 발주를 돕는 관리 뷰"),

    # Remaining 94 descriptions
    "cta-free-shipping-progress-bar": ("무료 배송 달성 진행률 게이지 바", "장바구니 금액이 무료 배송 기준에 얼마나 근접했는지 보여주는 바"),
    "stats-four-metric-row": ("4열 대형 수치 지표 바", "시원한 대형 폰트의 숫자와 설명 레이블로 구성된 4열 통계"),
    "stats-stats-on-dark-card": ("다크 카드 패널 통계", "어두운 패널 안에 3개의 핵심 성장 지표를 강조한 카드"),
    "stats-metric-cards-with-sparkline-bars": ("스파크라인 차트 포함 KPI 타일", "순수 CSS 트렌드 바 차트가 함께 렌더링되는 KPI 지표 카드"),
    "stats-goal-progress-bars": ("목표 달성률 진행 바", "목표치와 현재 달성 퍼센티지(%)를 게이지로 보여주는 위젯"),
    "stats-uptime-status-strip": ("서비스 가동률(Uptime) 상태 스트립", "서비스별 과거 히스토리 바와 실시간 요약 정보를 보여주는 상태 바"),
    "stats-count-up-metrics-on-view": ("스크롤 시 카운트업 애니메이션 지표", "화면에 진입할 때 0부터 목표 수치까지 부드럽게 숫자가 올라가는 인터랙션"),
    "stats-ring-gauge-trio": ("링 도넛 차트 3종 세트", "중앙에 수치가 표시되는 3개의 원형 도넛 SVG 게이지"),
    "stats-conversion-funnel-steps": ("전환 퍼널(Funnel) 단계 분석", "단계별 이탈률과 전환 수치를 깔끔하게 시각화한 퍼널 바"),
    "stats-week-over-week-delta-table": ("주간 전주 대비(WoW) 증감표", "전주 대비 상승/하락(+/-) 기호가 명확히 표기된 컴팩트 지표 표"),
    "stats-live-counter-ticker": ("실시간 라이브 티커 카운터", "페이지를 보고 있는 동안에도 숫자가 실시간으로 갱신되는 카운터"),
    "stats-leaderboard-with-rank-movement": ("순위 변동 표시 리더보드", "현재 등수, 점수 및 상승/하락 순위 변동 아이콘이 표시되는 순위표"),
    "stats-benchmark-against-industry": ("업계 평균 대비 벤치마크 비교", "내 서비스 지표를 업계 중간값(Median) 및 상위 10%와 나란히 비교"),
    "stats-poll-results-breakdown": ("설문조사 투표 결과 요약", "문항별 득표율, 투표수 및 총 참여자 수가 표시되는 결과 차트"),
    "stats-sustainability-impact-panel": ("ESG 친환경 지속가능성 지표 패널", "탄소 배출 절감량, 재생 에너지 사용률을 수치로 정리한 패널"),
    "stats-milestone-counters-timeline": ("기업 성장 마일스톤 연혁 카운터", "연도별 역사와 당시 달성한 누적 수치를 함께 보여주는 타임라인"),

    "nav-sticky-top-nav": ("상단 고정형 기본 내비게이션 바", "로고, 카테고리 링크 및 시작하기 버튼으로 구성된 표준 상단 바"),
    "nav-nav-with-mega-dropdown": ("메가 드롭다운 포함 내비게이션 바", "마우스 호버 시 주제별 링크 그룹이 시원하게 펼쳐지는 드롭다운"),
    "nav-floating-pill-nav": ("플로팅 필(Pill) 캡슐 내비게이션 바", "페이지 상단에 부유하는 둥근 알약 모양의 미니멀 헤더"),
    "nav-app-bar-with-search-and-tabs": ("검색창 및 탭 결합 앱 헤더 바", "글로벌 검색창과 서브 섹션 탭이 일체형으로 디자인된 헤더"),
    "nav-collapsible-sidebar-nav": ("접이식 사이드바 내비게이션", "아이콘 모드로 깔끔하게 축소되는 그룹형 수직 메뉴"),
    "nav-nav-with-announcement-bar": ("공지사항 배너 포함 내비게이션 바", "헤더 상단에 닫기 가능한 중요 프로모션 공지 스트립을 얹은 내비게이션"),
    "nav-sliding-underline-tabs": ("슬라이딩 언더라인 탭 내비게이션", "선택된 탭 아래로 밑줄 표시기가 부드럽게 미끄러지듯 이동하는 탭"),
    "nav-shrink-on-scroll-nav": ("스크롤 시 축소되는 스마트 내비게이션", "스크롤을 내리면 높이가 줄어들며 화면 공간을 넓혀주는 헤더"),
    "nav-shop-nav-with-cart-badge": ("장바구니 배지 포함 이커머스 내비게이션", "카테고리 행, 상품 검색창 및 장바구니 수량 배지가 결합된 쇼핑몰 헤더"),
    "nav-breadcrumb-page-header": ("브레드크럼(경로) 결합 페이지 헤더", "현재 위치 경로, 페이지 타이틀 및 주요 액션 버튼이 모인 상단 바"),
    "nav-nav-with-currency-and-language": ("통화 및 언어 선택 포함 글로벌 바", "해외 고객을 위한 다국어/통화 변환 드롭다운이 내장된 헤더"),
    "nav-anchor-nav-with-scroll-spy": ("스크롤 스파이 지원 앵커 내비게이션", "스크롤 위치에 따라 현재 읽고 있는 섹션 링크가 자동으로 하이라이트"),

    "testimonials-logo-wall-quote": ("고객사 로고 월과 추천사 하이라이트", "대표적인 고객사 로고 행과 함께 인상적인 핵심 후기를 강조"),
    "testimonials-masonry-quote-wall": ("비정형 메이슨리 후기 모음 월", "길이가 다양한 고객 후기 카드를 벽돌 쌓기 형태로 자연스럽게 배열"),
    "testimonials-rating-summary-with-reviews": ("평점 종합과 최근 리뷰 피드", "종합 별점 통계 옆에 최신 고객 평가 피드가 나란히 배치된 레이아웃"),
    "testimonials-video-story-cards": ("동영상 고객 인터뷰 스토리 카드", "재생 버튼이 있는 썸네일과 핵심 인용구가 어우러진 비디오 카드"),
    "testimonials-auto-advancing-quote-slider": ("자동 롤링 추천사 슬라이더", "진행 링과 도트 인디케이터에 맞춰 한 편씩 넘어가는 인용문 슬라이더"),
    "testimonials-case-study-result-card": ("수치 성과 기반 고객 성공 사례 카드", "실제 달성한 비즈니스 성과 수치에 닻을 내린 설득력 있는 추천사"),
    "testimonials-social-post-wall": ("SNS 피드 형태의 찬사 모음 월", "트위터나 링크드인의 칭찬 멘션을 실제 포스트 모양으로 구성한 그리드"),
    "testimonials-review-badges-with-quote": ("G2/Capterra 신뢰 배지 포함 추천사", "공인된 외부 리뷰 플랫폼의 평점 배지가 뒷받침하는 고객 추천사"),
    "testimonials-avatar-tab-quote-switcher": ("인물 아바타 탭 추천사 전환기", "팀원이나 고객의 얼굴 사진을 클릭해 해당 인터뷰를 전환하는 탭"),
    "testimonials-scrolling-wall-of-love": ("양방향 무한 롤링 후기 마퀴(Marquee)", "두 줄의 후기 카드가 서로 반대 방향으로 끊임없이 흘러가는 효과"),
    "testimonials-filterable-quote-grid-by-industry": ("업종/산업군별 필터링 추천사 그리드", "칩을 클릭해 사용자의 비즈니스 영역과 동일한 분야의 후기만 선별"),
    "testimonials-interview-style-testimonial": ("Q&A 인터뷰 형식 고객 대담", "실제 대화 형식의 질문과 답변 중 핵심 문장을 뽑아낸 에디토리얼 후기"),
    "testimonials-quote-over-product-screenshot": ("제품 캡처 위에 얹은 고객 추천사", "칭찬받고 있는 실제 소프트웨어 UI 화면 위에 투명하게 올린 후기"),
    "testimonials-team-voices-for-careers": ("재직자 인터뷰 채용 추천사", "실제 회사에서 일하는 크루들이 전하는 사내 문화와 경험담"),
    "testimonials-logo-wall-with-hover-quotes": ("호버 시 후기가 나타나는 로고 월", "고객사 로고 위에 마우스를 올리면 해당 기업의 추천사가 팝업"),
    "testimonials-voice-note-testimonial-player": ("실제 음성 녹음 추천사 플레이어", "고객의 생생한 육성 오디오와 텍스트 스크립트가 동기화되는 플레이어"),

    "footer-multi-column-footer": ("다열 링크 그리드 표준 푸터", "브랜드 정보, 4개 열의 탐색 링크, 저작권 및 법적 고지가 완비된 푸터"),
    "footer-minimal-centered-footer": ("미니멀 중앙 정렬 푸터", "로고와 한 줄의 인라인 링크, 카피라이트로 깔끔하게 끝맺는 푸터"),
    "footer-compact-app-footer-bar": ("인앱 초슬림 유틸리티 푸터 바", "시스템 정상 작동 상태와 언어 설정만 담은 슬림한 하단 바"),
    "footer-regulated-disclosure-footer": ("금융/의료 규제 고지용 푸터", "복잡한 법적 필수 고지 사항과 면책 조항을 가독성 있게 정리한 푸터"),
    "footer-accordion-footer-for-mobile": ("모바일 반응형 아코디언 푸터", "작은 모바일 화면에서는 링크 목록이 접히는 아코디언 구조 푸터"),

    "faq-accordion-list": ("네이티브 details 태그 아코디언 FAQ", "별도 스크립트 없이 부드럽게 펼쳐지는 HTML 네이티브 아코디언 질문 목록"),
    "faq-two-column-faq": ("2열 좌우 분할 자주 묻는 질문", "왼쪽에는 제목과 안내문, 오른쪽에는 질문과 답변 목록을 배치한 레이아웃"),
    "faq-searchable-faq-with-filters": ("실시간 검색 및 필터 지원 FAQ", "검색창과 주제별 필터 칩으로 원하는 질문을 즉시 찾아내는 인터페이스"),
    "faq-accordion-with-helpful-votes": ("도움이 되었나요 평가 투표 포함 FAQ", "답변을 읽은 후 유용성 평가(👍/👎)를 바로 수집하는 아코디언"),
    "faq-faq-with-category-rail": ("카테고리 레일 고정형 FAQ", "왼쪽에 주제 목록이 고정되어 원하는 분야로 빠르게 스크롤하는 FAQ"),
    "faq-faq-with-copy-link-anchors": ("질문별 고유 공유 링크(URL) 복사 FAQ", "각 질문마다 고유 앵커 링크가 있어 특정 질문만 즉시 공유 가능한 뷰"),
    "faq-billing-faq-with-plan-recap": ("현재 플랜 요약과 결제 FAQ", "현재 이용 중인 요금제 요약 정보 옆에 자주 묻는 결제 질문을 함께 배치"),
    "faq-conversational-faq-bubbles": ("대화형 말풍선 스타일 FAQ", "메신저 채팅 말풍선 모양으로 질문과 답변을 감각적으로 표현한 FAQ"),
    "faq-faq-tabs-by-audience": ("이용자 대상별(구매자/관리자/개발자) FAQ", "역할별로 나누어 각자의 눈높이에 맞는 답변을 제공하는 탭 FAQ"),
    "faq-troubleshooting-decision-tree": ("문제 해결 디시전 트리(의사결정) FAQ", "질문에 예/아니오로 답해 나가며 해결책에 도달하는 단계형 안내"),
    "faq-glossary-index-a-to-z": ("알파벳/가나다 색인 용어집 FAQ", "첫 글자 인덱스를 클릭해 용어 정의로 빠르게 이동하는 사전형 FAQ"),
    "faq-shipping-and-returns-faq": ("배송 및 반품/환불 안내 FAQ", "배송 소요 기간, 반품 절차 및 지역별 배송비 안내 표가 포함된 FAQ"),
    "faq-faq-with-demo-video-cards": ("시연 영상 카드 포함 FAQ", "글로 된 설명과 함께 짧은 시연 클립 비디오로 궁금증을 풀어주는 FAQ"),

    "dashboards-sidebar-stat-cards": ("사이드바 앱 셸과 핵심 지표 카드", "고정 사이드바 메뉴와 상단 지표 카드 행이 어우러진 대시보드 셸"),
    "dashboards-data-table-with-toolbar": ("검색 툴바 및 상태 칩 포함 데이터 표", "실시간 검색과 상태 배지 필터링이 지원되는 반응형 테이블"),
    "dashboards-chart-card-with-legend": ("범례 및 기간 필터 포함 차트 카드", "순수 CSS 누적 바 차트와 기간 선택기(7일/30일/90일)가 탑재된 카드"),
    "dashboards-inbox-split-view": ("수신함 분할 뷰 (마스터-디테일)", "왼쪽 대화 목록과 오른쪽 상세 본문 읽기 창이 결합된 인박스 뷰"),
    "dashboards-analytics-overview-with-range-chips": ("기간별 통계 요약 대시보드", "조회 기간 선택 칩에 따라 페이지의 모든 수치가 유기적으로 전환"),
    "dashboards-usage-and-billing-meters": ("자원 사용량 및 요금 청구 미터기", "요금제 허용치 대비 현재 리소스 사용량을 게이지로 보여주는 위젯"),
    "dashboards-incident-board": ("실시간 장애 및 인시던트 관리 보드", "심각도 등급, 담당자, 조치 현황이 실시간으로 관리되는 인시던트 현황판"),
    "dashboards-week-schedule-grid": ("주간 주별 일정 타임 블록 그리드", "7일간의 시간대별 블록과 현재 시각선(Now line)이 표시되는 스케줄러"),
    "dashboards-log-viewer-with-live-tail": ("실시간 라이브 테일 로그 뷰어", "스트리밍되는 시스템 로그를 레벨별로 필터링하고 일시정지할 수 있는 콘솔"),
    "dashboards-cost-explorer-by-service": ("클라우드 서비스별 비용 지출 분석", "인프라 서비스별 지출 비중과 다음 달 예상 비용을 예측하는 차트"),
    "dashboards-regional-performance-board": ("글로벌 리전별 응답 속도 및 가동률", "세계 지도 블록 옆에 리전별 지연 시간(Latency)과 가동률을 표시하는 보드")
}

def translate_prompt_to_korean(en_prompt, slug, title_ko):
    p = en_prompt.strip()

    # Generic opening conversion
    p_ko = p
    p_ko = re.sub(r'^(?:Build|Create|Design|Make)\s+(?:an?|the)\s+(.*?)\s+with\s+Tailwind\s+CSS\.?',
                  r'Tailwind CSS를 사용하여 \1를 제작하세요.', p_ko, flags=re.IGNORECASE)

    replacements = [
        (r'\bcentered\b', '중앙 정렬된'),
        (r'\bfull-height\b', '전체 높이(full-height)'),
        (r'\bfull-width\b', '너비 100%(full-width)'),
        (r'\bsplit-screen\b', '화면 분할(split-screen)'),
        (r'\bsoft neutral background\b', '은은한 중립 톤(neutral) 배경'),
        (r'\bdark background\b', '어두운 다크 배경'),
        (r'\bheadline\b', '헤드라인 제목'),
        (r'\bsubtitle\b', '부제목'),
        (r'\bsubtle borders?\b', '은은한 테두리선'),
        (r'\bclear focus rings?\b', '선명한 포커스 링'),
        (r'\bgenerous spacing\b', '여유로운 여백과 간격'),
        (r'\bresponsive\b', '반응형'),
        (r'\bbreakpoint\b', '브레이크포인트'),
        (r'\bhidden below the lg breakpoint\b', 'lg 브레이크포인트 미만에서는 숨김 처리'),
        (r'\bprimary button\b', '주요 강조(primary) 버튼'),
        (r'\bsecondary button\b', '보조(secondary) 버튼'),
        (r'\boutline button\b', '아웃라인 버튼'),
        (r'\bghost button\b', '고스트 버튼'),
        (r'\bdivider\b', '구분선'),
        (r'\btestimonial\b', '고객 추천사'),
        (r'\bavatar\b', '아바타 이미지'),
        (r'\bcheckbox\b', '체크박스'),
        (r'\binputs?\b', '입력 필드'),
        (r'\bdropdown\b', '드롭다운'),
        (r'\bmodal\b', '모달 팝업'),
        (r'\bplaceholder\b', '플레이스홀더'),
        (r'\bcard\b', '카드'),
        (r'\btiles?\b', '타일'),
        (r'\baccordion\b', '아코디언'),
        (r'\btooltip\b', '툴팁'),
        (r'\btoggle\b', '토글 스위치'),
        (r'\bbadge\b', '배지'),
        (r'\bcarousel\b', '캐러셀 슬라이더'),
        (r'\btimeline\b', '타임라인'),
        (r'\bprogress bar\b', '진행률 표시 바'),
        (r'\bstatus\b', '상태'),
        (r'\bclickable\b', '클릭 가능한'),
        (r'\bhover effects?\b', '호버 인터랙션 효과'),
        (r'\btransition\b', '전환 애니메이션'),
        (r'\bclipboard\b', '클립보드'),
        (r'\bcopy button\b', '복사 버튼'),
        (r'\bdesktop and mobile\b', '데스크톱 및 모바일'),
        (r'\btablet\b', '태블릿'),
        (r'\bnavigation bar\b', '내비게이션 바'),
        (r'\bfooter\b', '푸터'),
        (r'\bheader\b', '헤더'),
        (r'\bsidebar\b', '사이드바'),
        (r'\bterms and privacy\b', '이용약관 및 개인정보처리방침'),
    ]

    script_split = re.split(r'\bThen add JavaScript (?:that|to)\b', p_ko, flags=re.IGNORECASE)
    if len(script_split) == 2:
        ui_part = script_split[0].strip()
        js_part = script_split[1].strip()

        js_part = js_part.replace("copies", "클립보드에 복사하고")
        js_part = js_part.replace("flips the button label", "버튼 레이블을 일시적으로 변경하며")
        js_part = js_part.replace("disabled until", "조건이 충족될 때까지 비활성화하고")
        js_part = js_part.replace("on click", "클릭 시")
        js_part = js_part.replace("calculates", "실시간으로 계산하여")
        js_part = js_part.replace("toggles", "열고 닫는 토글을 구현하고")

        p_ko = f"{ui_part}\n\n그런 다음 실무에서 기대하는 동작을 위해 JavaScript를 추가하세요: {js_part}"

    for eng, kor in replacements:
        p_ko = re.sub(eng, kor, p_ko, flags=re.IGNORECASE)

    p_ko = re.sub(r' +', ' ', p_ko)
    p_ko = p_ko.replace("제작하세요. ", "제작하세요: ")
    p_ko = p_ko.replace("Include ", "구성 요소로는 ")
    p_ko = p_ko.replace("Keep it ", "디자인 스타일은 ")

    return p_ko

def main():
    json_path = "data/prompts.json"
    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    updated_titles = 0
    updated_descs = 0
    updated_prompts = 0

    for it in items:
        slug = it["slug"]

        if slug in CURATED_TRANSLATIONS:
            ko_title, ko_desc = CURATED_TRANSLATIONS[slug]
            if it.get("titleKo") != ko_title:
                it["titleKo"] = ko_title
                updated_titles += 1
            if it.get("descKo") != ko_desc:
                it["descKo"] = ko_desc
                updated_descs += 1

        prompt_en = it.get("promptEn", "")
        refined_prompt = translate_prompt_to_korean(prompt_en, slug, it["titleKo"])
        if refined_prompt != it.get("promptKo"):
            it["promptKo"] = refined_prompt
            updated_prompts += 1

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"✅ Full curated localization complete for {len(items)} items:")
    print(f" - Updated {updated_titles} titles")
    print(f" - Updated {updated_descs} descriptions")
    print(f" - Refined {updated_prompts} Korean prompts")

if __name__ == "__main__":
    main()
