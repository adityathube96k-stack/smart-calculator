/** Returns true and clears error state if valid; otherwise shows message and returns false. */
function validateNumberInput(inputEl, errorEl, fieldLabel) {
    const value = parseFloat(inputEl.value);
    if (inputEl.value.trim() === "" || Number.isNaN(value)) {
        showFieldError(errorEl, `${fieldLabel} must be a valid number.`);
        return false;
    }
    clearFieldError(errorEl);
    return true;
}

function validateRequired(inputEl, errorEl, fieldLabel) {
    if (!inputEl.value || inputEl.value.trim() === "") {
        showFieldError(errorEl, `${fieldLabel} is required.`);
        return false;
    }
    clearFieldError(errorEl);
    return true;
}

function showFieldError(errorEl, message) {
    if (!errorEl) return;
    errorEl.textContent = message;
}

function clearFieldError(errorEl) {
    if (!errorEl) return;
    errorEl.textContent = "";
}
