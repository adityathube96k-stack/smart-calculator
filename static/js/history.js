document.addEventListener("DOMContentLoaded", () => {
    const clearBtn = document.getElementById("clearHistoryBtn");
    if (!clearBtn) return;

    clearBtn.addEventListener("click", async () => {
        if (!confirm("Clear all saved history? This can't be undone.")) return;

        try {
            await postJSON("/history/clear", {});
            window.location.reload();
        } catch (err) {
            alert(err.message);
        }
    });
});
