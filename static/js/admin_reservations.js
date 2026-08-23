document.addEventListener("DOMContentLoaded", function () {

    const tableBody = document.querySelector(
        "#reservations-table-body"
    );

    if (!tableBody) {
        return;
    }


    // =========================================
    // گرفتن فیلترهای فعلی صفحه
    // =========================================

    function getFilters() {

        const params = new URLSearchParams();

        const search = document.querySelector(
            'input[name="search"]'
        );

        const barber = document.querySelector(
            'select[name="barber"]'
        );

        const date = document.querySelector(
            'input[name="date"]'
        );


        if (search && search.value) {
            params.set("search", search.value);
        }


        if (barber && barber.value) {
            params.set("barber", barber.value);
        }


        if (date && date.value) {
            params.set("date", date.value);
        }


        // =========================================
        // تشخیص نوبت‌های گذشته
        // =========================================

        const urlParams = new URLSearchParams(
            window.location.search
        );

        if (urlParams.get("past") === "1") {
            params.set("past", "1");
        }


        return params;
    }


    // =========================================
    // دریافت نوبت‌ها
    // =========================================

    async function loadReservations() {

        try {

            const params = getFilters();

            let url =
                "/superadmin/reservations/live/";


            if (params.toString()) {
                url += "?" + params.toString();
            }


            const response = await fetch(
                url,
                {
                    headers: {
                        "X-Requested-With":
                            "XMLHttpRequest"
                    }
                }
            );


            if (!response.ok) {

                throw new Error(
                    "API Error: " +
                    response.status
                );

            }


            const data =
                await response.json();


            updateTable(
                data.reservations
            );


        } catch (error) {

            console.error(
                "خطا در دریافت نوبت‌ها:",
                error
            );

        }

    }


    // =========================================
    // ساخت جدول
    // =========================================

    function updateTable(reservations) {

        tableBody.innerHTML = "";


        // =========================================
        // بدون نوبت
        // =========================================

        if (!reservations.length) {

            tableBody.innerHTML = `

                <tr>

                   <td colspan="11">

                        هنوز هیچ نوبتی ثبت نشده است.

                    </td>

                </tr>

            `;

            return;
        }


        // =========================================
        // ساخت ردیف‌ها
        // =========================================

        reservations.forEach(
            reservation => {

                const row =
                    document.createElement("tr");


                // =========================================
                // وضعیت
                // =========================================

                let pendingSelected = "";
                let approvedSelected = "";
                let doneSelected = "";
                let cancelSelected = "";


                if (
                    reservation.status === "pending"
                ) {

                    pendingSelected = "selected";

                }

                else if (
                    reservation.status === "approved"
                ) {

                    approvedSelected = "selected";

                }

                else if (
                    reservation.status === "done"
                ) {

                    doneSelected = "selected";

                }

                else if (
                    reservation.status === "cancel"
                ) {

                    cancelSelected = "selected";

                }


                // =========================================
                // HTML ردیف
                // =========================================

                row.innerHTML = `

                    <!-- مشتری -->

                    <td>
                        ${reservation.customer_name}
                    </td>


                    <!-- خدمت -->

                    <td>
                        ${reservation.service}
                    </td>


                    <!-- قیمت خدمت -->

                    <td>

                        ${Number(
                            reservation.service_price || 0
                        ).toLocaleString("fa-IR")}

                        تومان

                    </td>


                    <!-- پرداخت شده -->

                    <td>

                        ${Number(
                            reservation.paid_amount || 0
                        ).toLocaleString("fa-IR")}

                        تومان

                    </td>


                    <!-- باقی مانده -->

                    <td>

                        ${Number(
                            reservation.remaining_amount || 0
                        ).toLocaleString("fa-IR")}

                        تومان

                    </td>


                    <!-- آرایشگر -->

                    <td>
                        ${reservation.barber}
                    </td>


                    <!-- تاریخ -->

                    <td>
                        ${reservation.date}
                    </td>


                    <!-- ساعت -->

                    <td>
                        ${reservation.time}
                    </td>


                    <!-- وضعیت -->

                    <td>

                        <form
                            method="POST"
                            action="/superadmin/reservations/${reservation.id}/status/"
                        >

                            <input
                                type="hidden"
                                name="csrfmiddlewaretoken"
                                value="${getCSRFToken()}"
                            >


                            <select name="status">

                                <option
                                    value="pending"
                                    ${pendingSelected}
                                >
                                    در انتظار
                                </option>


                                <option
                                    value="approved"
                                    ${approvedSelected}
                                >
                                    تایید شده
                                </option>


                                <option
                                    value="done"
                                    ${doneSelected}
                                >
                                    انجام شده
                                </option>


                                <option
                                    value="cancel"
                                    ${cancelSelected}
                                >
                                    لغو شده
                                </option>

                            </select>


                            <button
                                type="submit"
                                class="btn-edit"
                            >

                                ذخیره

                            </button>

                        </form>

                    </td>
                    <!-- جزئیات -->

<td>

    <a
       href="/superadmin/reservations/${reservation.id}/detail/"
        class="btn-edit">

        جزئیات

    </a>

</td>


                    <!-- عملیات -->

                    <td>

                        <a
                            href="/superadmin/reservations/${reservation.id}/delete/"
                            class="btn-delete"
                            onclick="
                                return confirm(
                                    'از حذف این نوبت مطمئن هستید؟'
                                )
                            "
                        >

                            حذف

                        </a>

                    </td>

                `;


                tableBody.appendChild(row);

            }
        );

    }


    // =========================================
    // دریافت CSRF
    // =========================================

    function getCSRFToken() {

        const cookie =
            document.cookie
                .split("; ")
                .find(
                    row =>
                        row.startsWith(
                            "csrftoken="
                        )
                );


        if (!cookie) {
            return "";
        }


        return decodeURIComponent(
            cookie.split("=")[1]
        );

    }


    // =========================================
    // اولین اجرا
    // =========================================

    loadReservations();


    // =========================================
    // Live Update
    // =========================================

    setInterval(
        loadReservations,
        5000
    );

});