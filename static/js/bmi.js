document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("calcBmiBtn");
    if (!btn) return;

    const weightInput = document.getElementById("weightInput");
    const heightInput = document.getElementById("heightInput");
    const errorEl = document.getElementById("bmiError");
    const resultEl = document.getElementById("bmiResult");
    const categoryEl = document.getElementById("bmiCategory");

    btn.addEventListener("click", async () => {
        if (!validateNumberInput(weightInput, errorEl, "Weight")) return;
        if (!validateNumberInput(heightInput, errorEl, "Height")) return;

        try {
            const data = await postJSON("/bmi", {
                weight_kg: parseFloat(weightInput.value),
                height_cm: parseFloat(heightInput.value),
            });
            resultEl.textContent = data.bmi;
            categoryEl.textContent = data.category;
            errorEl.textContent = "";
        } catch (err) {
            errorEl.textContent = err.message;
        }
    });
});
