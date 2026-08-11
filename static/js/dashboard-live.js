document.addEventListener("DOMContentLoaded", function () {

    const refreshDashboard = async () => {

        try {

            const response = await fetch("/superadmin/reservations/live/");

            if (!response.ok) {
                return;
            }

            const data = await response.json();

            const tbody = document.querySelector(
                ".dashboard-box table tbody"
            );

            if (!tbody) {
                return;
            }

            tbody.innerHTML = "";

            if (!data.reservations.length) {

                tbody.innerHTML = `
                    <tr>
                        <td colspan="6">
                            هنوز رزروی ثبت نشده است.
                        </td>
                    </tr>
                `;

                return;
            }

            data.reservations.slice(0, 8).forEach(function (reservation) {

                const statusMap = {
                    pending: "در انتظار پرداخت",
                    approved: "تایید شده",
                    done: "انجام شده",
                    cancel: "لغو شده"
                };

                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${reservation.customer_name}</td>
                    <td>${reservation.service}</td>
                    <td>${reservation.barber}</td>
                    <td>${reservation.date}</td>
                    <td>${reservation.time}</td>
                    <td>${statusMap[reservation.status] || reservation.status}</td>
                `;

                tbody.appendChild(row);

            });

        } catch (error) {

            console.error(
                "خطا در بروزرسانی نوبت‌های داشبورد:",
                error
            );

        }

    };

    // اولین بار بلافاصله اجرا شود
    refreshDashboard();

    // هر 5 ثانیه بروزرسانی شود
    setInterval(refreshDashboard, 5000);

});