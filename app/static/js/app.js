const startDateInput = document.getElementById("startDate");
const endDateInput = document.getElementById("endDate");

const loadButton = document.getElementById("loadButton");

const statusElement = document.getElementById("status");
const spinnerElement = document.getElementById("spinner");
const resultsElement = document.getElementById("results");

function getYesterdayDate() {
    const yesterday = new Date();

    yesterday.setDate(yesterday.getDate() - 1);

    return yesterday.toISOString().split("T")[0];
}

function setDefaultDates() {
    const yesterday = getYesterdayDate();

    startDateInput.value = yesterday;
    endDateInput.value = yesterday;
}

function setLoading(isLoading) {
    loadButton.disabled = isLoading;
    spinnerElement.classList.toggle("visible", isLoading);

    if (isLoading) {
        statusElement.textContent = "Loading weather data...";
    }
}
function createRow(item, index) {
    const row = document.createElement("tr");

    row.innerHTML = `
        <td>${index + 1}</td>
        <td>${item.city}</td>
        <td>${item.country}</td>
        <td>${item.score}</td>
    `;

    return row;
}

function renderResults(data) {
    resultsElement.innerHTML = "";

    data.forEach((item, index) => {
        resultsElement.appendChild(
            createRow(item, index),
        );
    });
}

async function loadData() {
    setLoading(true);
    resultsElement.innerHTML = "";

    const params = new URLSearchParams({
        start_date: startDateInput.value,
        end_date: endDateInput.value,
    });

    try {
        const response = await fetch(
            `/api/v1/cities-scores?${params.toString()}`
        );

        let data = null;

        try {
            data = await response.json();
        } catch {
            data = null;
        }

        if (!response.ok) {
            const errorMessage =
                data?.detail ||
                "Failed to load weather data. Please try again later.";

            throw new Error(errorMessage);
        }

        renderResults(data);
        statusElement.textContent = "";
    } catch (error) {
        resultsElement.innerHTML = "";
        statusElement.textContent = error.message;
    } finally {
        setLoading(false);
    }
}

loadButton.addEventListener(
    "click",
    loadData,
);

setDefaultDates();