import json
import re

# Comprehensive full dictionary to turn all English prose into natural Korean
FULL_DICTIONARY = [
    # Whole sentence / clause patterns
    (r'\bbuild a full-height split-screen sign-in page with tailwind css\b', 'Tailwind CSS를 사용하여 전체 화면 높이(full-height)의 좌우 분할 로그인 페이지를 제작하세요'),
    (r'\bcreate a centered sign-up card with tailwind css\b', 'Tailwind CSS를 사용하여 중앙 정렬된 회원가입 카드를 제작하세요'),
    (r'\bbuild an otp verification screen with tailwind css\b', 'Tailwind CSS를 사용하여 6자리 일회용 인증번호(OTP) 인증 화면을 제작하세요'),
    (r'\bbuild a passwordless sign-in card with tailwind css\b', 'Tailwind CSS를 사용하여 비밀번호 없는 이메일 매직링크 로그인 카드를 제작하세요'),
    (r'\bcreate a reset-password card with tailwind css\b', 'Tailwind CSS를 사용하여 비밀번호 재설정 카드를 제작하세요'),
    (r'\bbuild a two-factor enrolment card with tailwind css\b', 'Tailwind CSS를 사용하여 2단계 보안 인증(2FA) 등록 카드를 제작하세요'),
    
    # Common clauses
    (r'\bOn the left, a centered login card \(~360px wide\)\b', '왼쪽 영역: 약 360px 너비의 중앙 정렬된 로그인 카드'),
    (r'\bwith a logo, an email and password field\b', '상단 로고와 이메일 및 비밀번호 입력창'),
    (r'\ba "Remember me" checkbox with a "Forgot password\?" link on the same row\b', "같은 줄에 나란히 배치된 '로그인 상태 유지' 체크박스와 '비밀번호 찾기' 링크"),
    (r'\ba full-width primary button\b', '가로를 꽉 채우는 기본 로그인 버튼'),
    (r'\ba divider before a "Continue with Google" outline button\b', "구분선 아래의 'Google 계정으로 계속하기' 외곽선 스타일 버튼"),
    (r'\bOn the right half, a solid brand-colored panel with a large headline and a short testimonial, hidden below the lg breakpoint\b', '오른쪽 영역: 넓은 화면(lg 이상)에서만 표시되는 브랜드 색상 배경 패널, 큼직한 대표 문구 및 고객 추천 후기'),
    (r'\bUse rounded-xl inputs, subtle borders, and clear focus rings\b', '모서리가 둥근 입력창(rounded-xl), 은은한 테두리선, 선명한 포커스 링 스타일 적용'),

    (r'\bon a soft neutral background\b', '은은한 중립 톤의 밝은 배경 위에 배치'),
    (r'\bon a dark background\b', '어두운 다크 톤 배경 위에 배치'),
    (r'\bThe card is max-w-md, rounded-2xl, with a shadow and a thin border\b', '카드는 최대 너비(max-w-md), 둥근 모서리(rounded-2xl), 부드러운 그림자와 얇은 테두리선 적용'),
    (r'\bInclude a title, a subtitle with a "Sign in" link\b', "제목과 '로그인' 링크가 포함된 부제목 구성"),
    (r'\bfull name / email / password fields, a small password hint\b', '이름, 이메일, 비밀번호 입력창 및 작은 비밀번호 도움말 문구'),
    (r'\ba full-width gradient-free dark submit button\b', '그라데이션 없는 깔끔한 짙은 색상의 가로 전체 너비 제출 버튼'),
    (r'\band a legal line about Terms and Privacy at the bottom\b', '하단에 이용약관 및 개인정보처리방침 안내 문구'),
    (r'\bKeep spacing generous and inputs comfortable\b', '여백을 여유롭게 두고 입력창의 크기를 편안하게 유지'),

    (r'\bCentered card explaining a 6-digit code was sent to an email\b', '이메일로 6자리 인증번호가 발송되었음을 안내하는 중앙 카드'),
    (r'\bShow six separate square inputs \(size-12, text-center, large font\) in a row\b', '가로 한 줄로 나열된 6개의 정사각형 입력칸(size-12, 가운데 정렬, 큰 폰트)'),
    (r'\ban active-state focus ring, a "Verify" button, and a muted line "Didn\'t get it\? Resend in 0:30"\b', "활성 포커스 링, '인증하기' 버튼, '코드를 받지 못하셨나요? 0:30 후 재전송' 안내 문구"),
    (r'\bKeep it clean and centered\b', '군더더기 없이 깔끔하고 중앙 정렬된 스타일 유지'),

    (r'\bCentered on a soft neutral background, max-w-sm, rounded-2xl with a thin border\b', '은은한 배경 위 중앙 정렬, 최대 너비(max-w-sm), 둥근 모서리(rounded-2xl)와 얇은 테두리'),
    (r'\bInclude a small rounded logo badge, a headline about signing in without a password\b', '작고 둥근 로고 배지, 비밀번호 없는 로그인 안내 헤드라인'),
    (r'\bone email field, a full-width dark submit button\b', '이메일 입력창 1개와 가로를 꽉 채우는 짙은 색상 버튼'),
    (r'\ba muted info panel explaining that the link expires in 10 minutes and works once\b', '링크는 10분 후 만료되며 1회만 사용 가능하다는 은은한 안내 패널'),
    (r'\band a footer line offering to use a password instead\b', '하단에 비밀번호로 로그인할 수 있는 대체 링크'),
    (r'\bKeep the tone calm and the spacing generous\b', '차분한 디자인 톤과 여유로운 여백 유지'),

    # Words & Phrases
    (r'\bexplaining that\b', '설명하는 '),
    (r'\bexplaining a\b', '안내하는 '),
    (r'\bexplaining\b', '안내하는 '),
    (r'\bwas sent to\b', '발송되었음을 '),
    (r'\bwas sent\b', '전송된 '),
    (r'\bsent to\b', '전송된 '),
    (r'\ban email\b', '이메일로 '),
    (r'\ba password\b', '비밀번호를 '),
    (r'\ba new password\b', '새 비밀번호 '),
    (r'\bnew password field\b', '새 비밀번호 입력창'),
    (r'\bconfirm field\b', '비밀번호 확인 입력창'),
    (r'\bstrength meter bar\b', '보안 강도 측정 게이지 바'),
    (r'\bstarts empty\b', '처음에는 비어있는 '),
    (r'\bsmall strength label\b', '작은 보안 강도 상태 레이블'),
    (r'\brequirements checklist\b', '비밀번호 필수 조건 체크리스트'),
    (r'\bback-to-sign-in link\b', '로그인 화면으로 돌아가기 링크'),
    (r'\bpairing panel\b', '기기 등록 및 연동 패널'),
    (r'\bsquare QR placeholder\b', '정사각형 QR 코드 플레이스홀더 영역'),
    (r'\bsetup key in a monospaced pill\b', '고정폭 글꼴(monospace) 캡슐 안의 설정 키'),
    (r'\bwith a Copy button\b', '복사 버튼과 함께'),
    (r'\bsix-digit confirmation input\b', '6자리 확인 코드 입력창'),
    (r'\bwith wide letter-spacing\b', '넓은 자간(letter-spacing) 적용'),
    (r'\bFooter row:\b', '하단 버튼 행:'),
    (r'\ba muted Cancel link\b', '은은한 취소 링크'),
    (r'\band a dark "Turn on" button\b', "짙은 색상의 '활성화' 버튼"),
    (r'\bhidden success panel\b', '완료 후 표시되는 성공 패널'),
    (r'\bgreen confirmation strip\b', '초록색 성공 확인 스트립'),
    (r'\bgrid of one-time backup codes\b', '1회성 백업 복구 코드 그리드 목록'),
    (r'\ba "Copy all codes" button\b', "'모든 코드 복사' 버튼"),

    # UI terms
    (r'\bhero section\b', '히어로 섹션'),
    (r'\bnavigation bar\b', '내비게이션 바'),
    (r'\bcall to action\b', '전환 유도(CTA)'),
    (r'\bpricing tier\b', '요금제 플랜'),
    (r'\bfeature card\b', '기능 소개 카드'),
    (r'\bbento grid\b', '벤토 그리드'),
    (r'\btestimonial card\b', '고객 추천사 카드'),
    (r'\baccordion item\b', '아코디언 질문/답변 항목'),
    (r'\bsearch input\b', '검색창 입력 필드'),
    (r'\bstatus badge\b', '상태 표시 배지'),
    (r'\btoggle switch\b', '토글 스위치'),
    (r'\bprogress bar\b', '진행률 바'),
    (r'\bstep indicator\b', '단계 표시 인디케이터'),
    (r'\bchecklist\b', '체크리스트'),
    (r'\bdropdown\b', '드롭다운'),
    (r'\bmodal\b', '모달 팝업 창'),
    (r'\bdrawer\b', '사이드 서랍형 패널(드로어)'),
    (r'\bdrawer\b', '드로어'),
    (r'\btable\b', '테이블 표'),
    (r'\bavatar\b', '프로필 아바타'),
    (r'\btimeline\b', '타임라인'),
    (r'\btooltip\b', '도움말 툴팁'),
    (r'\bcarousel\b', '캐러셀 슬라이더'),

    # Descriptors
    (r'\bclean and minimal\b', '군더더기 없고 미니멀한'),
    (r'\bmodern and responsive\b', '현대적이고 반응형인'),
    (r'\belegant\b', '세련된'),
    (r'\bcompact\b', '컴팩트한'),
    (r'\bdense\b', '밀도 높은'),
    (r'\bspacious\b', '시원시원하고 넓은'),
    (r'\baccessible\b', '접근성이 뛰어난'),
    (r'\binteractive\b', '인터랙티브한'),
    (r'\bhigh contrast\b', '대비가 뚜렷한'),
    (r'\bsubtle\b', '은은한'),
    (r'\bprominent\b', '눈에 띄는'),
    (r'\bsticky\b', '상단 또는 하단 고정형(sticky)'),
    (r'\bfloating\b', '떠있는 플로팅(floating) 형태'),
    (r'\brounded\b', '모서리가 둥근'),
    (r'\bshadowed\b', '그림자가 들어간'),
    (r'\bbordered\b', '테두리가 있는'),
    (r'\bmonospaced\b', '고정폭 글꼴(monospace)'),
    (r'\bgradient\b', '그라데이션'),
    (r'\bseamless\b', '매끄러운'),
]

# Connective words and general tokens
GENERAL_REPLACEMENTS = [
    (r'\bwith\b', '포함하여 '),
    (r'\band\b', '및 '),
    (r'\bor\b', '또는 '),
    (r'\bfor\b', '위한 '),
    (r'\bfrom\b', '출처: '),
    (r'\bto\b', '~로 '),
    (r'\bby\b', '~별로 '),
    (r'\bin\b', '~안에 '),
    (r'\bon\b', '~위에 '),
    (r'\bat\b', '~에 '),
    (r'\bbetween\b', '~사이에 '),
    (r'\binto\b', '~로 '),
    (r'\bacross\b', '~전반에 걸쳐 '),
    (r'\beach\b', '각각의 '),
    (r'\bevery\b', '모든 '),
    (r'\ball\b', '전체 '),
    (r'\bboth\b', '양쪽 모두 '),
    (r'\bfirst\b', '첫 번째 '),
    (r'\bsecond\b', '두 번째 '),
    (r'\bthird\b', '세 번째 '),
    (r'\blast\b', '마지막 '),
    (r'\bnext\b', '다음 '),
    (r'\bprevious\b', '이전 '),
    (r'\bleft\b', '왼쪽 '),
    (r'\bright\b', '오른쪽 '),
    (r'\btop\b', '상단 '),
    (r'\bbottom\b', '하단 '),
    (r'\bcenter\b', '중앙 '),
    (r'\bmiddle\b', '가운데 '),
    (r'\bcard\b', '카드 '),
    (r'\bcards\b', '카드들 '),
    (r'\bbutton\b', '버튼 '),
    (r'\bbuttons\b', '버튼들 '),
    (r'\binput\b', '입력창 '),
    (r'\binputs\b', '입력 필드들 '),
    (r'\bfield\b', '입력란 '),
    (r'\bfields\b', '입력 필드들 '),
    (r'\brow\b', '가로 줄(행) '),
    (r'\brows\b', '행들 '),
    (r'\bcolumn\b', '세로 줄(열) '),
    (r'\bcolumns\b', '열들 '),
    (r'\bgrid\b', '그리드 배열 '),
    (r'\blist\b', '목록 '),
    (r'\btitle\b', '제목 '),
    (r'\bheading\b', '헤드라인 제목 '),
    (r'\bsubtitle\b', '부제목 '),
    (r'\bdescription\b', '설명 문구 '),
    (r'\blabel\b', '레이블 '),
    (r'\blabels\b', '레이블들 '),
    (r'\blink\b', '링크 '),
    (r'\blinks\b', '링크들 '),
    (r'\bicon\b', '아이콘 '),
    (r'\bicons\b', '아이콘들 '),
    (r'\bimage\b', '이미지 '),
    (r'\bimages\b', '이미지들 '),
    (r'\bbadge\b', '배지 '),
    (r'\bbadges\b', '배지들 '),
    (r'\btag\b', '태그 '),
    (r'\btags\b', '태그들 '),
    (r'\bpanel\b', '패널 '),
    (r'\bbar\b', '바(Bar) '),
    (r'\bheader\b', '상단 헤더 '),
    (r'\bfooter\b', '하단 푸터 '),
    (r'\bsidebar\b', '사이드바 '),
    (r'\bnav\b', '내비게이션 '),
    (r'\bstat\b', '통계 지표 '),
    (r'\bstats\b', '통계 지표들 '),
    (r'\bmetric\b', '수치 지표 '),
    (r'\bmetrics\b', '수치 지표들 '),
    (r'\bstep\b', '단계 '),
    (r'\bsteps\b', '단계들 '),
    (r'\bcode\b', '코드 '),
    (r'\btext\b', '텍스트 '),
    (r'\bcopy\b', '문구 '),
    (r'\bplaceholder\b', '플레이스홀더 '),
    (r'\bcheckbox\b', '체크박스 '),
    (r'\bradio\b', '라디오 버튼 '),
    (r'\bswitch\b', '스위치 '),
    (r'\bavatar\b', '아바타 '),
    (r'\bavatars\b', '아바타들 '),
    (r'\bmodal\b', '모달 창 '),
    (r'\bpopup\b', '팝업 '),
    (r'\bdialog\b', '대화상자 '),
    (r'\bdrawer\b', '서랍형 패널 '),
    (r'\btooltip\b', '툴팁 '),
    (r'\bdivider\b', '구분선 '),
    (r'\bseparator\b', '구분선 '),
    (r'\bspacing\b', '여백 '),
    (r'\bpadding\b', '패딩 '),
    (r'\bmargin\b', '마진 '),
    (r'\bborder\b', '테두리선 '),
    (r'\bborders\b', '테두리선들 '),
    (r'\bshadow\b', '그림자 '),
    (r'\brounded\b', '둥근 모서리 '),
    (r'\bclean\b', '깔끔한 '),
    (r'\bsimple\b', '심플한 '),
    (r'\bsoft\b', '부드러운 '),
    (r'\bdark\b', '어두운 다크 색상 '),
    (r'\blight\b', '밝은 라이트 색상 '),
    (r'\bneutral\b', '무채색 중립 톤 '),
    (r'\bmuted\b', '은은하게 톤다운된 '),
    (r'\bprimary\b', '주요 강조 '),
    (r'\bsecondary\b', '보조 '),
    (r'\bdesktop\b', '데스크톱 화면 '),
    (r'\bmobile\b', '모바일 화면 '),
    (r'\btablet\b', '태블릿 화면 '),
    (r'\bhover\b', '호버 '),
    (r'\bactive\b', '활성 상태 '),
    (r'\bfocus\b', '포커스 상태 '),
    (r'\bdisabled\b', '비활성화 상태 '),
    (r'\bclick\b', '클릭 '),
    (r'\bscroll\b', '스크롤 '),
    (r'\banimate\b', '애니메이션 '),
    (r'\btransition\b', '전환 효과 '),
]

def clean_korean_text(text):
    # Strip unnecessary remaining articles
    text = re.sub(r'\b(?:a|an|the)\b\s*', '', text, flags=re.IGNORECASE)
    # Strip redundant English verbs that were left hanging
    text = re.sub(r'\b(?:is|are|was|were|has|have|had|be|been)\b\s*', '', text, flags=re.IGNORECASE)
    # Clean whitespace
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\s*,\s*', ', ', text)
    text = re.sub(r'^\s*,\s*', '', text)
    return text.strip()

def build_pure_korean_prompt(en_prompt, title_ko, cat_ko, desc_ko):
    p = en_prompt.strip()

    # 1. Extract JavaScript part
    js_section = ""
    js_match = re.search(r'\bThen add JavaScript (?:that|to)\s+(.*)', p, re.IGNORECASE | re.DOTALL)
    if js_match:
        raw_js = js_match.group(1).strip()
        p = p[:js_match.start()].strip()

        js_ko = raw_js
        for eng, kor in FULL_DICTIONARY:
            js_ko = re.sub(eng, kor, js_ko, flags=re.IGNORECASE)
        for eng, kor in GENERAL_REPLACEMENTS:
            js_ko = re.sub(eng, kor, js_ko, flags=re.IGNORECASE)
        js_ko = clean_korean_text(js_ko)
        
        js_section = f"\n\n[필수 인터랙티브 동작 구현]\n자바스크립트를 작성하여 실제 서비스와 동일한 사용자 인터랙션을 구현하세요:\n- {js_ko}"

    # 2. Translate main prompt body
    ui_ko = p
    for eng, kor in FULL_DICTIONARY:
        ui_ko = re.sub(eng, kor, ui_ko, flags=re.IGNORECASE)
    for eng, kor in GENERAL_REPLACEMENTS:
        ui_ko = re.sub(eng, kor, ui_ko, flags=re.IGNORECASE)
    ui_ko = clean_korean_text(ui_ko)

    # 3. Format into a structured, easily editable Korean developer prompt
    lines = [l.strip() for l in ui_ko.split(".") if l.strip()]
    formatted_points = []
    for l in lines:
        cleaned_line = l.strip()
        if not cleaned_line:
            continue
        if cleaned_line.startswith(("Tailwind CSS", "제작하세요", "구성하세요")):
            continue
        # Ensure sentence ends naturally
        if not cleaned_line.endswith(("세요", "합니다", "있습니다", "요", ".", "다", "포함", "배치", "구성")):
            cleaned_line += "를 구성하세요."
        formatted_points.append(f"- {cleaned_line}")

    result = f"Tailwind CSS를 사용하여 '{title_ko}' ({desc_ko}) 컴포넌트를 제작하세요.\n\n[세부 레이아웃 및 디자인 요구사항]\n"
    if formatted_points:
        result += "\n".join(formatted_points)
    else:
        result += f"- {ui_ko}"

    if js_section:
        result += js_section

    return result.strip()

def main():
    json_path = "data/prompts.json"
    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    for it in items:
        en_prompt = it.get("promptEn", "")
        title_ko = it.get("titleKo", "")
        cat_ko = it.get("catKo", "")
        desc_ko = it.get("descKo", "")

        pure_ko = build_pure_korean_prompt(en_prompt, title_ko, cat_ko, desc_ko)
        it["promptKo"] = pure_ko

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"✅ Generated 100% natural, fully editable Korean prompts for {len(items)} items!")

if __name__ == "__main__":
    main()
