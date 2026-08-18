document.addEventListener("DOMContentLoaded", function () {

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
    // نام ماه‌های شمسی
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
    // روزهای هفته
    // =====================================================

    const weekDays = [

        "ش",
        "ی",
        "د",
        "س",
        "چ",
        "پ",
        "ج"

    ];


    // =====================================================
    // تبدیل میلادی به شمسی
    // =====================================================

    function gregorianToJalali(value) {

        if (!value) {
            return null;
        }


        const parts =
            value.split("-");


        if (parts.length !== 3) {
            return null;
        }


        const gy =
            parseInt(parts[0], 10);

        const gm =
            parseInt(parts[1], 10);

        const gd =
            parseInt(parts[2], 10);


        if (
            !gy ||
            !gm ||
            !gd
        ) {

            return null;

        }


        try {

            return jalaali.toJalaali(
                gy,
                gm,
                gd
            );

        }

        catch (error) {

            console.error(
                "خطا در تبدیل میلادی به شمسی:",
                error
            );

            return null;

        }

    }


    // =====================================================
    // تبدیل شمسی به میلادی
    // =====================================================

    function jalaliToGregorian(
        jy,
        jm,
        jd
    ) {

        return jalaali.toGregorian(
            jy,
            jm,
            jd
        );

    }


    // =====================================================
    // فرمت تاریخ شمسی
    // =====================================================

    function formatJalali(
        jy,
        jm,
        jd
    ) {

        return (

            jy +
            "/" +
            String(jm).padStart(2, "0") +
            "/" +
            String(jd).padStart(2, "0")

        );

    }


    // =====================================================
    // گرفتن تاریخ امروز شمسی
    // =====================================================

    const now = new Date();

    const todayJalali =
        jalaali.toJalaali(

            now.getFullYear(),

            now.getMonth() + 1,

            now.getDate()

        );


    // =====================================================
    // ساخت تقویم
    // =====================================================

    function openCalendar(
        displayBox,
        hiddenInput
    ) {


        // =================================================
        // ماه و سال اولیه
        // =================================================

        let viewYear =
            todayJalali.jy;

        let viewMonth =
            todayJalali.jm;


        // =================================================
        // اگر قبلاً تاریخ ذخیره شده
        // =================================================

        const existing =
            gregorianToJalali(
                hiddenInput.value
            );


        if (existing) {

            viewYear =
                existing.jy;

            viewMonth =
                existing.jm;

        }


        // =================================================
        // ساخت Modal
        // =================================================

        const modal =
            document.createElement(
                "div"
            );


        modal.className =
            "profile-calendar-modal";


        modal.innerHTML = `

            <div class="profile-calendar-content">

                <!-- =====================================
                     Header
                ====================================== -->

                <div class="profile-calendar-header">


                    <!-- ماه قبل -->

                    <button
                        type="button"
                        class="profile-prev"
                    >
                        ❮
                    </button>


                    <!-- انتخاب ماه -->

                    <select
                        class="profile-month-select"
                    >

                        ${monthNames
                            .slice(1)
                            .map(
                                (month, index) => `
                                    <option value="${index + 1}">
                                        ${month}
                                    </option>
                                `
                            )
                            .join("")
                        }

                    </select>


                    <!-- انتخاب سال -->

                    <select
                        class="profile-year-select"
                    >

                        ${Array.from(
                            {
                                length: 151
                            },
                            (_, i) => {

                                const year =
                                    1405 - i;

                                return `
                                    <option value="${year}">
                                        ${year}
                                    </option>
                                `;

                            }
                        ).join("")}

                    </select>


                    <!-- ماه بعد -->

                    <button
                        type="button"
                        class="profile-next"
                    >
                        ❯
                    </button>


                    <!-- بستن -->

                    <button
                        type="button"
                        class="profile-calendar-close"
                    >
                        ✕
                    </button>


                </div>


                <!-- =====================================
                     روزهای هفته
                ====================================== -->

                <div class="profile-calendar-week">

                    ${weekDays
                        .map(
                            day =>
                                `<span>${day}</span>`
                        )
                        .join("")
                    }

                </div>


                <!-- =====================================
                     روزهای ماه
                ====================================== -->

                <div
                    class="profile-calendar-days"
                ></div>


            </div>

        `;


        document.body.appendChild(
            modal
        );


        // =================================================
        // گرفتن عناصر
        // =================================================

        const daysContainer =
            modal.querySelector(
                ".profile-calendar-days"
            );


        const monthSelect =
            modal.querySelector(
                ".profile-month-select"
            );


        const yearSelect =
            modal.querySelector(
                ".profile-year-select"
            );


        const prev =
            modal.querySelector(
                ".profile-prev"
            );


        const next =
            modal.querySelector(
                ".profile-next"
            );


        const close =
            modal.querySelector(
                ".profile-calendar-close"
            );


        // =================================================
        // Render Calendar
        // =================================================

        function renderCalendar() {

            daysContainer.innerHTML =
                "";


            // =================================================
            // هماهنگ کردن Select ها با ماه و سال فعلی
            // =================================================

            monthSelect.value =
                String(viewMonth);


            yearSelect.value =
                String(viewYear);


            // =================================================
            // تعداد روزهای ماه
            // =================================================

            const monthDays =
                jalaali.jalaaliMonthLength(
                    viewYear,
                    viewMonth
                );


            // =================================================
            // روز اول ماه به میلادی
            // =================================================

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


            // =================================================
            // پیدا کردن روز هفته
            // =================================================

            let startDay =
                firstDate.getDay();


            /*
                JavaScript:

                Sunday = 0
                Monday = 1
                ...
                Saturday = 6

                تقویم ما:

                شنبه = 0
                یکشنبه = 1
                ...
                جمعه = 6
            */

            startDay =
                (startDay + 1) % 7;


            // =================================================
            // خانه‌های خالی اول ماه
            // =================================================

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
                    "profile-calendar-day empty";


                daysContainer.appendChild(
                    empty
                );

            }


            // =================================================
            // ساخت روزهای ماه
            // =================================================

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
                    "profile-calendar-day";


                dayBox.innerText =
                    day;


                // =================================================
                // تبدیل روز شمسی به میلادی
                // =================================================

                const gregorian =
                    jalaliToGregorian(

                        viewYear,

                        viewMonth,

                        day

                    );


                // =================================================
                // ساخت تاریخ میلادی
                // =================================================

                const isoDate =

                    gregorian.gy +
                    "-" +
                    String(
                        gregorian.gm
                    ).padStart(
                        2,
                        "0"
                    ) +
                    "-" +
                    String(
                        gregorian.gd
                    ).padStart(
                        2,
                        "0"
                    );


                // =================================================
                // بررسی تاریخ انتخاب شده
                // =================================================

                if (
                    hiddenInput.value ===
                    isoDate
                ) {

                    dayBox.classList.add(
                        "selected"
                    );

                }


                // =================================================
                // انتخاب روز
                // =================================================

                dayBox.addEventListener(
                    "click",
                    function () {


                        // =========================================
                        // ذخیره مقدار میلادی در input
                        // =========================================

                        hiddenInput.value =
                            isoDate;


                        // =========================================
                        // نمایش تاریخ شمسی به کاربر
                        // =========================================

                        const span =
                            displayBox.querySelector(
                                "span"
                            );


                        if (span) {

                            span.innerText =
                                formatJalali(

                                    viewYear,

                                    viewMonth,

                                    day

                                );

                        }


                        // =========================================
                        // بستن تقویم
                        // =========================================

                        modal.remove();

                    }
                );


                daysContainer.appendChild(
                    dayBox
                );

            }

        }


        // =====================================================
        // تغییر مستقیم ماه
        // =====================================================

        monthSelect.addEventListener(
            "change",
            function () {

                viewMonth =
                    parseInt(
                        this.value,
                        10
                    );


                renderCalendar();

            }
        );


        // =====================================================
        // تغییر مستقیم سال
        // =====================================================

        yearSelect.addEventListener(
            "change",
            function () {

                viewYear =
                    parseInt(
                        this.value,
                        10
                    );


                renderCalendar();

            }
        );


        // =====================================================
        // ماه قبل
        // =====================================================

        prev.addEventListener(
            "click",
            function () {

                viewMonth--;


                if (
                    viewMonth < 1
                ) {

                    viewMonth = 12;

                    viewYear--;

                }


                // اگر سال خارج از لیست شد
                if (
                    viewYear < 1255
                ) {

                    viewYear = 1255;

                }


                renderCalendar();

            }
        );


        // =====================================================
        // ماه بعد
        // =====================================================

        next.addEventListener(
            "click",
            function () {

                viewMonth++;


                if (
                    viewMonth > 12
                ) {

                    viewMonth = 1;

                    viewYear++;

                }


                // اگر سال خارج از لیست شد
                if (
                    viewYear > 1405
                ) {

                    viewYear = 1405;

                }


                renderCalendar();

            }
        );


        // =====================================================
        // بستن تقویم
        // =====================================================

        close.addEventListener(
            "click",
            function () {

                modal.remove();

            }
        );


        // =====================================================
        // بستن با کلیک بیرون تقویم
        // =====================================================

        modal.addEventListener(
            "click",
            function (event) {

                if (
                    event.target === modal
                ) {

                    modal.remove();

                }

            }
        );


        // =====================================================
        // نمایش اولیه
        // =====================================================

        renderCalendar();

    }


    // =====================================================
    // اتصال تقویم به سه فیلد
    // =====================================================

    document
        .querySelectorAll(
            ".profile-date-input"
        )
        .forEach(
            function (displayBox) {


                // =================================================
                // پیدا کردن input مربوطه
                // =================================================

                const target =
                    displayBox.dataset.target;


                const hiddenInput =
                    document.getElementById(
                        target
                    );


                if (!hiddenInput) {
                    return;
                }


                // =================================================
                // نمایش تاریخ ذخیره شده
                // =================================================

                const existing =
                    gregorianToJalali(
                        hiddenInput.value
                    );


                if (existing) {

                    const span =
                        displayBox.querySelector(
                            "span"
                        );


                    if (span) {

                        span.innerText =

                            formatJalali(

                                existing.jy,

                                existing.jm,

                                existing.jd

                            );

                    }

                }


                // =================================================
                // باز کردن تقویم
                // =================================================

                displayBox.addEventListener(
                    "click",
                    function () {

                        openCalendar(

                            displayBox,

                            hiddenInput

                        );

                    }
                );

            }
        );

});