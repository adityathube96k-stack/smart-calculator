document.addEventListener("DOMContentLoaded", () => {
    // Mobile nav toggle
    const navToggle = document.getElementById("navToggle");
    const navLinks = document.getElementById("navLinks");
    if (navToggle && navLinks) {
        navToggle.addEventListener("click", () => {
            const isOpen = navLinks.classList.toggle("is-open");
            navToggle.setAttribute("aria-expanded", isOpen);
        });
    }

    // Mobile dropdown toggle (finance menu)
    document.querySelectorAll(".navbar__dropdown-toggle").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            if (window.innerWidth > 768) return;
            e.preventDefault();
            btn.closest(".navbar__dropdown").classList.toggle("is-open");
        });
    });
});

/** Copy a result value to the clipboard. Used by "Copy Result" buttons. */
function copyResult(value, buttonEl) {
    navigator.clipboard.writeText(String(value)).then(() => {
        if (!buttonEl) return;
        const original = buttonEl.textContent;
        buttonEl.textContent = "Copied!";
        setTimeout(() => { buttonEl.textContent = original; }, 1500);
    });
}

/** Shared POST helper for calculator API calls. Returns parsed JSON or throws with a message. */
async function postJSON(url, payload) {
    const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!data.success) {
        throw new Error(data.error || "Something went wrong.");
    }
    return data.data;
}
