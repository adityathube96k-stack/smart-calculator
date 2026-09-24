document.addEventListener("DOMContentLoaded", () => {
    initAgeCalculator();
    initDateDifference();
    initTimeCalculator();
});

function initAgeCalculator() {
    const btn = document.getElementById("calcAgeBtn");
    if (!btn) return;

    const dobInput = document.getElementById("dobInput");
    const birthTimeInput = document.getElementById("birthTimeInput");
    const errorEl = document.getElementById("ageError");
    const resultsEl = document.getElementById("ageResults");

    btn.addEventListener("click", async () => {
        if (!validateRequired(dobInput, errorEl, "Date of birth")) return;

        try {
            const data = await postJSON("/age", {
                date_of_birth: dobInput.value,
                birth_time: birthTimeInput.value || null,
            });

            document.getElementById("ageMain").textContent =
                `${data.years}y ${data.months}m ${data.days}d`;
            document.getElementById("ageWeeks").textContent = data.total_weeks;
            document.getElementById("ageTotalDays").textContent = data.total_days;
            document.getElementById("ageHours").textContent = data.total_hours;
            document.getElementById("ageMinutes").textContent = data.total_minutes;
            document.getElementById("ageDayOfBirth").textContent = data.day_of_birth;
            document.getElementById("ageZodiac").textContent = data.zodiac_sign;
            document.getElementById("ageNextBirthday").textContent = data.next_birthday;
            document.getElementById("ageCountdown").textContent = data.birthday_countdown_days;

            resultsEl.style.display = "block";
            errorEl.textContent = "";
        } catch (err) {
            errorEl.textContent = err.message;
        }
    });
}

function initDateDifference() {
    const btn = document.getElementById("calcDateDiffBtn");
    if (!btn) return;

    const startInput = document.getElementById("startDateInput");
    const endInput = document.getElementById("endDateInput");
    const errorEl = document.getElementById("dateDiffError");
    const resultEl = document.getElementById("dateDiffResult");

    btn.addEventListener("click", async () => {
        if (!validateRequired(startInput, errorEl, "Start date")) return;
        if (!validateRequired(endInput, errorEl, "End date")) return;

        try {
            const data = await postJSON("/date", {
                start_date: startInput.value,
                end_date: endInput.value,
            });
            resultEl.textContent = `${data.total_days} days (${data.total_weeks} weeks, ${data.years} years)`;
            errorEl.textContent = "";
        } catch (err) {
            errorEl.textContent = err.message;
        }
    });
}

function initTimeCalculator() {
    const btn = document.getElementById("calcTimeBtn");
    if (!btn) return;

    const baseInput = document.getElementById("baseTimeInput");
    const hoursInput = document.getElementById("hoursInput");
    const minutesInput = document.getElementById("minutesInput");
    const secondsInput = document.getElementById("secondsInput");
    const opSelect = document.getElementById("timeOpSelect");
    const errorEl = document.getElementById("timeError");
    const resultEl = document.getElementById("timeResult");

    btn.addEventListener("click", async () => {
        if (!validateRequired(baseInput, errorEl, "Base time")) return;

        try {
            const data = await postJSON("/time", {
                base_time: baseInput.value + ":00",
                hours: parseInt(hoursInput.value || 0, 10),
                minutes: parseInt(minutesInput.value || 0, 10),
                seconds: parseInt(secondsInput.value || 0, 10),
                operation: opSelect.value,
            });
            resultEl.textContent = data.result_time;
            errorEl.textContent = "";
        } catch (err) {
            errorEl.textContent = err.message;
        }
    });
}
