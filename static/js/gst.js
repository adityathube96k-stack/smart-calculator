document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("calcGstBtn");
    if (!btn) return;

    const amountInput = document.getElementById("gstAmountInput");
    const rateInput = document.getElementById("gstRateInput");
    const modeSelect = document.getElementById("gstModeSelect");
    const errorEl = document.getElementById("gstError");
    const resultsEl = document.getElementById("gstResults");

    btn.addEventListener("click", async () => {
        if (!validateNumberInput(amountInput, errorEl, "Amount")) return;
        if (!validateNumberInput(rateInput, errorEl, "GST rate")) return;

        try {
            const data = await postJSON("/gst", {
                amount: parseFloat(amountInput.value),
                gst_rate: parseFloat(rateInput.value),
                mode: modeSelect.value,
            });
            document.getElementById("gstBase").textContent = data.base_amount;
            document.getElementById("gstAmount").textContent = data.gst_amount;
            document.getElementById("gstTotal").textContent = data.total_amount;
            resultsEl.style.display = "grid";
            errorEl.textContent = "";
        } catch (err) {
            errorEl.textContent = err.message;
        }
    });
});
