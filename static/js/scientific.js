document.addEventListener("DOMContentLoaded", () => {
    const keypad = document.getElementById("sciKeypad");
    const valueInput = document.getElementById("sciValue");
    const value2Input = document.getElementById("sciValue2");
    const value2Field = document.getElementById("sciValue2Field");
    const resultEl = document.getElementById("sciResult");
    const opLabel = document.getElementById("sciOpLabel");
    const errorEl = document.getElementById("sciError");
    const copyBtn = document.getElementById("copyResultBtn");

    keypad.addEventListener("click", async (e) => {
        const btn = e.target.closest(".calc-key");
        if (!btn) return;
        const operation = btn.dataset.op;

        value2Field.style.display = operation === "power" ? "block" : "none";

        const payload = {
            operation,
            value: valueInput.value ? parseFloat(valueInput.value) : 0,
        };
        if (operation === "power") {
            payload.value2 = value2Input.value ? parseFloat(value2Input.value) : undefined;
        }

        try {
            const data = await postJSON("/scientific", payload);
            resultEl.textContent = data.result;
            opLabel.textContent = data.expression;
            errorEl.textContent = "";
        } catch (err) {
            errorEl.textContent = err.message;
        }
    });

    copyBtn.addEventListener("click", () => copyResult(resultEl.textContent, copyBtn));
});
