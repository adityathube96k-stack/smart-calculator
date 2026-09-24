const UNIT_OPTIONS = {
    length: ["mm", "cm", "m", "km", "in", "ft", "yd", "mi"],
    weight: ["mg", "g", "kg", "ton", "oz", "lb"],
    temperature: ["c", "f", "k"],
};

document.addEventListener("DOMContentLoaded", () => {
    const categorySelect = document.getElementById("unitCategorySelect");
    const fromSelect = document.getElementById("unitFromSelect");
    const toSelect = document.getElementById("unitToSelect");
    const valueInput = document.getElementById("unitValueInput");
    const btn = document.getElementById("calcUnitBtn");
    const errorEl = document.getElementById("unitError");
    const resultEl = document.getElementById("unitResult");

    if (!categorySelect) return;

    function populateUnits() {
        const units = UNIT_OPTIONS[categorySelect.value];
        fromSelect.innerHTML = units.map((u) => `<option value="${u}">${u.toUpperCase()}</option>`).join("");
        toSelect.innerHTML = units.map((u) => `<option value="${u}">${u.toUpperCase()}</option>`).join("");
        if (units.length > 1) toSelect.selectedIndex = 1;
    }

    categorySelect.addEventListener("change", populateUnits);
    populateUnits();

    btn.addEventListener("click", async () => {
        if (!validateNumberInput(valueInput, errorEl, "Value")) return;

        try {
            const data = await postJSON("/convert", {
                category: categorySelect.value,
                value: parseFloat(valueInput.value),
                from_unit: fromSelect.value,
                to_unit: toSelect.value,
            });
            resultEl.textContent = data.result;
            errorEl.textContent = "";
        } catch (err) {
            errorEl.textContent = err.message;
        }
    });
});
