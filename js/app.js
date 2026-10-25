/* ============================================================
   VibePrompt KR — app.js (Enhanced Edition)
   바이브 코더를 위한 한국어 UI 프롬프트 라이브러리 & Tailwind CSS 스니펫
   기능:
     - 실시간 검색 & 카테고리 필터링 (한글/영문)
     - 즐겨찾기(★ 북마크) & 로컬스토리지 보존
     - 카드 퀵 복사 (Quick Copy)
     - 모달 키보드 내비게이션 (이전 ‹ / 다음 ›, 좌우 화살표 키)
     - 실시간 인터랙티브 프리뷰 (143개 JS 스크립트 실행 & 자동 높이 조절)
     - Pretendard 한글 폰트 프리뷰 토글
     - 프롬프트 커스터마이저 (React/HTML, 한국어 UI 문구, 다크모드 지시어)
     - 다중 섹션 통합 '랜딩페이지 프롬프트 장바구니' (Prompt Cart)
   ============================================================ */

(function () {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  const app = $(".app");
  const sidebar = $("#sidebar");
  const sideBurger = $("#sideBurger");
  const collapseBtn = $("#sideCollapse");
  const sideNav = $("#sideNav");
  const searchInput = $("#search");
  const grid = $("#grid");
  const emptyState = $("#empty");
  const resultsTitle = $("#resultsTitle");
  const resultsCount = $("#resultsCount");
  const toast = $("#toast");
  const favCountBadge = $("#favCount");

  // Modal elements
  const modal = $("#modal");
  const modalTitle = $("#modalTitle");
  const modalPrevBtn = $("#modalPrevBtn");
  const modalNextBtn = $("#modalNextBtn");
  const modalCatBreadcrumb = $("#modalCatBreadcrumb");
  const modalTag = $("#modalTag");
  const modalPromptTitle = $("#modalPromptTitle");
  const modalPromptDesc = $("#modalPromptDesc");
  const modalFavToggleBtn = $("#modalFavToggleBtn");
  const modalCartToggleBtn = $("#modalCartToggleBtn");
  const modalStageCanvas = $("#modalStageCanvas");
  const modalStageSizes = $("#modalStageSizes");
  const modalPreviewFrame = $("#modalPreviewFrame");
  const previewFontToggle = $("#previewFontToggle");
  const promptCustomizer = $("#promptCustomizer");
  const modalCopyBtn = $("#modalCopyBtn");
  const panePromptKo = $("#panePromptKo");
  const panePromptEn = $("#panePromptEn");
  const paneCodeHtml = $("#paneCodeHtml");
  const codeSnippetText = $("#codeSnippetText");

  // Cart Floating Bar elements
  const promptCartBar = $("#promptCartBar");
  const cartCountBadge = $("#cartCountBadge");
  const cartSectionNames = $("#cartSectionNames");
  const cartCopyBtn = $("#cartCopyBtn");
  const cartClearBtn = $("#cartClearBtn");

  // State
  let promptsMap = {};
  let promptsList = [];
  let visibleSlugs = [];
  let activeCat = "all";
  let activeTab = "prompt-ko";
  let currentPrompt = null;
  let toastTimer = null;
  let usePretendardInPreview = true;

  // Customizer options
  let customFw = "html"; // html | react | vue
  let customKoreanUi = true;
  let customDarkMode = false;

  // Storage sets
  let favs = new Set();
  let cart = new Set();

  function loadStorage() {
    try {
      const savedFavs = localStorage.getItem("vibeprompt_favs");
      if (savedFavs) favs = new Set(JSON.parse(savedFavs));

      const savedCart = localStorage.getItem("vibeprompt_cart");
      if (savedCart) cart = new Set(JSON.parse(savedCart));
    } catch (e) {
      console.error("Storage load error:", e);
    }
    updateFavBadges();
    updateCartBar();
  }

  function saveStorage() {
    try {
      localStorage.setItem("vibeprompt_favs", JSON.stringify(Array.from(favs)));
      localStorage.setItem("vibeprompt_cart", JSON.stringify(Array.from(cart)));
    } catch (e) {
      console.error("Storage save error:", e);
    }
  }

  // Toast Notification
  function showToast(msg) {
    if (!toast) return;
    toast.textContent = msg || "클립보드에 복사되었습니다!";
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.classList.remove("show");
    }, 2200);
  }

  // Copy to Clipboard
  async function copyText(text, successMsg) {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        const textarea = document.createElement("textarea");
        textarea.value = text;
        textarea.style.position = "fixed";
        textarea.style.left = "-9999px";
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
      }
      showToast(successMsg || "클립보드에 복사되었습니다!");
    } catch (err) {
      console.error("Copy failed:", err);
      showToast("복사에 실패했습니다.");
    }
  }

  // Load Prompts Data
  async function loadData() {
    try {
      const res = await fetch("./data/prompts.json");
      promptsList = await res.json();
      promptsList.forEach((p) => {
        promptsMap[p.slug] = p;
      });
      loadStorage();
      applyFilter();
      checkHashRoute();
    } catch (e) {
      console.error("Failed to load prompts.json", e);
    }
  }

  // Update Favorite UI
  function updateFavBadges() {
    if (favCountBadge) favCountBadge.textContent = favs.size;
    $$(".card-fav-btn", grid).forEach((btn) => {
      const slug = btn.dataset.fav;
      btn.classList.toggle("active", favs.has(slug));
    });
    if (modalFavToggleBtn && currentPrompt) {
      const isFav = favs.has(currentPrompt.slug);
      modalFavToggleBtn.textContent = isFav ? "★ 즐겨찾기 해제" : "★ 즐겨찾기 추가";
      modalFavToggleBtn.classList.toggle("active", isFav);
    }
  }

  function toggleFav(slug) {
    if (!slug) return;
    if (favs.has(slug)) {
      favs.delete(slug);
      showToast("즐겨찾기에서 제거되었습니다.");
    } else {
      favs.add(slug);
      showToast("즐겨찾기에 추가되었습니다!");
    }
    saveStorage();
    updateFavBadges();
    if (activeCat === "fav") {
      applyFilter();
    }
  }

  // Cart Management
  function updateCartBar() {
    if (!promptCartBar) return;
    const count = cart.size;
    if (count === 0) {
      promptCartBar.classList.add("hidden");
    } else {
      promptCartBar.classList.remove("hidden");
      if (cartCountBadge) cartCountBadge.textContent = count;
      if (cartSectionNames) {
        const names = Array.from(cart)
          .map((s) => promptsMap[s]?.titleKo || s)
          .slice(0, 3)
          .join(", ");
        cartSectionNames.textContent = count > 3 ? `${names} 외 ${count - 3}개` : names;
      }
    }

    if (modalCartToggleBtn && currentPrompt) {
      const inCart = cart.has(currentPrompt.slug);
      modalCartToggleBtn.textContent = inCart ? "✓ 장바구니에서 빼기" : "+ 장바구니에 담기";
      modalCartToggleBtn.classList.toggle("active", inCart);
    }
  }

  function toggleCart(slug) {
    if (!slug) return;
    if (cart.has(slug)) {
      cart.delete(slug);
      showToast("장바구니에서 제외되었습니다.");
    } else {
      cart.add(slug);
      showToast("장바구니에 추가되었습니다! (하단 바 확인)");
    }
    saveStorage();
    updateCartBar();
  }

  function clearCart() {
    cart.clear();
    saveStorage();
    updateCartBar();
    showToast("장바구니가 비워졌습니다.");
  }

  function copyCartMasterPrompt() {
    if (cart.size === 0) return;
    const items = Array.from(cart).map((slug) => promptsMap[slug]).filter(Boolean);

    let prompt = `당신은 최고의 웹 UI/UX 엔지니어이자 풀스택 프론트엔드 개발자입니다.\n`;
    prompt += `Tailwind CSS를 사용하여 아래 ${items.length}개 섹션으로 구성된 모던하고 유기적인 완성형 반응형 랜딩페이지를 제작해주세요.\n\n`;
    prompt += `[핵심 공통 가이드라인]\n`;
    prompt += `1. 일관된 디자인 시스템: 모든 섹션은 통일된 폰트, 세련된 중립 톤 색상 팔레트, 여백 시스템, border-radius를 공유해야 합니다.\n`;
    prompt += `2. 반응형 최적화: 모바일(375px), 태블릿(768px), 데스크톱(1280px+)에서 모두 완벽하게 작동해야 합니다.\n`;
    prompt += `3. 한국어 텍스트: 모든 헤드라인, 본문, 버튼, 폼 레이블을 자연스러운 한국어 카피로 작성해주세요.\n\n`;
    prompt += `[포함될 섹션 상세 명세]\n`;

    items.forEach((item, idx) => {
      prompt += `\n--- 섹션 ${idx + 1}: [${item.catKo}] ${item.titleKo} ---\n`;
      prompt += `${item.promptKo || item.promptEn}\n`;
    });

    copyText(prompt, "통합 랜딩페이지 마스터 프롬프트가 복사되었습니다!");
  }

  // Filter Logic
  function applyFilter() {
    const q = (searchInput ? searchInput.value : "").trim().toLowerCase();
    const cards = $$(".card", grid);
    let visibleCount = 0;
    visibleSlugs = [];

    cards.forEach((card) => {
      const cat = card.dataset.cat;
      const slug = card.dataset.slug;
      const searchBlob = card.dataset.search || "";

      let matchCat = false;
      if (activeCat === "all") {
        matchCat = true;
      } else if (activeCat === "fav") {
        matchCat = favs.has(slug);
      } else {
        matchCat = cat === activeCat;
      }

      const matchText = !q || searchBlob.includes(q);
      const isVisible = matchCat && matchText;

      card.classList.toggle("hidden", !isVisible);
      if (isVisible) {
        visibleCount++;
        visibleSlugs.push(slug);
      }
    });

    if (emptyState) emptyState.classList.toggle("hidden", visibleCount !== 0);
    if (grid) grid.classList.toggle("hidden", visibleCount === 0);

    // Update title & count
    const activeCatLink = $(`.cat[data-cat="${activeCat}"]`);
    const catLabel = activeCatLink ? $(".cat-name", activeCatLink).textContent : "전체";
    if (resultsTitle) resultsTitle.textContent = q ? `검색 결과 ("${q}")` : catLabel;
    if (resultsCount) resultsCount.textContent = `${visibleCount}개 프롬프트`;

    updateFavBadges();
  }

  // Category Click
  if (sideNav) {
    sideNav.addEventListener("click", (e) => {
      const catBtn = e.target.closest(".cat");
      if (!catBtn) return;
      e.preventDefault();

      $$(".cat", sideNav).forEach((c) => c.classList.remove("active"));
      catBtn.classList.add("active");
      activeCat = catBtn.dataset.cat || "all";
      if (grid) grid.dataset.activeCat = activeCat;

      applyFilter();

      if (sidebar) sidebar.classList.remove("nav-open");
    });
  }

  // Search Input
  if (searchInput) {
    searchInput.addEventListener("input", applyFilter);
  }

  // Keyboard Shortcuts
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && document.activeElement !== searchInput && !e.metaKey && !e.ctrlKey) {
      e.preventDefault();
      if (searchInput) searchInput.focus();
    }
    if (e.key === "Escape") {
      closeModal();
    }
    if (modal && !modal.hidden) {
      if (e.key === "ArrowLeft") {
        e.preventDefault();
        navigateModal(-1);
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        navigateModal(1);
      }
    }
  });

  // Sidebar Collapse
  if (collapseBtn && app) {
    collapseBtn.addEventListener("click", () => {
      app.classList.toggle("side-collapsed");
    });
  }

  // Mobile Burger
  if (sideBurger && sidebar) {
    sideBurger.addEventListener("click", () => {
      sidebar.classList.toggle("nav-open");
    });
  }

  // Generate Custom Prompt based on user options
  function buildCustomPrompt(rawPrompt) {
    if (!rawPrompt) return "";
    let finalPrompt = rawPrompt.trim();

    const directives = [];
    if (customFw === "react") {
      directives.push("React (Next.js App Router, Tailwind CSS, lucide-react 아이콘) 컴포넌트로 작성해주세요. TypeScript 인터페이스(Props)를 포함해주세요.");
    } else if (customFw === "vue") {
      directives.push("Vue 3 (Single File Component <template><script setup lang=\"ts\">) 및 Tailwind CSS로 작성해주세요.");
    }

    if (customKoreanUi) {
      directives.push("컴포넌트 내 모든 제목, 안내 문구, 버튼 레이블, 플레이스홀더 텍스트를 자연스럽고 세련된 한국어로 작성해주세요.");
    }

    if (customDarkMode) {
      directives.push("Tailwind CSS의 'dark:' 유틸리티 클래스를 적용하여 라이트 모드와 다크 모드를 모두 완벽하게 지원하도록 스타일링해주세요.");
    }

    if (directives.length > 0) {
      finalPrompt += `\n\n[추가 개발 지시사항]\n` + directives.map((d, i) => `${i + 1}. ${d}`).join("\n");
    }

    return finalPrompt;
  }

  // Render Live Preview Frame
  function renderLivePreview(item) {
    if (!modalPreviewFrame || !item) return;

    const rawHtml = item.code || "";
    const scriptTag = item.script ? `<script>\n${item.script}\n</script>` : "";
    const fontLink = usePretendardInPreview
      ? `<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
         <style>
           body, button, input, select, textarea { font-family: "Pretendard", ui-sans-serif, system-ui, -apple-system, sans-serif !important; }
         </style>`
      : `<style>
           body { font-family: ui-sans-serif, system-ui, -apple-system, sans-serif; }
         </style>`;

    const frameDoc = `<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="https://cdn.tailwindcss.com"></script>
  ${fontLink}
  <style>
    html, body { margin: 0; padding: 0; min-height: 100%; background: #ffffff; }
  </style>
</head>
<body class="p-4 sm:p-6 md:p-8 flex items-center justify-center min-h-screen bg-neutral-50/60">
  <div class="w-full">
    ${rawHtml}
  </div>
  <script>
    var post = function () {
      parent.postMessage(
        { type: "vp-height", height: Math.ceil(document.body.getBoundingClientRect().height) },
        "*"
      );
    };
    addEventListener("load", post);
    new ResizeObserver(post).observe(document.body);
    setTimeout(post, 300);
  </script>
  ${scriptTag}
</body>
</html>`;

    modalPreviewFrame.srcdoc = frameDoc;
  }

  // Handle Resize message from iframe
  window.addEventListener("message", (e) => {
    if (e.data && e.data.type === "vp-height" && e.data.height) {
      if (modalPreviewFrame && modalStageCanvas?.dataset.size === "full") {
        modalPreviewFrame.style.minHeight = Math.max(380, e.data.height + 20) + "px";
      }
    }
  });

  // Open Modal
  function openModal(slug) {
    const item = promptsMap[slug];
    if (!item) return;
    currentPrompt = item;

    // Header info
    modalTitle.textContent = `${item.titleKo} (${item.titleEn})`;
    modalCatBreadcrumb.textContent = item.catKo;
    modalTag.textContent = item.catKo;
    modalPromptTitle.textContent = item.titleKo;
    modalPromptDesc.textContent = `${item.descKo} — [원문: ${item.descEn}]`;

    // Navigation buttons state
    const curIdx = visibleSlugs.indexOf(slug);
    if (modalPrevBtn) modalPrevBtn.disabled = curIdx <= 0;
    if (modalNextBtn) modalNextBtn.disabled = curIdx < 0 || curIdx >= visibleSlugs.length - 1;

    // Favorite & Cart buttons in modal
    updateFavBadges();
    updateCartBar();

    // Panes
    updatePromptPanes();

    // Full combined code snippet
    const combinedCode = item.script
      ? `${item.code}\n\n<!-- JavaScript 동작 스크립트 -->\n<script>\n${item.script}\n</script>`
      : item.code;
    codeSnippetText.textContent = combinedCode;

    // Live preview
    renderLivePreview(item);
    setPreviewSize("full");
    setTab("prompt-ko");

    // Show modal
    modal.hidden = false;
    requestAnimationFrame(() => modal.classList.add("open"));
    document.body.style.overflow = "hidden";

    if (location.hash !== `#${slug}`) {
      history.replaceState(null, "", `#${slug}`);
    }
  }

  // Update Prompt Panes with Customizer applied
  function updatePromptPanes() {
    if (!currentPrompt) return;
    const customKo = buildCustomPrompt(currentPrompt.promptKo || currentPrompt.promptEn);
    panePromptKo.textContent = customKo;
    panePromptEn.textContent = currentPrompt.promptEn;
  }

  // Navigate Modal (Prev / Next)
  function navigateModal(dir) {
    if (!currentPrompt || visibleSlugs.length === 0) return;
    const curIdx = visibleSlugs.indexOf(currentPrompt.slug);
    if (curIdx === -1) return;
    const newIdx = curIdx + dir;
    if (newIdx >= 0 && newIdx < visibleSlugs.length) {
      openModal(visibleSlugs[newIdx]);
    }
  }

  if (modalPrevBtn) modalPrevBtn.addEventListener("click", () => navigateModal(-1));
  if (modalNextBtn) modalNextBtn.addEventListener("click", () => navigateModal(1));

  // Close Modal
  function closeModal() {
    if (!modal || modal.hidden) return;
    modal.classList.remove("open");
    document.body.style.overflow = "";
    setTimeout(() => {
      modal.hidden = true;
      modalPreviewFrame.srcdoc = "";
    }, 250);

    if (location.hash) {
      history.replaceState(null, "", location.pathname + location.search);
    }
  }

  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target.hasAttribute("data-close")) {
        closeModal();
      }
    });
  }

  // Stage Viewport Size Switcher
  function setPreviewSize(size) {
    if (!modalStageCanvas || !modalStageSizes) return;
    $$(".size", modalStageSizes).forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.size === size);
    });
    modalStageCanvas.dataset.size = size;

    if (size === "mobile") {
      modalPreviewFrame.style.width = "375px";
      modalPreviewFrame.style.minHeight = "640px";
    } else if (size === "tablet") {
      modalPreviewFrame.style.width = "768px";
      modalPreviewFrame.style.minHeight = "540px";
    } else {
      modalPreviewFrame.style.width = "100%";
      modalPreviewFrame.style.minHeight = "440px";
    }
  }

  if (modalStageSizes) {
    modalStageSizes.addEventListener("click", (e) => {
      const btn = e.target.closest(".size");
      if (!btn) return;
      setPreviewSize(btn.dataset.size);
    });
  }

  // Font Toggle in Preview
  if (previewFontToggle) {
    previewFontToggle.addEventListener("click", () => {
      usePretendardInPreview = !usePretendardInPreview;
      previewFontToggle.classList.toggle("active", usePretendardInPreview);
      previewFontToggle.textContent = usePretendardInPreview ? "한글 폰트 On" : "기본 폰트";
      if (currentPrompt) renderLivePreview(currentPrompt);
    });
  }

  // Prompt Customizer event listener
  if (promptCustomizer) {
    promptCustomizer.addEventListener("click", (e) => {
      const optChip = e.target.closest(".opt-chip");
      if (optChip) {
        $$(".opt-chip", promptCustomizer).forEach((c) => c.classList.remove("active"));
        optChip.classList.add("active");
        customFw = optChip.dataset.val;
        updatePromptPanes();
        return;
      }

      const optToggle = e.target.closest(".opt-toggle");
      if (optToggle) {
        const toggleType = optToggle.dataset.toggle;
        if (toggleType === "korean-ui") {
          customKoreanUi = !customKoreanUi;
          optToggle.classList.toggle("active", customKoreanUi);
        } else if (toggleType === "dark-mode") {
          customDarkMode = !customDarkMode;
          optToggle.classList.toggle("active", customDarkMode);
        }
        updatePromptPanes();
      }
    });
  }

  // Tab Switcher
  function setTab(tabName) {
    activeTab = tabName;
    $$(".code-tab", modal).forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.tab === tabName);
    });

    panePromptKo.classList.toggle("hidden", tabName !== "prompt-ko");
    panePromptEn.classList.toggle("hidden", tabName !== "prompt-en");
    paneCodeHtml.classList.toggle("hidden", tabName !== "code-html");

    if (modalCopyBtn) {
      if (tabName === "prompt-ko") modalCopyBtn.textContent = "한국어 프롬프트 복사";
      else if (tabName === "prompt-en") modalCopyBtn.textContent = "영문 원본 프롬프트 복사";
      else modalCopyBtn.textContent = "Tailwind 코드 복사";
    }
  }

  const codeTabsContainer = $(".code-tabs", modal);
  if (codeTabsContainer) {
    codeTabsContainer.addEventListener("click", (e) => {
      const tabBtn = e.target.closest(".code-tab");
      if (!tabBtn) return;
      setTab(tabBtn.dataset.tab);
    });
  }

  // Copy Button in Modal
  if (modalCopyBtn) {
    modalCopyBtn.addEventListener("click", () => {
      if (!currentPrompt) return;
      if (activeTab === "prompt-ko") {
        copyText(panePromptKo.textContent, "한국어 프롬프트가 복사되었습니다!");
      } else if (activeTab === "prompt-en") {
        copyText(currentPrompt.promptEn, "영문 원본 프롬프트가 복사되었습니다!");
      } else {
        copyText(codeSnippetText.textContent, "Tailwind CSS 코드가 복사되었습니다!");
      }
    });
  }

  // Modal Favorite & Cart Toggles
  if (modalFavToggleBtn) {
    modalFavToggleBtn.addEventListener("click", () => {
      if (currentPrompt) toggleFav(currentPrompt.slug);
    });
  }
  if (modalCartToggleBtn) {
    modalCartToggleBtn.addEventListener("click", () => {
      if (currentPrompt) toggleCart(currentPrompt.slug);
    });
  }

  // Floating Cart Actions
  if (cartCopyBtn) cartCopyBtn.addEventListener("click", copyCartMasterPrompt);
  if (cartClearBtn) cartClearBtn.addEventListener("click", clearCart);

  // Card Grid Event Delegation
  if (grid) {
    grid.addEventListener("click", (e) => {
      // 1. Favorite Star Button Click
      const favBtn = e.target.closest(".card-fav-btn");
      if (favBtn) {
        e.preventDefault();
        e.stopPropagation();
        toggleFav(favBtn.dataset.fav);
        return;
      }

      // 2. Quick Copy Button Click
      const quickCopyBtn = e.target.closest(".quick-copy-btn");
      if (quickCopyBtn) {
        e.preventDefault();
        e.stopPropagation();
        const slug = quickCopyBtn.dataset.quickCopy;
        const item = promptsMap[slug];
        if (item) {
          copyText(item.promptKo || item.promptEn, `"${item.titleKo}" 프롬프트가 복사되었습니다!`);
          quickCopyBtn.classList.add("copied");
          const copyLabel = $(".quick-copy-text", quickCopyBtn);
          if (copyLabel) copyLabel.textContent = "완료!";
          setTimeout(() => {
            quickCopyBtn.classList.remove("copied");
            if (copyLabel) copyLabel.textContent = "복사";
          }, 1500);
        }
        return;
      }

      // 3. Card click to open modal
      const card = e.target.closest(".card");
      if (!card) return;
      e.preventDefault();
      const slug = card.dataset.slug;
      if (slug) {
        openModal(slug);
      }
    });
  }

  // Hash Route Check
  function checkHashRoute() {
    const hash = location.hash.replace(/^#/, "");
    if (hash && promptsMap[hash]) {
      openModal(hash);
    }
  }

  window.addEventListener("hashchange", checkHashRoute);

  // Initialize
  loadData();
})();
