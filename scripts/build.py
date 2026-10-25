import json
import re
import html

def build_search_blob(item):
    tokens = [
        item.get("titleKo", ""),
        item.get("titleEn", ""),
        item.get("descKo", ""),
        item.get("descEn", ""),
        item.get("catKo", ""),
        item.get("cat", ""),
        item.get("promptKo", "")[:200],
        item.get("promptEn", "")[:200],
    ]
    raw = " ".join(tokens).lower()
    cleaned = re.sub(r"\s+", " ", raw).strip()
    return html.escape(cleaned, quote=True)

def generate_card_html(item):
    slug = item["slug"]
    cat = item.get("cat", "")
    catKo = item.get("catKo", "")
    titleKo = html.escape(item.get("titleKo", ""))
    descKo = html.escape(item.get("descKo", ""))
    bg = item.get("bg", "rgb(255 255 255)")
    search_blob = build_search_blob(item)

    card = f'''<article class="card" data-cat="{cat}" data-slug="{slug}" data-search="{search_blob}">
  <div class="card-link" role="button" tabindex="0" data-slug="{slug}" aria-label="{titleKo} 상세보기">
    <div class="card-stage has-shot" style="--shot-bg:{bg}">
      <button class="card-fav-btn" data-fav="{slug}" title="즐겨찾기 추가/제거" aria-label="즐겨찾기">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
        </svg>
      </button>
      <img class="card-shot" src="./previews/{slug}.avif" alt="{titleKo} 미리보기" width="600" height="400" loading="lazy" decoding="async">
    </div>
    <div class="card-foot">
      <div class="row">
        <div class="card-meta">
          <span class="card-tag mono">{catKo}</span>
          <h3 class="name">{titleKo}</h3>
          <div class="desc">{descKo}</div>
        </div>
        <div class="card-actions">
          <button class="quick-copy-btn" data-quick-copy="{slug}" title="한국어 프롬프트 바로 복사" aria-label="프롬프트 복사">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            <span class="quick-copy-text">복사</span>
          </button>
          <span class="view-code">보기</span>
        </div>
      </div>
    </div>
  </div>
</article>'''
    return card

def main():
    with open("data/prompts.json", "r", encoding="utf-8") as f:
        items = json.load(f)

    # Category counts
    counts = {"all": len(items)}
    for it in items:
        cat = it.get("cat", "other")
        counts[cat] = counts.get(cat, 0) + 1

    cards_html = "\n".join([generate_card_html(it) for it in items])

    with open("index.html", "r", encoding="utf-8") as f:
        index_content = f.read()

    # 1. Update Grid Content
    grid_pattern = r'(<div class="grid" id="grid"[^>]*>).*?(</div>\s*<div class="empty-state)'
    new_grid = f'\\1\n{cards_html}\n        \\2'
    index_content = re.sub(grid_pattern, new_grid, index_content, flags=re.DOTALL)

    # 2. Add Favorite item in sidebar if not present
    if 'data-cat="fav"' not in index_content:
        fav_nav_item = '''<a class="cat" href="javascript:void(0)" data-cat="fav" title="즐겨찾기">
  <svg class="cat-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
  <span class="cat-name">★ 즐겨찾기</span>
  <span class="cat-count" id="favCount">0</span>
</a>\n'''
        index_content = index_content.replace(
            '<a class="cat active" href="javascript:void(0)" data-cat="all" title="전체">',
            fav_nav_item + '<a class="cat active" href="javascript:void(0)" data-cat="all" title="전체">'
        )

    # 3. Update category counts in sidebar
    for cat_id, cnt in counts.items():
        cat_pattern = rf'(<a class="cat[^"]*"\s+href="[^"]*"\s+data-cat="{cat_id}"[^>]*>.*?<span class="cat-count">)\d+(</span>)'
        index_content = re.sub(cat_pattern, rf'\g<1>{cnt}\g<2>', index_content, flags=re.DOTALL)

    # 4. Update total count
    index_content = re.sub(r'id="resultsCount">\d+개 프롬프트<', f'id="resultsCount">{len(items)}개 프롬프트<', index_content)
    index_content = re.sub(r'<div class="hero-sub mono">\d+개 프롬프트', f'<div class="hero-sub mono">{len(items)}개 프롬프트', index_content)

    # 5. Fix breadcrumb reload bug
    index_content = index_content.replace(
        '<a href="./">‹ 라이브러리</a>',
        '<button type="button" class="breadcrumb-back-btn" data-close>‹ 라이브러리</button>'
    )

    # 6. Ensure Modal Navigation & Cart Bar are present
    if 'id="modalPrevBtn"' not in index_content:
        # Update modal head with navigation buttons
        old_modal_head = '''<div class="code-modal-head">
        <div class="code-modal-title" id="modalTitle">프롬프트 상세</div>
        <button class="code-modal-close" data-close aria-label="닫기">✕</button>
      </div>'''
        new_modal_head = '''<div class="code-modal-head">
        <div class="code-modal-title" id="modalTitle">프롬프트 상세</div>
        <div class="modal-nav-group">
          <button class="modal-nav-btn" id="modalPrevBtn" title="이전 프롬프트 (←)" aria-label="이전 프롬프트">‹</button>
          <button class="modal-nav-btn" id="modalNextBtn" title="다음 프롬프트 (→)" aria-label="다음 프롬프트">›</button>
          <button class="code-modal-close" data-close aria-label="닫기">✕</button>
        </div>
      </div>'''
        index_content = index_content.replace(old_modal_head, new_modal_head)

    if 'id="promptCustomizer"' not in index_content:
        # Add customizer right before code-tabs
        customizer_markup = '''<!-- Prompt Customizer -->
        <div class="prompt-customizer" id="promptCustomizer">
          <div class="customizer-group">
            <span class="customizer-label">프레임워크:</span>
            <button class="opt-chip active" data-opt="fw" data-val="html">HTML</button>
            <button class="opt-chip" data-opt="fw" data-val="react">React / Next.js</button>
            <button class="opt-chip" data-opt="fw" data-val="vue">Vue 3</button>
          </div>
          <div class="customizer-group">
            <span class="customizer-label">옵션:</span>
            <button class="opt-toggle active" data-toggle="korean-ui" title="모든 버튼, 텍스트, 플레이스홀더를 자연스러운 한국어로 작성">🇰🇷 한국어 UI 텍스트</button>
            <button class="opt-toggle" data-toggle="dark-mode" title="dark: 유틸리티 클래스로 다크 모드 스타일 지원">🌙 다크 모드</button>
          </div>
        </div>
        <div class="code-tabs">'''
        index_content = index_content.replace('<div class="code-tabs">', customizer_markup)

    if 'id="previewFontToggle"' not in index_content:
        # Add Font toggle button to stage-sizes
        old_stage_sizes = '''<div class="stage-sizes" id="modalStageSizes">
              <button class="size active" data-size="full">전체 화면 (Full)</button>
              <button class="size" data-size="tablet">태블릿 (Tablet)</button>
              <button class="size" data-size="mobile">모바일 (Mobile)</button>
            </div>'''
        new_stage_sizes = '''<div class="stage-sizes" id="modalStageSizes">
              <button class="size active" data-size="full">전체 화면 (Full)</button>
              <button class="size" data-size="tablet">태블릿 (Tablet)</button>
              <button class="size" data-size="mobile">모바일 (Mobile)</button>
              <button class="font-toggle-btn active" id="previewFontToggle" title="프리뷰에 Pretendard 한글 폰트 적용 여부 토글">한글 폰트 On</button>
            </div>'''
        index_content = index_content.replace(old_stage_sizes, new_stage_sizes)

    if 'id="promptCartBar"' not in index_content:
        # Add Cart Floating Bar before closing body
        cart_bar_markup = '''  <!-- Prompt Cart Floating Bar -->
  <div class="prompt-cart-bar hidden" id="promptCartBar">
    <div class="cart-info">
      <span class="cart-count-badge" id="cartCountBadge">0</span>
      <span class="cart-title">개 섹션 선택됨</span>
      <span class="cart-names" id="cartSectionNames"></span>
    </div>
    <div class="cart-actions">
      <button class="cart-btn cart-copy-btn" id="cartCopyBtn">🚀 통합 랜딩페이지 프롬프트 복사</button>
      <button class="cart-btn cart-clear-btn" id="cartClearBtn">비우기</button>
    </div>
  </div>

  <!-- Toast Message -->'''
        index_content = index_content.replace('<!-- Toast Message -->', cart_bar_markup)

    # Add Cart Toggle button in modal detail-actions if not present
    if 'id="modalCartToggleBtn"' not in index_content:
        index_content = index_content.replace(
            '<p class="detail-desc" id="modalPromptDesc" style="color: var(--ink-dim); font-size: 15px;">설명</p>',
            '''<p class="detail-desc" id="modalPromptDesc" style="color: var(--ink-dim); font-size: 15px;">설명</p>
            <div style="margin-top: 10px; display: flex; gap: 8px;">
              <button type="button" class="lang-toggle-btn" id="modalFavToggleBtn">★ 즐겨찾기</button>
              <button type="button" class="lang-toggle-btn" id="modalCartToggleBtn">+ 장바구니에 담기</button>
            </div>'''
        )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_content)

    print(f"✅ Successfully rebuilt index.html with all enhanced features!")

if __name__ == "__main__":
    main()
