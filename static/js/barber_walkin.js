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


    // =========================
    // بررسی Jalaali
    // =========================

    if (!window.jalaali) {

        console.error("JALAALI NOT FOUND");

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


        // خانه‌های خالی
        for (
            let i = 0;
            i < startDay;
            i++
        ) {

            const empty =
                document.createElement("div");

            empty.className =
                "calendar-day empty";

            calendar.appendChild(empty);
        }


        // روزهای ماه
        for (
            let day = 1;
            day <= monthDays;
            day++
        ) {

            const dayBox =
                document.createElement("div");

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


            if (selected < today) {

                dayBox.classList.add(
                    "disabled"
                );

            } else {

                dayBox.addEventListener(
                    "click",
                    function () {

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


                        // نمایش شمسی
                        selectedDate.innerText =
                            viewYear +
                            "/" +
                            String(viewMonth)
                                .padStart(2, "0") +
                            "/" +
                            String(day)
                                .padStart(2, "0");


                        // تاریخ میلادی برای Django
                        hiddenDate.value =
                            gregorian.gy +
                            "-" +
                            String(gregorian.gm)
                                .padStart(2, "0") +
                            "-" +
                            String(gregorian.gd)
                                .padStart(2, "0");


                        // بستن تقویم
                        calendarModal.style.display =
                            "none";


                        // ساخت ساعت‌ها
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


    // =========================
    // گرفتن ساعت‌های پر از Django
    // =========================

    async function getBusyTimes(date) {

        try {

            const response =
                await fetch(
                   `/superadmin/barber-walkin/busy-times/?date=${date}`
                );


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

        } catch (error) {

            console.error(
                "BUSY TIMES ERROR:",
                error
            );

            return [];

        }

    }


    // =========================
    // ساخت ساعت‌ها
    // =========================

    async function createTimes(date) {

        timeGrid.innerHTML = "";

        hiddenTime.value = "";


        const busyTimes =
            await getBusyTimes(date);


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


                // اگر ساعت رزرو شده باشد
                // اصلاً نمایش داده نشود
                if (
                    busyTimes.includes(time)
                ) {

                    continue;

                }


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

    }


    // =========================
    // باز کردن تقویم
    // =========================

    openCalendar.addEventListener(
        "click",
        function () {

            calendarModal.style.display =
                "flex";

            renderCalendar();

        }
    );


    // =========================
    // ماه قبل
    // =========================

    prevMonth.addEventListener(
        "click",
        function (e) {

            e.preventDefault();

            viewMonth--;

            if (viewMonth < 1) {

                viewMonth = 12;

                viewYear--;

            }

            renderCalendar();

        }
    );


    // =========================
    // ماه بعد
    // =========================

    nextMonth.addEventListener(
        "click",
        function (e) {

            e.preventDefault();

            viewMonth++;

            if (viewMonth > 12) {

                viewMonth = 1;

                viewYear++;

            }

            renderCalendar();

        }
    );


    // =========================
    // بستن تقویم
    // =========================

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