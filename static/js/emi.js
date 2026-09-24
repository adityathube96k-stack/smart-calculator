document.addEventListener("DOMContentLoaded", () => {
    initEmi();
    initLoan();
});

function initEmi() {
    const btn = document.getElementById("calcEmiBtn");
    if (!btn) return;

    const principalInput = document.getElementById("emiPrincipalInput");
    const rateInput = document.getElementById("emiRateInput");
    const tenureInput = document.getElementById("emiTenureInput");
    const errorEl = document.getElementById("emiError");
    const resultsEl = document.getElementById("emiResults");

    btn.addEventListener("click", async () => {
        if (!validateNumberInput(principalInput, errorEl, "Loan amount")) return;
        if (!validateNumberInput(rateInput, errorEl, "Interest rate")) return;
        if (!validateNumberInput(tenureInput, errorEl, "Tenure")) return;

        try {
            const data = await postJSON("/emi", {
                principal: parseFloat(principalInput.value),
                annual_rate: parseFloat(rateInput.value),
                tenure_months: parseFloat(tenureInput.value),
            });
            document.getElementById("emiValue").textContent = data.emi;
            document.getElementById("emiInterest").textContent = data.total_interest;
            document.getElementById("emiTotal").textContent = data.total_payment;
            resultsEl.style.display = "grid";
            errorEl.textContent = "";
        } catch (err) {
            errorEl.textContent = err.message;
        }
    });
}

function initLoan() {
    const btn = document.getElementById("calcLoanBtn");
    if (!btn) return;

    const principalInput = document.getElementById("loanPrincipalInput");
    const rateInput = document.getElementById("loanRateInput");
    const tenureInput = document.getElementById("loanTenureInput");
    const errorEl = document.getElementById("loanError");
    const resultsEl = document.getElementById("loanResults");

    btn.addEventListener("click", async () => {
        if (!validateNumberInput(principalInput, errorEl, "Loan amount")) return;
        if (!validateNumberInput(rateInput, errorEl, "Interest rate")) return;
        if (!validateNumberInput(tenureInput, errorEl, "Tenure")) return;

        try {
            const data = await postJSON("/loan", {
                principal: parseFloat(principalInput.value),
                annual_rate: parseFloat(rateInput.value),
                tenure_years: parseFloat(tenureInput.value),
            });
            document.getElementById("loanInterest").textContent = data.total_interest;
            document.getElementById("loanPayable").textContent = data.total_payable;
            document.getElementById("loanMonthly").textContent = data.monthly_payment;
            resultsEl.style.display = "grid";
            errorEl.textContent = "";
        } catch (err) {
            errorEl.textContent = err.message;
        }
    });
}
