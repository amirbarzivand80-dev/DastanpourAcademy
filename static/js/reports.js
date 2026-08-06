const chartMonths = JSON.parse(
    document.getElementById("months-data").textContent
);

const chartTotals = JSON.parse(
    document.getElementById("totals-data").textContent
);


new Chart(
    document.getElementById("incomeChart"),
    {
        type: "line",

        data: {

            labels: chartMonths,

            datasets: [
                {
                    label: "درآمد",

                    data: chartTotals,

                    borderWidth: 3,

                    fill: true,

                    tension: 0.4
                }
            ]
        }
    }
);