document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // بررسی Jalaali
    // =====================================================

    if (!window.jalaali) {
        console.error("Jalaali library پیدا نشد.");
        return;
    }


    // =====================================================
    // آکاردئون خدمات
    // =====================================================

    document.querySelectorAll(".accordion").forEach(button => {

        button.addEventListener("click", function () {

            const content = this.nextElementSibling;

            document.querySelectorAll(".accordion-content")
                .forEach(item => {

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
    // تاریخ امروز
    // =====================================================

    const now = new Date();

    const todayJalali = jalaali.toJalaali(
        now.getFullYear(),
        now.getMonth() + 1,
        now.getDate()
    );


    // =====================================================
    // تبدیل ساعت به دقیقه
    // =====================================================

    function timeToMinutes(time) {

        if (!time) {
            return 0;
        }

        const parts = time.split(":");

        return (
            parseInt(parts[0], 10) * 60 +
            parseInt(parts[1], 10)
        );

    }


    // =====================================================
    // تبدیل دقیقه به ساعت
    // =====================================================

    function minutesToTime(minutes) {

        const hour =
            Math.floor(minutes / 60);

        const minute =
            minutes % 60;

        return (
            String(hour).padStart(2, "0") +
            ":" +
            String(minute).padStart(2, "0")
        );

    }


   function createTimes(
    timeGrid,
    hiddenTime,
    blocked = [],
    workStart = "09:00",
    workEnd = "18:00",
    appointmentDuration = 30
) {

    timeGrid.innerHTML = "";
    hiddenTime.value = "";

    const startMinutes =
        timeToMinutes(workStart);

    const endMinutes =
        timeToMinutes(workEnd);

    const duration =
        parseInt(
            appointmentDuration,
            10
        ) || 30;


    if (startMinutes >= endMinutes) {

        timeGrid.innerHTML =
            "<p>ساعت کاری آرایشگر صحیح نیست.</p>";

        return;

    }


    // =================================================
    // بررسی امروز
    // =================================================

    const currentDate = new Date();

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


    const serviceSchedule =
        hiddenTime.closest(
            ".service-schedule"
        );


    const hiddenDate =
        serviceSchedule
            ? serviceSchedule.querySelector(
                ".service-hidden-date"
            )
            : null;


    const selectedDate =
        hiddenDate
            ? hiddenDate.value
            : "";


    const isToday =
        selectedDate === today;


    const currentMinutes =
        currentDate.getHours() * 60 +
        currentDate.getMinutes();


    let hasTime = false;


    // =================================================
    // ساخت ساعت‌ها
    // =================================================

    for (
        let minutes = startMinutes;
        minutes + duration <= endMinutes;
        minutes += duration
    ) {

        const time =
            minutesToTime(minutes);

        const slotEnd =
            minutes + duration;


        // =================================================
        // ساعت گذشته
        // =================================================

        if (
            isToday &&
            minutes <= currentMinutes
        ) {

            continue;

        }


        // =================================================
        // بررسی رزرو شده بودن ساعت
        // =================================================

        let isBlocked = false;


        blocked.forEach(item => {

            const blockedStart =
                timeToMinutes(
                    item.start
                );

            const blockedEnd =
                timeToMinutes(
                    item.end
                );


            if (
                minutes < blockedEnd &&
                slotEnd > blockedStart
            ) {

                isBlocked = true;

            }

        });


        hasTime = true;


        // =================================================
        // ساخت دکمه ساعت
        // =================================================

        const button =
            document.createElement(
                "button"
            );


        button.type = "button";

        button.className = "time-btn";

        button.innerText = time;


        // =================================================
        // ساعت رزرو شده
        // =================================================

        if (isBlocked) {

            button.classList.add(
                "booked"
            );

            button.disabled = true;

            button.title =
                "این ساعت قبلاً رزرو شده است.";

        }


        // =================================================
        // ساعت آزاد
        // =================================================

        else {

            button.addEventListener(
                "click",
                function () {

                    timeGrid
                        .querySelectorAll(
                            ".time-btn"
                        )
                        .forEach(btn => {

                            btn.classList.remove(
                                "active"
                            );

                        });


                    button.classList.add(
                        "active"
                    );


                    hiddenTime.value =
                        time;


                    // متن دکمه اصلی ساعت

                    const schedule =
                        hiddenTime.closest(
                            ".service-schedule"
                        );


                    if (schedule) {

                        const timeButton =
                            schedule.querySelector(
                                ".selected-service-time span"
                            );


                        if (timeButton) {

                            timeButton.innerText =
                                "ساعت انتخاب شده: " +
                                time;

                        }

                    }


                    console.log(
                        "SELECTED TIME:",
                        time
                    );


                    // بستن Popup

                    const modal =
                        document.querySelector(
                            ".service-time-modal"
                        );


                    if (modal) {

                        modal.remove();

                    }

                }
            );

        }


        timeGrid.appendChild(
            button
        );

    }


    // =================================================
    // هیچ ساعتی وجود ندارد
    // =================================================

    if (!hasTime) {

        timeGrid.innerHTML =
            "<p>برای این تاریخ ساعت کاری باقی نمانده است.</p>";

    }

}

    // =====================================================
    // Popup ساعت
    // =====================================================

    function openTimeModal(serviceItem) {

        const originalGrid =
            serviceItem.querySelector(
                ".service-time-grid"
            );


        const hiddenTime =
            serviceItem.querySelector(
                ".service-hidden-time"
            );


        const selectedTimeBox =
            serviceItem.querySelector(
                ".selected-service-time"
            );


        if (!originalGrid || !hiddenTime) {
            return;
        }


        // اگر ساعت هنوز ساخته نشده

        if (
            !originalGrid.querySelector(".time-btn")
        ) {

            alert(
                "ابتدا تاریخ را انتخاب کنید تا ساعت‌های خالی نمایش داده شوند."
            );

            return;

        }


        // اگر Popup قبلی وجود دارد

        const oldModal =
            document.querySelector(
                ".service-time-modal"
            );


        if (oldModal) {
            oldModal.remove();
        }


        // =================================================
        // ساخت Popup
        // =================================================

        const modal =
            document.createElement("div");


        modal.className =
            "service-time-modal";


        modal.innerHTML = `

            <div class="service-time-modal-content">

                <div class="service-time-modal-header">

                    <h3>
                        انتخاب ساعت
                    </h3>

                    <button
                        type="button"
                        class="close-service-time"
                    >
                        ✕
                    </button>

                </div>


                <p style="
                    color:#aaa;
                    margin-bottom:15px;
                    text-align:center;
                ">
                    ساعت مورد نظر خود را انتخاب کنید
                </p>


                <div
                    class="service-time-slider"
                ></div>

            </div>

        `;


        document.body.appendChild(modal);


        const slider =
            modal.querySelector(
                ".service-time-slider"
            );


        const buttons =
            originalGrid.querySelectorAll(
                ".time-btn"
            );


        // =================================================
        // انتقال دکمه‌ها به ریل
        // =================================================

        buttons.forEach(button => {

            const clone =
                button.cloneNode(true);


            if (
                hiddenTime.value ===
                clone.innerText
            ) {

                clone.classList.add(
                    "active"
                );

            }


            clone.addEventListener(
                "click",
                function () {

                    const selectedTime =
                        clone.innerText;


                    hiddenTime.value =
                        selectedTime;


                    buttons.forEach(btn => {

                        btn.classList.remove(
                            "active"
                        );

                    });


                    clone.classList.add(
                        "active"
                    );


                    const text =
                        selectedTimeBox
                            ?.querySelector(
                                "span"
                            );


                    if (text) {

                        text.innerText =
                            "ساعت انتخاب شده: " +
                            selectedTime;

                    }


                    console.log(
                        "SELECTED TIME:",
                        selectedTime
                    );


                    modal.remove();

                }
            );


            slider.appendChild(
                clone
            );

        });


        // =================================================
        // بستن Popup
        // =================================================

        const closeButton =
            modal.querySelector(
                ".close-service-time"
            );


        closeButton.addEventListener(
            "click",
            function () {

                modal.remove();

            }
        );


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


        // =================================================
        // ریل با موس
        // =================================================

        let isDown = false;

        let startX;

        let scrollLeft;


        slider.addEventListener(
            "mousedown",
            function (event) {

                isDown = true;

                slider.style.cursor =
                    "grabbing";

                startX =
                    event.pageX -
                    slider.offsetLeft;

                scrollLeft =
                    slider.scrollLeft;

            }
        );


        slider.addEventListener(
            "mouseleave",
            function () {

                isDown = false;

                slider.style.cursor =
                    "grab";

            }
        );


        slider.addEventListener(
            "mouseup",
            function () {

                isDown = false;

                slider.style.cursor =
                    "grab";

            }
        );


        slider.addEventListener(
            "mousemove",
            function (event) {

                if (!isDown) {
                    return;
                }


                event.preventDefault();


                const x =
                    event.pageX -
                    slider.offsetLeft;


                const walk =
                    (x - startX) * 1.5;


                slider.scrollLeft =
                    scrollLeft - walk;

            }
        );


        // =================================================
        // لمس موبایل
        // =================================================

        let touchStartX = 0;

        let touchScrollLeft = 0;


        slider.addEventListener(
            "touchstart",
            function (event) {

                touchStartX =
                    event.touches[0].pageX;

                touchScrollLeft =
                    slider.scrollLeft;

            },
            { passive: true }
        );


        slider.addEventListener(
            "touchmove",
            function (event) {

                const currentX =
                    event.touches[0].pageX;


                const distance =
                    currentX -
                    touchStartX;


                slider.scrollLeft =
                    touchScrollLeft -
                    distance;

            },
            { passive: true }
        );

    }


    // =====================================================
    // دریافت ساعت‌های آرایشگر
    // =====================================================

    async function loadServiceTimes(
        serviceItem,
        barberId,
        date
    ) {

        const timeGrid =
            serviceItem.querySelector(
                ".service-time-grid"
            );


        const hiddenTime =
            serviceItem.querySelector(
                ".service-hidden-time"
            );


        if (
            !timeGrid ||
            !hiddenTime
        ) {

            return;

        }


        timeGrid.innerHTML =
            "<p>در حال دریافت ساعت‌ها...</p>";

        hiddenTime.value = "";


        try {

            const url =
                "/reservation/blocked-times/" +
                "?barber=" +
                encodeURIComponent(
                    barberId
                ) +
                "&date=" +
                encodeURIComponent(
                    date
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
                "SERVICE RESERVATION DATA:",
                data
            );


            const workingHours =
                data.find(
                    item =>
                        item.type ===
                        "working_hours"
                );


            if (!workingHours) {

                timeGrid.innerHTML =
                    "<p>ساعت کاری آرایشگر پیدا نشد.</p>";

                return;

            }


            const blocked =
                data.filter(
                    item =>
                        item.type ===
                        "blocked"
                );


            createTimes(
                timeGrid,
                hiddenTime,
                blocked,
                workingHours.start,
                workingHours.end,
                workingHours.duration
            );


            // =================================================
            // ساعت‌ها آماده شدند
            // =================================================

            const selectedTimeBox =
                serviceItem.querySelector(
                    ".selected-service-time"
                );


            if (selectedTimeBox) {

                selectedTimeBox.style.display =
                    "flex";


                const text =
                    selectedTimeBox.querySelector(
                        "span"
                    );


                if (text) {

                    text.innerText =
                        "برای انتخاب ساعت کلیک کنید";

                }


                // باز کردن Popup با کلیک

                selectedTimeBox.onclick =
                    function () {

                        openTimeModal(
                            serviceItem
                        );

                    };

            }

        }

        catch (error) {

            console.error(
                "LOAD SERVICE TIMES ERROR:",
                error
            );


            timeGrid.innerHTML =
                "<p>دریافت ساعت‌ها با خطا مواجه شد.</p>";

        }

    }


    // =====================================================
    // مدیریت خدمات
    // =====================================================

    document
        .querySelectorAll(".service-item")
        .forEach(serviceItem => {


            const serviceCheckbox =
                serviceItem.querySelector(
                    'input[name="services"]'
                );


            const schedule =
                serviceItem.querySelector(
                    ".service-schedule"
                );


            const barberInputs =
                serviceItem.querySelectorAll(
                    ".service-barber-card input"
                );


            const dateInput =
                serviceItem.querySelector(
                    ".service-date-input"
                );


            const selectedDate =
                serviceItem.querySelector(
                    ".service-selected-date"
                );


            const hiddenDate =
                serviceItem.querySelector(
                    ".service-hidden-date"
                );


            const hiddenTime =
                serviceItem.querySelector(
                    ".service-hidden-time"
                );


            const timeGrid =
                serviceItem.querySelector(
                    ".service-time-grid"
                );


            // =================================================
            // انتخاب خدمت
            // =================================================

            if (serviceCheckbox) {

                serviceCheckbox.addEventListener(
                    "change",
                    function () {

                        if (this.checked) {

                            if (schedule) {

                                schedule.style.display =
                                    "block";

                            }

                        }

                        else {

                            if (schedule) {

                                schedule.style.display =
                                    "none";

                            }


                            barberInputs.forEach(
                                input => {

                                    input.checked =
                                        false;

                                }
                            );


                            if (hiddenDate) {

                                hiddenDate.value =
                                    "";

                            }


                            if (selectedDate) {

                                selectedDate.innerText =
                                    "برای انتخاب تاریخ کلیک کنید";

                            }


                            if (hiddenTime) {

                                hiddenTime.value =
                                    "";

                            }


                            if (timeGrid) {

                                timeGrid.innerHTML =
                                    "";

                            }

                        }

                    }
                );

            }


            // =================================================
            // انتخاب آرایشگر
            // =================================================

            barberInputs.forEach(
                barberInput => {

                    barberInput.addEventListener(
                        "change",
                        function () {

                            console.log(
                                "SELECTED BARBER:",
                                this.value
                            );
// =================================================
// نمایش قیمت آرایشگر انتخاب شده
// =================================================

const selectedBarberCard =
    this.closest(".service-barber-card");

const selectedBarberPrice =
    serviceItem.querySelector(
        ".selected-barber-price"
    );

const barberPriceValue =
    serviceItem.querySelector(
        ".barber-price-value"
    );


if (
    selectedBarberCard &&
    selectedBarberPrice &&
    barberPriceValue
) {

    const price =
        selectedBarberCard.dataset.price;


    if (price) {

        barberPriceValue.innerText =
            Number(price).toLocaleString("fa-IR");

        selectedBarberPrice.style.display =
            "flex";

    }

    else {

        barberPriceValue.innerText =
            "ثبت نشده";

        selectedBarberPrice.style.display =
            "flex";

    }

}

                            if (hiddenDate) {

                                hiddenDate.value =
                                    "";

                            }


                            if (selectedDate) {

                                selectedDate.innerText =
                                    "برای انتخاب تاریخ کلیک کنید";

                            }


                            if (hiddenTime) {

                                hiddenTime.value =
                                    "";

                            }


                            if (timeGrid) {

                                timeGrid.innerHTML =
                                    "";

                            }


                            const selectedTimeBox =
                                serviceItem.querySelector(
                                    ".selected-service-time"
                                );


                            if (selectedTimeBox) {

                                selectedTimeBox.style.display =
                                    "flex";


                                const text =
                                    selectedTimeBox.querySelector(
                                        "span"
                                    );


                                if (text) {

                                    text.innerText =
                                        "ابتدا تاریخ را انتخاب کنید";

                                }

                            }

                        }
                    );

                }
            );


            // =================================================
            // تقویم خدمت
            // =================================================

            if (dateInput) {

                dateInput.addEventListener(
                    "click",
                    function () {


                        const selectedBarber =
                            serviceItem.querySelector(
                                ".service-barber-card input:checked"
                            );


                        if (!selectedBarber) {

                            alert(
                                "ابتدا آرایشگر این خدمت را انتخاب کنید."
                            );

                            return;

                        }


                        let viewYear =
                            todayJalali.jy;

                        let viewMonth =
                            todayJalali.jm;


                        const modal =
                            document.createElement(
                                "div"
                            );


                        modal.className =
                            "calendar-modal";


                        modal.style.display =
                            "flex";


                        modal.innerHTML = `

                            <div class="calendar-content">

                                <button
                                    type="button"
                                    class="service-prev-month"
                                >
                                    ❮
                                </button>

                                <h3
                                    class="service-calendar-title"
                                ></h3>

                                <button
                                    type="button"
                                    class="service-next-month"
                                >
                                    ❯
                                </button>

                                <button
                                    type="button"
                                    class="service-close-calendar"
                                >
                                    ✕
                                </button>

                                <div class="week-days">

                                    <span>ش</span>
                                    <span>ی</span>
                                    <span>د</span>
                                    <span>س</span>
                                    <span>چ</span>
                                    <span>پ</span>
                                    <span>ج</span>

                                </div>

                                <div
                                    class="calendar-days service-calendar-days"
                                ></div>

                            </div>
                        `;


                        document.body.appendChild(
                            modal
                        );


                        const calendar =
                            modal.querySelector(
                                ".service-calendar-days"
                            );


                        const calendarTitle =
                            modal.querySelector(
                                ".service-calendar-title"
                            );


                        const prev =
                            modal.querySelector(
                                ".service-prev-month"
                            );


                        const next =
                            modal.querySelector(
                                ".service-next-month"
                            );


                        const close =
                            modal.querySelector(
                                ".service-close-calendar"
                            );


                        function renderServiceCalendar() {

                            calendar.innerHTML =
                                "";


                            calendarTitle.innerText =
                                monthNames[viewMonth] +
                                " " +
                                viewYear;


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


                            let startDay =
                                firstDate.getDay();


                            startDay =
                                (startDay + 1) % 7;


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


                                if (selected < today) {

    // روز گذشته نمایش داده نشود
    dayBox.style.visibility = "hidden";

}

else {

    dayBox.addEventListener(
        "click",
        function () {

            selectedDate.innerText =
                viewYear +
                "/" +
                String(viewMonth).padStart(2, "0") +
                "/" +
                String(day).padStart(2, "0");


            hiddenDate.value =
                gregorian.gy +
                "-" +
                String(gregorian.gm).padStart(2, "0") +
                "-" +
                String(gregorian.gd).padStart(2, "0");


            modal.remove();


            const selectedTimeBox =
                serviceItem.querySelector(
                    ".selected-service-time"
                );


            if (selectedTimeBox) {

                selectedTimeBox.style.display =
                    "flex";


                const text =
                    selectedTimeBox.querySelector(
                        "span"
                    );


                if (text) {

                    text.innerText =
                        "در حال دریافت ساعت‌ها...";

                }

            }


            loadServiceTimes(
                serviceItem,
                selectedBarber.value,
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


                        prev.addEventListener(
                            "click",
                            function () {

                                viewMonth--;


                                if (viewMonth < 1) {

                                    viewMonth = 12;

                                    viewYear--;

                                }


                                renderServiceCalendar();

                            }
                        );


                        next.addEventListener(
                            "click",
                            function () {

                                viewMonth++;


                                if (viewMonth > 12) {

                                    viewMonth = 1;

                                    viewYear++;

                                }


                                renderServiceCalendar();

                            }
                        );


                        close.addEventListener(
                            "click",
                            function () {

                                modal.remove();

                            }
                        );


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


                        renderServiceCalendar();

                    }
                );

            }

        });


    // =====================================================
    // انتخاب خودکار خدمت از URL
    // =====================================================

    const params =
        new URLSearchParams(
            window.location.search
        );


    const serviceId =
        params.get("service");


    if (serviceId) {

        const selectedService =
            document.querySelector(
                'input[name="services"][value="' +
                serviceId +
                '"]'
            );


        if (selectedService) {

            selectedService.checked =
                true;


            const content =
                selectedService.closest(
                    ".accordion-content"
                );


            if (content) {

                content.style.display =
                    "block";

            }


            const schedule =
                content?.querySelector(
                    ".service-schedule"
                );


            if (schedule) {

                schedule.style.display =
                    "block";

            }

        }

    }


});