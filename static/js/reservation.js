document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".accordion").forEach(button => {
    button.addEventListener("click", function () {

        const content = this.nextElementSibling;

        document.querySelectorAll(".accordion-content").forEach(item => {
            if (item !== content) {
                item.style.display = "none";
            }
        });

        content.style.display =
            content.style.display === "block"
                ? "none"
                : "block";
    });
});

    // =====================================================
    // عناصر صفحه
    // =====================================================

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

    const hiddenTime =
        document.getElementById("hiddenTime");

    const timeSection =
        document.getElementById("timeSection");

    const timeGrid =
        document.getElementById("timeGrid");


    // =====================================================
    // بررسی Jalaali
    // =====================================================

    if (!window.jalaali) {

        console.error(
            "Jalaali library پیدا نشد."
        );

        return;
    }


    // =====================================================
    // تاریخ امروز
    // =====================================================

    const now = new Date();

    const todayJalali =
        jalaali.toJalaali(
            now.getFullYear(),
            now.getMonth() + 1,
            now.getDate()
        );


    let viewYear =
        todayJalali.jy;

    let viewMonth =
        todayJalali.jm;


    // =====================================================
    // نام ماه‌ها
    // =====================================================

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
    // باز کردن تقویم
    // =====================================================

    if (openCalendar) {

        openCalendar.addEventListener(
            "click",
            function () {

                calendarModal.style.display =
                    "flex";

                renderCalendar();

            }
        );

    }


    // =====================================================
    // بستن تقویم با کلیک بیرون
    // =====================================================

    window.addEventListener(
        "click",
        function (event) {

            if (
                event.target === calendarModal
            ) {

                calendarModal.style.display =
                    "none";

            }

        }
    );


    // =====================================================
    // ساخت تقویم
    // =====================================================

    function renderCalendar() {

        if (!calendar) {
            return;
        }


        calendar.innerHTML = "";


        if (calendarTitle) {

            calendarTitle.innerText =
                monthNames[viewMonth] +
                " " +
                viewYear;

        }


        const monthDays =
            jalaali.jalaaliMonthLength(
                viewYear,
                viewMonth
            );


        const firstGregorian =
            jalaali.toGregorian(
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


        // شروع هفته از شنبه

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


        // =================================================
        // روزهای ماه
        // =================================================

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
                jalaali.toGregorian(
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


            selected.setHours(
                0,
                0,
                0,
                0
            );


            const today =
                new Date();

            today.setHours(
                0,
                0,
                0,
                0
            );


            // روزهای گذشته

            if (selected < today) {

                dayBox.classList.add(
                    "disabled"
                );

            }

            else {

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


                        // تاریخ شمسی

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


                        // نمایش ساعت‌ها

                        timeSection.style.display =
                            "block";


                        // پاک کردن ساعت قبلی

                        hiddenTime.value =
                            "";


                        // گرفتن ساعت‌های آرایشگر

                        loadAvailableTimes();

                    }
                );

            }


            calendar.appendChild(
                dayBox
            );

        }

    }


    // =====================================================
    // ماه قبل
    // =====================================================

    if (prevMonth) {

        prevMonth.addEventListener(
            "click",
            function (event) {

                event.preventDefault();


                viewMonth--;


                if (viewMonth < 1) {

                    viewMonth = 12;

                    viewYear--;

                }


                renderCalendar();

            }
        );

    }


    // =====================================================
    // ماه بعد
    // =====================================================

    if (nextMonth) {

        nextMonth.addEventListener(
            "click",
            function (event) {

                event.preventDefault();


                viewMonth++;


                if (viewMonth > 12) {

                    viewMonth = 1;

                    viewYear++;

                }


                renderCalendar();

            }
        );

    }


    // =====================================================
    // آرایشگر انتخاب شده
    // =====================================================

    function getSelectedBarber() {

        return document.querySelector(
            "input[name='barber']:checked"
        );

    }


    // =====================================================
    // تبدیل HH:MM به دقیقه
    // =====================================================

    function timeToMinutes(time) {

        if (!time) {
            return 0;
        }


        const parts =
            time.split(":");


        return (
            parseInt(parts[0], 10) * 60 +
            parseInt(parts[1], 10)
        );

    }


    // =====================================================
    // تبدیل دقیقه به HH:MM
    // =====================================================

    function minutesToTime(minutes) {

        const hour =
            Math.floor(
                minutes / 60
            );


        const minute =
            minutes % 60;


        return (
            String(hour).padStart(2, "0") +
            ":" +
            String(minute).padStart(2, "0")
        );

    }


    // =====================================================
    // دریافت ساعت‌های آرایشگر
    // =====================================================

    async function loadAvailableTimes() {

        const barber =
            getSelectedBarber();


        // آرایشگر انتخاب نشده

        if (!barber) {

            timeGrid.innerHTML =
                "<p>ابتدا آرایشگر را انتخاب کنید.</p>";

            return;

        }


        // تاریخ انتخاب نشده

        if (!hiddenDate.value) {

            timeGrid.innerHTML =
                "<p>ابتدا تاریخ را انتخاب کنید.</p>";

            return;

        }


        timeGrid.innerHTML =
            "<p>در حال دریافت ساعت‌ها...</p>";


        try {

            const url =
                "/reservation/blocked-times/" +
                "?barber=" +
                encodeURIComponent(
                    barber.value
                ) +
                "&date=" +
                encodeURIComponent(
                    hiddenDate.value
                );


            const response =
                await fetch(url);


            if (!response.ok) {

                throw new Error(
                    "HTTP " +
                    response.status
                );

            }


            const data =
                await response.json();


            console.log(
                "RESERVATION DATA:",
                data
            );


            // =================================================
            // API شما یک آرایه برمی‌گرداند
            //
            // اولین آیتم:
            //
            // {
            //   type: "working_hours",
            //   start: "09:00",
            //   end: "18:00",
            //   duration: 30
            // }
            //
            // بقیه:
            //
            // {
            //   type: "blocked",
            //   start: "10:00",
            //   end: "10:30"
            // }
            // =================================================


            const workingHours =
                data.find(
                    function (item) {

                        return (
                            item.type ===
                            "working_hours"
                        );

                    }
                );


            if (!workingHours) {

                timeGrid.innerHTML =
                    "<p>ساعت کاری آرایشگر پیدا نشد.</p>";

                return;

            }


            const blocked =
                data.filter(
                    function (item) {

                        return (
                            item.type ===
                            "blocked"
                        );

                    }
                );


            createTimes(
                blocked,
                workingHours.start,
                workingHours.end,
                workingHours.duration
            );


        }

        catch (error) {

            console.error(
                "LOAD TIMES ERROR:",
                error
            );


            timeGrid.innerHTML =
                "<p>دریافت ساعت‌ها با خطا مواجه شد.</p>";

        }

    }


    // =====================================================
    // ساخت ساعت‌ها
    // =====================================================

    function createTimes(
        blocked = [],
        workStart = "09:00",
        workEnd = "18:00",
        appointmentDuration = 30
    ) {

        timeGrid.innerHTML = "";

        hiddenTime.value = "";


        // -----------------------------
        // تبدیل مقادیر
        // -----------------------------

        const startMinutes =
            timeToMinutes(
                workStart
            );


        const endMinutes =
            timeToMinutes(
                workEnd
            );


        const duration =
            parseInt(
                appointmentDuration,
                10
            ) || 30;


        // -----------------------------
        // بررسی ساعت کاری
        // -----------------------------

        if (
            startMinutes >=
            endMinutes
        ) {

            timeGrid.innerHTML =
                "<p>ساعت کاری آرایشگر صحیح نیست.</p>";

            return;

        }


        // =================================================
        // تاریخ امروز
        // =================================================

        const currentDate =
            new Date();


        const today =
            currentDate.getFullYear() +
            "-" +
            String(
                currentDate.getMonth() + 1
            ).padStart(2, "0") +
            "-" +
            String(
                currentDate.getDate()
            ).padStart(2, "0");


        const isToday =
            hiddenDate.value === today;


        const currentMinutes =
            currentDate.getHours() * 60 +
            currentDate.getMinutes();


        let hasTime = false;


        // =================================================
        // ساخت ساعت‌ها
        // =================================================

        for (
            let minutes = startMinutes;

            minutes + duration <=
            endMinutes;

            minutes += duration
        ) {

            const time =
                minutesToTime(
                    minutes
                );


            const slotEnd =
                minutes + duration;


            let hide = false;


            // =================================================
            // ساعت گذشته
            // =================================================

            if (
                isToday &&
                minutes <= currentMinutes
            ) {

                hide = true;

            }


            // =================================================
            // بررسی تداخل با رزرو یا Block
            // =================================================

            if (!hide) {

                blocked.forEach(
                    function (item) {

                        const blockedStart =
                            timeToMinutes(
                                item.start
                            );


                        const blockedEnd =
                            timeToMinutes(
                                item.end
                            );


                        // اگر بازه نوبت
                        // با بازه مسدود تداخل دارد

                        if (
                            minutes <
                                blockedEnd &&
                            slotEnd >
                                blockedStart
                        ) {

                            hide = true;

                        }

                    }
                );

            }


            // =================================================
            // ساخت دکمه ساعت
            // =================================================

            if (!hide) {

                hasTime = true;


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


        // =================================================
        // اگر ساعت خالی نبود
        // =================================================

        if (!hasTime) {

            timeGrid.innerHTML =
                "<p>برای این تاریخ ساعت خالی وجود ندارد.</p>";

        }

    }


    // =====================================================
    // تغییر آرایشگر
    // =====================================================

    document
        .querySelectorAll(
            "input[name='barber']"
        )
        .forEach(
            function (barber) {

                barber.addEventListener(
                    "change",
                    function () {

                        hiddenTime.value =
                            "";


                        timeGrid.innerHTML =
                            "";


                        // اگر تاریخ قبلاً انتخاب شده
                        // ساعت آرایشگر جدید را بگیر

                        if (
                            hiddenDate.value
                        ) {

                            timeSection.style.display =
                                "block";


                            loadAvailableTimes();

                        }

                    }
                );

            }
        );


});

// =====================================================
// فیلتر آرایشگرها بر اساس خدمت انتخاب شده
// =====================================================

const serviceInputs = document.querySelectorAll(
    "input[name='service']"
);

const barberCards = document.querySelectorAll(
    ".barber-card"
);

const barberMessage = document.getElementById(
    "barberMessage"
);


serviceInputs.forEach(function (serviceInput) {

    serviceInput.addEventListener(
        "change",
        function () {

            const barberIds =
                this.dataset.barbers
                    ? this.dataset.barbers.split(",")
                    : [];


            let visibleBarbers = 0;


            barberCards.forEach(function (card) {

                const barberId =
                    card.dataset.barberId;

                const barberInput =
                    card.querySelector(
                        "input[name='barber']"
                    );


                if (
                    barberIds.includes(barberId)
                ) {

                    card.style.display = "";

                    visibleBarbers++;

                } else {

                    card.style.display = "none";

                    // اگر قبلاً انتخاب شده بود
                    // انتخابش را بردار

                    if (barberInput) {
                        barberInput.checked = false;
                    }

                }

            });


            // پیام اگر هیچ آرایشگری این خدمت را ارائه ندهد

            if (barberMessage) {

                if (visibleBarbers === 0) {

                    barberMessage.style.display =
                        "block";

                } else {

                    barberMessage.style.display =
                        "none";

                }

            }


            // ساعت قبلی را پاک کن

            if (hiddenTime) {
                hiddenTime.value = "";
            }

            if (timeGrid) {
                timeGrid.innerHTML = "";
            }

            if (timeSection) {
                timeSection.style.display = "none";
            }

        }
    );

});
// =====================================================
// انتخاب خودکار خدمت از URL
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    const params = new URLSearchParams(
        window.location.search
    );

    const serviceId = params.get("service");

    if (!serviceId) {
        return;
    }

    const selectedService = document.querySelector(
        'input[name="service"][value="' + serviceId + '"]'
    );

    if (!selectedService) {
        console.log("SERVICE NOT FOUND:", serviceId);
        return;
    }

    // انتخاب خدمت
    selectedService.checked = true;

    // باز کردن توضیحات خدمت
    const accordionContent =
        selectedService.closest(".accordion-content");

    if (accordionContent) {
        accordionContent.style.display = "block";
    }

    // آرایشگرهای مجاز این خدمت
    const barberIds =
        selectedService.dataset.barbers
            ? selectedService.dataset.barbers
                .split(",")
                .filter(Boolean)
            : [];

    let visibleBarbers = 0;

    barberCards.forEach(function (card) {

        const barberId =
            card.dataset.barberId;

        const barberInput =
            card.querySelector(
                'input[name="barber"]'
            );

        if (barberIds.includes(barberId)) {

            card.style.display = "";
            visibleBarbers++;

        } else {

            card.style.display = "none";

            if (barberInput) {
                barberInput.checked = false;
            }
        }

    });

    // پیام نبودن آرایشگر
    if (barberMessage) {

        barberMessage.style.display =
            visibleBarbers === 0
                ? "block"
                : "none";
    }

    console.log(
        "AUTO SELECTED SERVICE:",
        serviceId
    );

});