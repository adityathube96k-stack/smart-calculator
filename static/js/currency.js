document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("calcCurrencyBtn");
    if (!btn) return;

    const amountInput = document.getElementById("currencyAmountInput");
    const fromInput = document.getElementById("currencyFromInput");
    const toInput = document.getElementById("currencyToInput");
    const errorEl = document.getElementById("currencyError");
    const resultEl = document.getElementById("currencyResult");
    const rateLabel = document.getElementById("currencyRateLabel");

    btn.addEventListener("click", async () => {
        if (!validateNumberInput(amountInput, errorEl, "Amount")) return;
        if (!validateRequired(fromInput, errorEl, "From currency")) return;
        if (!validateRequired(toInput, errorEl, "To currency")) return;

        try {
            const data = await postJSON("/currency", {
                amount: parseFloat(amountInput.value),
                from_currency: fromInput.value.toUpperCase(),
                to_currency: toInput.value.toUpperCase(),
            });
            resultEl.textContent = data.converted;
            rateLabel.textContent = `Rate: ${data.rate}`;
            errorEl.textContent = "";
        } catch (err) {
            errorEl.textContent = err.message;
        }
    });
});
