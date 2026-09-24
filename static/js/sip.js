document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("calcSipBtn");
    if (!btn) return;

    const monthlyInput = document.getElementById("sipMonthlyInput");
    const rateInput = document.getElementById("sipRateInput");
    const tenureInput = document.getElementById("sipTenureInput");
    const errorEl = document.getElementById("sipError");
    const resultsEl = document.getElementById("sipResults");

    btn.addEventListener("click", async () => {
        if (!validateNumberInput(monthlyInput, errorEl, "Monthly investment")) return;
        if (!validateNumberInput(rateInput, errorEl, "Expected return rate")) return;
        if (!validateNumberInput(tenureInput, errorEl, "Tenure")) return;

        try {
            const data = await postJSON("/sip", {
                monthly_investment: parseFloat(monthlyInput.value),
                annual_rate: parseFloat(rateInput.value),
                tenure_years: parseFloat(tenureInput.value),
            });
            document.getElementById("sipInvested").textContent = data.invested_amount;
            document.getElementById("sipReturns").textContent = data.estimated_returns;
            document.getElementById("sipFutureValue").textContent = data.future_value;
            resultsEl.style.display = "grid";
            errorEl.textContent = "";
        } catch (err) {
            errorEl.textContent = err.message;
        }
    });
});
