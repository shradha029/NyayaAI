document.addEventListener("DOMContentLoaded", () => {
  // ---------------------------------------------------------------
  // Elements
  // ---------------------------------------------------------------
  const navToggle = document.getElementById("navToggle");
  const navLinks = document.getElementById("navLinks");

  const questionInput = document.getElementById("questionInput");
  const charCount = document.getElementById("charCount");
  const askBtn = document.getElementById("askBtn");
  const statusArea = document.getElementById("statusArea");
  const statusText = document.getElementById("statusText");
  const errorArea = document.getElementById("errorArea");
  const responseArea = document.getElementById("responseArea");

  const MAX_LEN = 1500;

  // ---------------------------------------------------------------
  // Mobile nav toggle
  // ---------------------------------------------------------------
  navToggle.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });

  navLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });

  // ---------------------------------------------------------------
  // Character counter
  // ---------------------------------------------------------------
  function updateCharCount() {
    const len = questionInput.value.length;
    charCount.textContent = `${len} / ${MAX_LEN}`;
    charCount.style.color = len > MAX_LEN ? "#b3261e" : "";
  }
  questionInput.addEventListener("input", updateCharCount);
  updateCharCount();

  // ---------------------------------------------------------------
  // Example chips + category cards fill the textarea
  // ---------------------------------------------------------------
  function fillQuestion(text) {
    questionInput.value = text;
    updateCharCount();
    document.getElementById("ask").scrollIntoView({ behavior: "smooth", block: "start" });
    questionInput.focus();
  }

  document.querySelectorAll(".example-chip").forEach((chip) => {
    chip.addEventListener("click", () => fillQuestion(chip.textContent.trim()));
  });

  document.querySelectorAll(".category-card").forEach((card) => {
    card.addEventListener("click", () => fillQuestion(card.dataset.question || ""));
  });

  // ---------------------------------------------------------------
  // Ask NyayaAI
  // ---------------------------------------------------------------
  const SECTION_META = [
    { key: "understanding", icon: "🔎", title: "Understanding Your Situation" },
    { key: "legalInfo", icon: "⚖️", title: "Relevant Legal Information" },
    { key: "nextSteps", icon: "✅", title: "Possible Next Steps" },
    { key: "documents", icon: "📄", title: "Documents / Evidence You May Need" },
    { key: "seekHelp", icon: "🚨", title: "When You Should Seek Professional Help" },
    { key: "sources", icon: "📚", title: "Sources / References" },
  ];

  function setLoading(isLoading) {
    askBtn.disabled = isLoading;
    askBtn.textContent = isLoading ? "Analyzing…" : "Get Legal Guidance";
    statusArea.hidden = !isLoading;
    if (isLoading) statusText.textContent = "Analyzing your question…";
  }

  function showError(message) {
    errorArea.textContent = message;
    errorArea.hidden = false;
  }

  function clearError() {
    errorArea.hidden = true;
    errorArea.textContent = "";
  }

  function renderList(text) {
    const lines = text
      .split("\n")
      .map((l) => l.trim())
      .filter(Boolean);

    const bulletLines = lines.filter((l) => l.startsWith("-") || l.startsWith("•"));

    if (bulletLines.length >= 1 && bulletLines.length === lines.length) {
      const items = bulletLines.map((l) => l.replace(/^[-•]\s*/, ""));
      const ul = document.createElement("ul");
      items.forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        ul.appendChild(li);
      });
      return ul;
    }

    const p = document.createElement("p");
    p.textContent = text;
    return p;
  }

  function renderResponse(answer) {
    responseArea.innerHTML = "";

    SECTION_META.forEach(({ key, icon, title }) => {
      const content = (answer[key] || "").trim();
      if (!content) return;

      const card = document.createElement("div");
      card.className = "resp-card";
      if (key === "seekHelp") card.classList.add("seek-help");
      if (key === "sources") card.classList.add("sources");

      const heading = document.createElement("h4");
      heading.textContent = `${icon} ${title}`;
      card.appendChild(heading);
      card.appendChild(renderList(content));

      responseArea.appendChild(card);
    });

    const note = document.createElement("p");
    note.className = "disclaimer-inline";
    note.textContent = "This is general legal information, not professional legal advice. Please verify with an official source or a qualified lawyer.";
    responseArea.appendChild(note);

    responseArea.hidden = false;
    responseArea.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  async function askNyayaAI() {
    clearError();
    responseArea.hidden = true;
    responseArea.innerHTML = "";

    const question = questionInput.value.trim();

    if (!question) {
      showError("Please describe your situation before submitting.");
      return;
    }

    if (question.length > MAX_LEN) {
      showError(`Please limit your question to ${MAX_LEN} characters.`);
      return;
    }

    setLoading(true);

    try {
      const res = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      let data;
      try {
        data = await res.json();
      } catch {
        throw new Error("Received an unexpected response from the server.");
      }

      if (!res.ok || !data.success) {
        throw new Error(data.error || "Something went wrong. Please try again.");
      }

      renderResponse(data.answer);
    } catch (err) {
      showError(err.message || "NyayaAI could not process your request. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  askBtn.addEventListener("click", askNyayaAI);

  questionInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
      askNyayaAI();
    }
  });
});
