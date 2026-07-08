console.log("Script Load");

let chart = null;

async function predictRevenue() {

    const data = {
        seating_capacity: Number(document.getElementById("seating_capacity").value),
        average_meal_price: Number(document.getElementById("average_meal_price").value),
        marketing_budget: Number(document.getElementById("marketing_budget").value),
        social_media_followers: Number(document.getElementById("social_media_followers").value),
        weekend_reservations: Number(document.getElementById("weekend_reservations").value),
        weekday_reservations: Number(document.getElementById("weekday_reservations").value)
    };

    document.getElementById("loader").style.display = "block";
    document.getElementById("result").innerHTML = "";

    try {

        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        document.getElementById("loader").style.display = "none";

        if (response.ok) {

            let start = 0;
            const end = result.predicted_revenue;

            const counter = setInterval(() => {

                start += end / 100;

                if (start >= end) {
                    start = end;
                    clearInterval(counter);

                    const ctx = document.getElementById("revenueChart").getContext("2d");

                    if (chart) chart.destroy();

                    chart = new Chart(ctx, {
                        type: "bar",
                        data: {
                            labels: ["Revenue"],
                            datasets: [{
                                label: "Revenue ₹",
                                data: [end]
                            }]
                        },
                        options: {
                            responsive: true
                        }
                    });
                }

                document.getElementById("result").innerHTML =
                    "💰 Predicted Revenue : ₹ " +
                    start.toLocaleString(undefined, {
                        maximumFractionDigits: 2
                    });

            }, 20);

        }

    } catch (error) {

        document.getElementById("loader").style.display = "none";

        document.getElementById("result").innerHTML =
            "❌ Server Connection Error!";
    }
}