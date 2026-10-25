import json
import re

POST_CLEANUPS = [
    (r'~위에\s*왼쪽,?\s*', '왼쪽 영역: '),
    (r'~위에\s*오른쪽,?\s*', '오른쪽 영역: '),
    (r'~위에\s*', ''),
    (r'~안에\s*', '내에 '),
    (r'~로\s*', '로 '),
    (r'~사이에\s*', '사이에 '),
    (r'~전반에 걸쳐\s*', '전체에 '),
    (r'출처:\s*', '에서 '),
    (r'포함하여\s*', '포함, '),
    (r'모서리가 둥근-(xl|2xl|lg|md|sm|full)', r'rounded-\1'),
    (r'활성 상태\s*-state\s*포커스 상태\s*ring', '활성화 시 선명한 포커스 링'),
    (r'은은하게 톤다운된\s*line', '은은한 안내 문구'),
    (r'포커스 상태\s*ring', '포커스 링'),
    (r'활성 상태\s*', '활성화 상태 '),
    (r'비활성화 상태\s*', '비활성화 상태 '),
    (r'\(~360px wide\)', '(약 360px 너비)'),
    (r'(\d+)px wide\b', r'\1px 너비'),
    (r'(\d+)px tall\b', r'\1px 높이'),
    (r'최대 너비\(최대 너비 (max-w-\w+)\)', r'최대 너비(\1)'),
    (r'둥근 모서리\(둥근 모서리 (rounded-\w+)\)', r'둥근 모서리(\1)'),
    (r'최대 너비\s*최대 너비', '최대 너비'),
    (r'둥근 모서리\s*둥근 모서리', '둥근 모서리'),
    (r'버튼를\b', '버튼을'),
    (r'창를\b', '창을'),
    (r'문구를\b', '문구를'),
    (r'를 구성하세요\.를 구성하세요\.', '를 구성하세요.'),
    (r'를 구성하세요\.\s*를 구성하세요\.', '를 구성하세요.'),
    (r'적용를 구성하세요\.', '적용하세요.'),
    (r'유지를 구성하세요\.', '유지하세요.'),
    (r'구성를 구성하세요\.', '구성하세요.'),
    (r'배치를 구성하세요\.', '배치하세요.'),
    (r'포함를 구성하세요\.', '포함하세요.'),
    (r'centered login\b', '중앙 정렬된 로그인'),
    (r'centered sign-up\b', '중앙 정렬된 회원가입'),
    (r'centered\b', '중앙 정렬된'),
    (r'sign-in\b', '로그인'),
    (r'sign-up\b', '회원가입'),
    (r'login\b', '로그인'),
    (r'signup\b', '회원가입'),
    (r'passwordless\b', '비밀번호 없는'),
    (r'Verify\b', '인증하기'),
    (r'Resend\b', '재전송'),
    (r'Submit\b', '제출하기'),
    (r'Cancel\b', '취소'),
    (r'Save\b', '저장'),
    (r'Edit\b', '수정'),
    (r'Delete\b', '삭제'),
    (r'Search\b', '검색'),
    (r'Google\b', '구글(Google)'),
    (r'terms and privacy\b', '이용약관 및 개인정보처리방침'),
    (r'terms of service\b', '서비스 이용약관'),
    (r'privacy policy\b', '개인정보처리방침'),
    (r'Didn\'t get it\? 재전송 내에 0:30', '인증번호를 받지 못하셨나요? 0:30 후 재전송'),
    (r'Didn\'t get it\? Resend in 0:30', '인증번호를 받지 못하셨나요? 0:30 후 재전송'),
    (r'six separate square inputs', '6개의 독립된 정사각형 입력칸'),
    (r'square inputs', '정사각형 입력칸'),
    (r'in row\b', '가로 한 줄로 배치'),
    (r'in column\b', '세로 열로 배치'),
    (r'size-12', '가로세로 크기 size-12'),
    (r'text-center', '가운데 정렬(text-center)'),
    (r'large font', '큼직한 폰트 크기'),
    (r'\n-\s*\n', '\n'),
    (r'Then add JavaScript.*', ''),
]

def final_polish(text):
    for pattern, repl in POST_CLEANUPS:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def run():
    with open("data/prompts.json", "r", encoding="utf-8") as f:
        items = json.load(f)

    for it in items:
        ko = it.get("promptKo", "")
        polished = final_polish(ko)

        # Append clean JS instruction if the component had a script
        if it.get("script"):
            js_snippet = it.get("script")
            js_summary = []
            if "otp" in it["slug"]:
                js_summary.append("한 글자 입력 시 다음 칸으로 자동 포커스 이동 및 백스페이스 시 이전 칸 이동")
                js_summary.append("6자리 인증번호 일괄 붙여넣기(Paste) 지원 및 숫자 이외 문자 자동 필터링")
                js_summary.append("모든 칸이 채워질 때까지 인증 버튼 비활성화, 30초 카운트다운 타이머 동작")
            elif "password" in it["slug"] or "meter" in it["slug"]:
                js_summary.append("키 입력 시 비밀번호 보안 조건(길이, 숫자, 특수문자, 대소문자 일치) 실시간 검증")
                js_summary.append("조건 만족 시 체크 표시(✓) 전환 및 강도 게이지 바 색상 실시간 반영")
                js_summary.append("모든 필수 조건 통과 전까지 제출 버튼 비활성화")
            elif "copy" in it["slug"] or "secret" in it["slug"]:
                js_summary.append("버튼 클릭 시 해당 텍스트/코드를 클립보드에 복사하고 일시적으로 '복사됨!' 피드백 표시")
            elif "tab" in it["slug"] or "switcher" in it["slug"]:
                js_summary.append("탭 클릭 시 활성화 스타일 전환 및 해당하는 콘텐츠 패널만 즉시 표시")
            elif "accordion" in it["slug"] or "faq" in it["slug"]:
                js_summary.append("항목 클릭 시 부드러운 아코디언 열림/닫힘 토글 및 다른 항목 자동 닫기 처리")
            elif "calc" in it["slug"] or "planner" in it["slug"] or "counter" in it["slug"]:
                js_summary.append("사용자 입력 값(수량, 슬라이더, 토글) 변경 시 실시간으로 결과 수치 재계산")
            elif "filter" in it["slug"] or "search" in it["slug"]:
                js_summary.append("검색어 입력 또는 카테고리 칩 선택 시 해당하는 항목만 즉각 필터링 노출")
            else:
                js_summary.append("버튼 클릭, 상태 변경, 입력 폼 검증 등 컴포넌트 실사용 인터랙션 구현")

            if "[필수 인터랙티브 동작 구현]" not in polished:
                js_bullets = "\n".join([f"- {s}" for s in js_summary])
                polished += f"\n\n[필수 인터랙티브 동작 구현]\n자바스크립트를 작성하여 실제 서비스와 동일한 사용자 경험을 제공하세요:\n{js_bullets}"

        it["promptKo"] = polished

    with open("data/prompts.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print("✅ Polish completed!")

if __name__ == "__main__":
    run()
