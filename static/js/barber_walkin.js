document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // عناصر صفحه
    // =========================

    const openCalendar =
        document.getElementById("openCalendar");

    const calendarModal =
        document.getElementById("calendarModal");

    const calendar =
        document.getElementById("calendar-days");

    const calendarTitle =
        document.getElementById("calendarTitle");

    const prevMonth =
        document.getElementById("prevMonth");

    const nextMonth =
        document.getElementById("nextMonth");

    const selectedDate =
        document.getElementById("selectedDate");

    const hiddenDate =
        document.getElementById("hiddenDate");

    const timeGrid =
        document.getElementById("timeGrid");

    const hiddenTime =
        document.getElementById("hiddenTime");

    // اگر کاربر ادمین باشد این وجود دارد
    const barberSelect =
        document.getElementById("barber-select");


    // =========================
    // بررسی عناصر
    // =========================

    if (
        !openCalendar ||
        !calendarModal ||
        !calendar ||
        !calendarTitle ||
        !prevMonth ||
        !nextMonth ||
        !selectedDate ||
        !hiddenDate ||
        !timeGrid ||
        !hiddenTime
    ) {

        console.error(
            "عناصر تقویم پیدا نشدند."
        );

        return;
    }


    // =========================
    // بررسی Jalaali
    // =========================

    if (!window.jalaali) {

        console.error(
            "JALAALI NOT FOUND"
        );

        return;
    }


    // =========================
    // تاریخ امروز
    // =========================

    const now = new Date();

    const todayJalali =
        window.jalaali.toJalaali(
            now.getFullYear(),
            now.getMonth() + 1,
            now.getDate()
        );


    let viewYear =
        todayJalali.jy;

    let viewMonth =
        todayJalali.jm;


    // =========================
    // نام ماه‌ها
    // =========================

    const monthNames = [

        "",

        "فروردین",
        "اردیبهشت",
        "خرداد",
        "تیر",
        "مرداد",
        "شهریور",
        "مهر",
        "آبان",
        "آذر",
        "دی",
        "بهمن",
        "اسفند"

    ];


    // =====================================================
    // گرفتن آرایشگر انتخاب شده
    // =====================================================

    function getSelectedBarber() {

        // اگر select وجود نداشته باشد
        // یعنی کاربر آرایشگر است
        if (!barberSelect) {

            return "";

        }

        return barberSelect.value;

    }


    // =====================================================
    // بررسی انتخاب آرایشگر
    // =====================================================

    function checkBarberSelected() {

        // آرایشگر خودش انتخاب شده
        if (!barberSelect) {

            return true;

        }

        if (!barberSelect.value) {

            alert(
                "لطفاً ابتدا آرایشگر را انتخاب کنید."
            );

            return false;

        }

        return true;

    }


    // =========================
    // ساخت تقویم
    // =========================

    function renderCalendar() {

        calendar.innerHTML = "";

        calendarTitle.innerText =
            monthNames[viewMonth] +
            " " +
            viewYear;


        const monthDays =
            window.jalaali.jalaaliMonthLength(
                viewYear,
                viewMonth
            );


        const firstGregorian =
            window.jalaali.toGregorian(
                viewYear,
                viewMonth,
                1
            );


        const firstDate =
            new Date(
                firstGregorian.gy,
                firstGregorian.gm - 1,
                firstGregorian.gd
            );


        let startDay =
            firstDate.getDay();


        startDay =
            (startDay + 1) % 7;


        // =========================
        // خانه‌های خالی
        // =========================

        for (
            let i = 0;
            i < startDay;
            i++
        ) {

            const empty =
                document.createElement(
                    "div"
                );

            empty.className =
                "calendar-day empty";

            calendar.appendChild(
                empty
            );

        }


        // =========================
        // روزهای ماه
        // =========================

        for (
            let day = 1;
            day <= monthDays;
            day++
        ) {

            const dayBox =
                document.createElement(
                    "div"
                );

            dayBox.className =
                "calendar-day";

            dayBox.innerText =
                day;


            const gregorian =
                window.jalaali.toGregorian(
                    viewYear,
                    viewMonth,
                    day
                );


            const selected =
                new Date(
                    gregorian.gy,
                    gregorian.gm - 1,
                    gregorian.gd
                );


            const today =
                new Date();

            today.setHours(
                0,
                0,
                0,
                0
            );


            // =========================
            // روزهای گذشته
            // =========================

            if (selected < today) {

                dayBox.classList.add(
                    "disabled"
                );

            }

            else {

                dayBox.addEventListener(
                    "click",
                    function () {

                        // =========================
                        // انتخاب روز
                        // =========================

                        document
                            .querySelectorAll(
                                ".calendar-day"
                            )
                            .forEach(
                                function (item) {

                                    item.classList.remove(
                                        "active"
                                    );

                                }
                            );


                        dayBox.classList.add(
                            "active"
                        );


                        // =========================
                        // نمایش تاریخ شمسی
                        // =========================

                        selectedDate.innerText =

                            viewYear +
                            "/" +
                            String(
                                viewMonth
                            ).padStart(2, "0") +
                            "/" +
                            String(
                                day
                            ).padStart(2, "0");


                        // =========================
                        // تاریخ میلادی برای Django
                        // =========================

                        hiddenDate.value =

                            gregorian.gy +
                            "-" +
                            String(
                                gregorian.gm
                            ).padStart(2, "0") +
                            "-" +
                            String(
                                gregorian.gd
                            ).padStart(2, "0");


                        // =========================
                        // بستن تقویم
                        // =========================

                        calendarModal.style.display =
                            "none";


                        // =========================
                        // ساخت ساعت‌ها
                        // =========================

                        createTimes(
                            hiddenDate.value
                        );

                    }
                );

            }


            calendar.appendChild(
                dayBox
            );

        }

    }


    // =====================================================
    // گرفتن ساعت‌های پر از Django
    // =====================================================

    async function getBusyTimes(date) {

        try {

            const barberId =
                getSelectedBarber();


            // =========================
            // اگر ادمین است
            // =========================

            if (
                barberSelect &&
                !barberId
            ) {

                return [];

            }


            // =========================
            // ساخت URL
            // =========================

            let url =

                `/superadmin/barber-walkin/busy-times/?date=${encodeURIComponent(date)}`;


            // اگر آرایشگر انتخاب شده
            // شناسه آن را هم بفرست

            if (barberId) {

                url +=
                    `&barber_id=${encodeURIComponent(barberId)}`;

            }


            console.log(
                "BUSY TIMES URL:",
                url
            );


            const response =
                await fetch(url);


            if (!response.ok) {

                console.error(
                    "خطا در دریافت ساعت‌های پر"
                );

                return [];

            }


            const busyTimes =
                await response.json();


            console.log(
                "BUSY TIMES:",
                busyTimes
            );


            return busyTimes;


        }

        catch (error) {

            console.error(
                "BUSY TIMES ERROR:",
                error
            );

            return [];

        }

    }


    // =====================================================
    // ساخت ساعت‌ها
    // =====================================================

    async function createTimes(date) {

        timeGrid.innerHTML = "";

        hiddenTime.value = "";


        // =========================
        // بررسی آرایشگر
        // =========================

        if (!checkBarberSelected()) {

            timeGrid.innerHTML = `

                <p>
                    ابتدا آرایشگر را انتخاب کنید.
                </p>

            `;

            return;

        }


        // =========================
        // پیام بارگذاری
        // =========================

        timeGrid.innerHTML = `

            <p>
                در حال بررسی ساعت‌های آزاد...
            </p>

        `;


        const busyTimes =
            await getBusyTimes(date);


        timeGrid.innerHTML = "";


        let availableCount = 0;


        // =========================
        // ساعت ۹ تا ۲۱
        // =========================

        for (
            let hour = 9;
            hour < 21;
            hour++
        ) {

            for (
                let minute of [0, 30]
            ) {

                const time =

                    String(hour)
                        .padStart(2, "0") +

                    ":" +

                    String(minute)
                        .padStart(2, "0");


                // =========================
                // ساعت رزرو شده
                // =========================

                if (
                    busyTimes.includes(time)
                ) {

                    continue;

                }


                availableCount++;


                const button =
                    document.createElement(
                        "button"
                    );


                button.type =
                    "button";


                button.className =
                    "time-btn";


                button.innerText =
                    time;


                button.addEventListener(
                    "click",
                    function () {

                        document
                            .querySelectorAll(
                                ".time-btn"
                            )
                            .forEach(
                                function (btn) {

                                    btn.classList.remove(
                                        "active"
                                    );

                                }
                            );


                        button.classList.add(
                            "active"
                        );


                        hiddenTime.value =
                            time;


                        console.log(
                            "SELECTED TIME:",
                            time
                        );

                    }
                );


                timeGrid.appendChild(
                    button
                );

            }

        }


        // =========================
        // هیچ ساعت آزادی نیست
        // =========================

        if (
            availableCount === 0
        ) {

            timeGrid.innerHTML = `

                <p>
                    برای این تاریخ ساعت آزادی وجود ندارد.
                </p>

            `;

        }

    }


    // =====================================================
    // تغییر آرایشگر
    // =====================================================

    if (barberSelect) {

        barberSelect.addEventListener(
            "change",
            function () {

                // پاک کردن تاریخ
                hiddenDate.value = "";

                selectedDate.innerText =
                    "برای انتخاب تاریخ کلیک کنید";


                // پاک کردن ساعت
                hiddenTime.value = "";

                timeGrid.innerHTML = `

                    <p>
                        ابتدا تاریخ را انتخاب کنید.
                    </p>

                `;


                console.log(
                    "SELECTED BARBER:",
                    barberSelect.value
                );

            }
        );

    }


    // =====================================================
    // باز کردن تقویم
    // =====================================================

    openCalendar.addEventListener(
        "click",
        function () {

            // اگر ادمین است
            // اول آرایشگر باید انتخاب شود

            if (
                !checkBarberSelected()
            ) {

                return;

            }


            calendarModal.style.display =
                "flex";


            renderCalendar();

        }
    );


    // =====================================================
    // ماه قبل
    // =====================================================

    prevMonth.addEventListener(
        "click",
        function (e) {

            e.preventDefault();


            viewMonth--;


            if (
                viewMonth < 1
            ) {

                viewMonth = 12;

                viewYear--;

            }


            renderCalendar();

        }
    );


    // =====================================================
    // ماه بعد
    // =====================================================

    nextMonth.addEventListener(
        "click",
        function (e) {

            e.preventDefault();


            viewMonth++;


            if (
                viewMonth > 12
            ) {

                viewMonth = 1;

                viewYear++;

            }


            renderCalendar();

        }
    );


    // =====================================================
    // بستن تقویم
    // =====================================================

    window.addEventListener(
        "click",
        function (e) {

            if (
                e.target === calendarModal
            ) {

                calendarModal.style.display =
                    "none";

            }

        }
    );

});