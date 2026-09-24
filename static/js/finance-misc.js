document.addEventListener("DOMContentLoaded", () => {
    initDiscount();
    initProfitLoss();
    initPercentage();
});

function initDiscount() {
    const btn = document.getElementById("calcDiscountBtn");
    if (!btn) return;

    const priceInput = document.getElementById("discountPriceInput");
    const percentInput = document.getElementById("discountPercentInput");
    const errorEl = document.getElementById("discountError");
    const resultsEl = document.getElementById("discountResults");

    btn.addEventListener("click", async () => {
        if (!validateNumberInput(priceInput, errorEl, "Original price")) return;
        if (!validateNumberInput(percentInput, errorEl, "Discount percent")) return;

        try {
            const data = await postJSON("/discount", {
                original_price: parseFloat(priceInput.value),
                discount_percent: parseFloat(percentInput.value),
            });
            document.getElementById("discountAmount").textContent = data.discount_amount;
            document.getElementById("discountFinal").textContent = data.final_price;
            resultsEl.style.display = "grid";
            errorEl.textContent = "";
        } catch (err) {
            errorEl.textContent = err.message;
        }
    });
}

function initProfitLoss() {
    const btn = document.getElementById("calcPlBtn");
    if (!btn) return;

    const costInput = document.getElementById("costPriceInput");
    const sellingInput = document.getElementById("sellingPriceInput");
    const errorEl = document.getElementById("plError");
    const panel = document.getElementById("plResultPanel");

    btn.addEventListener("click", async () => {
        if (!validateNumberInput(costInput, errorEl, "Cost price")) return;
        if (!validateNumberInput(sellingInput, errorEl, "Selling price")) return;

        try {
            const data = await postJSON("/profit-loss", {
                cost_price: parseFloat(costInput.value),
                selling_price: parseFloat(sellingInput.value),
            });
            const typeLabel = document.getElementById("plType");
            typeLabel.textContent = data.type.toUpperCase();
            document.getElementById("plAmount").textContent = data.amount;
            document.getElementById("plPercent").textContent = `${data.percent}%`;
            panel.style.display = "block";
            errorEl.textContent = "";
        } catch (err) {
            errorEl.textContent = err.message;
        }
    });
}

function initPercentage() {
    const btn = document.getElementById("calcPctBtn");
    if (!btn) return;

    const valueInput = document.getElementById("pctValueInput");
    const percentInput = document.getElementById("pctPercentInput");
    const errorEl = document.getElementById("pctError");
    const resultEl = document.getElementById("pctResult");

    btn.addEventListener("click", async () => {
        if (!validateNumberInput(valueInput, errorEl, "Value")) return;
        if (!validateNumberInput(percentInput, errorEl, "Percent")) return;

        try {
            const data = await postJSON("/percentage", {
                value: parseFloat(valueInput.value),
                percent: parseFloat(percentInput.value),
            });
            resultEl.textContent = data.result;
            errorEl.textContent = "";
        } catch (err) {
            errorEl.textContent = err.message;
        }
    });
}
