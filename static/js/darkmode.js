(function () {
    const root = document.documentElement;
    const stored = localStorage.getItem("theme");
    if (stored) root.setAttribute("data-theme", stored);

    document.addEventListener("DOMContentLoaded", () => {
        const toggle = document.getElementById("themeToggle");
        if (!toggle) return;

        toggle.addEventListener("click", () => {
            const current = root.getAttribute("data-theme") || "light";
            const next = current === "light" ? "dark" : "light";
            root.setAttribute("data-theme", next);
            localStorage.setItem("theme", next);
        });
    });
})();
