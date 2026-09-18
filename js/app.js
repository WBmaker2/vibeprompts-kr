/* ============================================================
   VibePrompt KR — app.js
   한국어 UI 프롬프트 라이브러리 & Tailwind CSS 스니펫
   기능: 실시간 검색 · 카테고리 필터 · 반응형 모달 뷰어 ·
        실시간 라이브 프리뷰(풀스크린/태블릿/모바일) · 
        한국어/영문/코드 탭 전환 및 원클릭 복사 · 해시 라우팅
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

  // Modal elements
  const modal = $("#modal");
  const modalTitle = $("#modalTitle");
  const modalCatBreadcrumb = $("#modalCatBreadcrumb");
  const modalTag = $("#modalTag");
  const modalPromptTitle = $("#modalPromptTitle");
  const modalPromptDesc = $("#modalPromptDesc");
  const modalStageCanvas = $("#modalStageCanvas");
  const modalStageSizes = $("#modalStageSizes");
  const modalPreviewFrame = $("#modalPreviewFrame");
  const modalCopyBtn = $("#modalCopyBtn");
  const panePromptKo = $("#panePromptKo");
  const panePromptEn = $("#panePromptEn");
  const paneCodeHtml = $("#paneCodeHtml");
  const codeSnippetText = $("#codeSnippetText");

  let promptsMap = {};
  let activeCat = "all";
  let activeTab = "prompt-ko";
  let currentPrompt = null;
  let toastTimer = null;

  // Show Toast
  function showToast(msg) {
    if (!toast) return;
    toast.textContent = msg || "클립보드에 복사되었습니다!";
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.classList.remove("show");
    }, 2000);
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
      const list = await res.json();
      list.forEach((p) => {
        promptsMap[p.slug] = p;
      });
      // Check hash route on init
      checkHashRoute();
    } catch (e) {
      console.error("Failed to load prompts.json", e);
    }
  }

  // Filtering Logic
  function applyFilter() {
    const q = (searchInput ? searchInput.value : "").trim().toLowerCase();
    const cards = $$(".card", grid);
    let visibleCount = 0;

    cards.forEach((card) => {
      const cat = card.dataset.cat;
      const searchBlob = card.dataset.search || "";
      const matchCat = activeCat === "all" || cat === activeCat;
      const matchText = !q || searchBlob.includes(q);

      const isVisible = matchCat && matchText;
      card.classList.toggle("hidden", !isVisible);
      if (isVisible) visibleCount++;
    });

    if (emptyState) emptyState.classList.toggle("hidden", visibleCount !== 0);
    if (grid) grid.classList.toggle("hidden", visibleCount === 0);

    // Update title & count
    const activeCatLink = $(`.cat[data-cat="${activeCat}"]`);
    const catLabel = activeCatLink ? $(".cat-name", activeCatLink).textContent : "전체";
    if (resultsTitle) resultsTitle.textContent = q ? `검색 결과 ("${q}")` : catLabel;
    if (resultsCount) resultsCount.textContent = `${visibleCount}개 프롬프트`;
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

      // Close mobile menu if open
      if (sidebar) sidebar.classList.remove("nav-open");
    });
  }

  // Search Input
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      applyFilter();
    });
  }

  // "/" Shortcut to focus search
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && document.activeElement !== searchInput && !e.metaKey && !e.ctrlKey) {
      e.preventDefault();
      if (searchInput) searchInput.focus();
    }
    if (e.key === "Escape") {
      closeModal();
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

    // Pane contents
    panePromptKo.textContent = item.promptKo || item.promptEn;
    panePromptEn.textContent = item.promptEn;
    codeSnippetText.textContent = item.code;

    // Set Live Preview iframe
    const rawHtml = item.code || "";
    const frameDoc = `<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    html, body { margin: 0; padding: 0; min-height: 100%; background: #ffffff; }
    body { font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
  </style>
</head>
<body class="p-4 sm:p-6 md:p-8 flex items-center justify-center min-h-screen bg-neutral-50/60">
  <div class="w-full">
    ${rawHtml}
  </div>
</body>
</html>`;
    modalPreviewFrame.srcdoc = frameDoc;

    // Reset viewport size to Full
    setPreviewSize("full");

    // Reset tab to Korean prompt
    setTab("prompt-ko");

    // Show modal
    modal.hidden = false;
    requestAnimationFrame(() => modal.classList.add("open"));
    document.body.style.overflow = "hidden";

    // Update URL hash without scrolling
    if (location.hash !== `#${slug}`) {
      history.replaceState(null, "", `#${slug}`);
    }
  }

  // Close Modal
  function closeModal() {
    if (!modal || modal.hidden) return;
    modal.classList.remove("open");
    document.body.style.overflow = "";
    setTimeout(() => {
      modal.hidden = true;
      modalPreviewFrame.srcdoc = "";
    }, 250);

    // Clear hash
    if (location.hash) {
      history.replaceState(null, "", location.pathname + location.search);
    }
  }

  // Close handlers
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
      else if (tabName === "prompt-en") modalCopyBtn.textContent = "영문 프롬프트 복사";
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
        copyText(currentPrompt.promptKo || currentPrompt.promptEn, "한국어 프롬프트가 복사되었습니다!");
      } else if (activeTab === "prompt-en") {
        copyText(currentPrompt.promptEn, "영문 원본 프롬프트가 복사되었습니다!");
      } else {
        copyText(currentPrompt.code, "Tailwind CSS 코드가 복사되었습니다!");
      }
    });
  }

  // Card Click delegation
  if (grid) {
    grid.addEventListener("click", (e) => {
      const card = e.target.closest(".card");
      if (!card) return;
      e.preventDefault();
      const slug = card.dataset.slug;
      if (slug) {
        openModal(slug);
      }
    });
  }

  // Check Hash Route
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
