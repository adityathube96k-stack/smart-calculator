document.addEventListener("DOMContentLoaded", () => {
    const keypad = document.getElementById("calcKeypad");
    const expressionEl = document.getElementById("calcExpression");
    const resultEl = document.getElementById("calcResult");
    const errorEl = document.getElementById("calcError");
    const copyBtn = document.getElementById("copyResultBtn");

    let expression = "";

    function render() {
        expressionEl.textContent = expression || "0";
    }

    async function evaluate() {
        if (!expression) return;
        try {
            const data = await postJSON("/calculate", { expression });
            resultEl.textContent = data.result;
            errorEl.textContent = "";
        } catch (err) {
            errorEl.textContent = err.message;
        }
    }

    keypad.addEventListener("click", (e) => {
        const btn = e.target.closest(".calc-key");
        if (!btn) return;

        const action = btn.dataset.action;
        const value = btn.dataset.value;

        if (action === "clear") {
            expression = "";
            resultEl.textContent = "0";
            errorEl.textContent = "";
        } else if (action === "backspace") {
            expression = expression.slice(0, -1);
        } else if (action === "equals") {
            evaluate();
            return;
        } else if (value) {
            expression += value;
        }

        render();
    });

    document.addEventListener("keydown", (e) => {
        if (/[\d+\-*/.()%]/.test(e.key)) {
            expression += e.key;
            render();
        } else if (e.key === "Enter") {
            evaluate();
        } else if (e.key === "Backspace") {
            expression = expression.slice(0, -1);
            render();
        } else if (e.key === "Escape") {
            expression = "";
            render();
        }
    });

    copyBtn.addEventListener("click", () => copyResult(resultEl.textContent, copyBtn));
});
