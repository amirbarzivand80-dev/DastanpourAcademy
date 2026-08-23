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

    document.querySelectorAll(".accordion").forEach(function (button) {

        button.addEventListener("click", function () {

            var content = this.nextElementSibling;

            document.querySelectorAll(".accordion-content")
                .forEach(function (item) {

                    if (item !== content) {
                        item.style.display = "none";
                    }

                });

            if (content) {
                content.style.display =
                    content.style.display === "block"
                        ? "none"
                        : "block";
            }

        });

    });


    // =====================================================
    // نام ماه‌های شمسی
    // =====================================================

    var monthNames = [
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

    var now = new Date();

    var todayJalali = jalaali.toJalaali(
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

        var parts = time.split(":");

        return (
            parseInt(parts[0], 10) * 60 +
            parseInt(parts[1], 10)
        );

    }


    // =====================================================
    // تبدیل دقیقه به ساعت
    // =====================================================

    function minutesToTime(minutes) {

        var hour = Math.floor(minutes / 60);

        var minute = minutes % 60;

        return (
            String(hour).padStart(2, "0") +
            ":" +
            String(minute).padStart(2, "0")
        );

    }


    // =====================================================
    // جزئیات خدمت
    // نمایش قیمت و مدت مخصوص آرایشگر
    // =====================================================

    function updateServiceDetails(serviceItem, barberId) {

        var detailItems =
            serviceItem.querySelectorAll(
                ".service-detail-item"
            );


        detailItems.forEach(function (detailItem) {

            var checkbox =
                detailItem.querySelector(
                    ".service-detail-checkbox"
                );


            var priceValue =
                detailItem.querySelector(
                    ".detail-price-value"
                );


            // =================================================
            // پیدا کردن اطلاعات آرایشگر
            // بدون Template Literal
            // =================================================

            var barberData = null;

            var barberDataItems =
                detailItem.querySelectorAll(
                    ".detail-barber-data"
                );


            barberDataItems.forEach(function (item) {

                if (
                    String(item.getAttribute("data-barber")) ===
                    String(barberId)
                ) {

                    barberData = item;

                }

            });


            // =================================================
            // اطلاعات برای این آرایشگر وجود دارد
            // =================================================

            if (barberData) {

                var price =
                    barberData.getAttribute("data-price");

                var duration =
                    barberData.getAttribute("data-duration");


                if (priceValue) {

                    var text =
                        Number(price || 0)
                            .toLocaleString("fa-IR");

                    text += " تومان";


                    if (duration) {

                        text +=
                            " - " +
                            duration +
                            " دقیقه";

                    }


                    priceValue.innerText = text;

                }


                if (checkbox) {

                    checkbox.disabled = false;

                }


                detailItem.style.opacity = "1";

            }


            // =================================================
            // برای این آرایشگر ثبت نشده
            // =================================================

            else {

                if (priceValue) {

                    priceValue.innerText =
                        "برای این آرایشگر ثبت نشده";

                }


                if (checkbox) {

                    checkbox.checked = false;

                    checkbox.disabled = true;

                }


                detailItem.style.opacity = "0.45";

            }

        });

    }


    // =====================================================
    // ریست جزئیات خدمت
    // =====================================================

    function resetServiceDetails(serviceItem) {

        var detailItems =
            serviceItem.querySelectorAll(
                ".service-detail-item"
            );


        detailItems.forEach(function (detailItem) {

            var checkbox =
                detailItem.querySelector(
                    ".service-detail-checkbox"
                );


            var priceValue =
                detailItem.querySelector(
                    ".detail-price-value"
                );


            if (checkbox) {

                checkbox.checked = false;

                checkbox.disabled = false;

            }


            if (priceValue) {

                priceValue.innerText =
                    "ابتدا آرایشگر را انتخاب کنید";

            }


            detailItem.style.opacity = "1";

        });

    }


    // =====================================================
    // ساخت ساعت‌ها
    // =====================================================

    function createTimes(
        timeGrid,
        hiddenTime,
        blocked,
        workStart,
        workEnd,
        appointmentDuration
    ) {

        if (!blocked) {
            blocked = [];
        }

        if (!workStart) {
            workStart = "09:00";
        }

        if (!workEnd) {
            workEnd = "18:00";
        }

        if (!appointmentDuration) {
            appointmentDuration = 30;
        }


        timeGrid.innerHTML = "";

        hiddenTime.value = "";


        var startMinutes =
            timeToMinutes(workStart);


        var endMinutes =
            timeToMinutes(workEnd);


        var duration =
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

        var currentDate = new Date();


        var today =
            currentDate.getFullYear() +
            "-" +
            String(
                currentDate.getMonth() + 1
            ).padStart(2, "0") +
            "-" +
            String(
                currentDate.getDate()
            ).padStart(2, "0");


        var serviceSchedule =
            hiddenTime.closest(
                ".service-schedule"
            );


        var hiddenDate =
            serviceSchedule
                ? serviceSchedule.querySelector(
                    ".service-hidden-date"
                )
                : null;


        var selectedDate =
            hiddenDate
                ? hiddenDate.value
                : "";


        var isToday =
            selectedDate === today;


        var currentMinutes =
            currentDate.getHours() * 60 +
            currentDate.getMinutes();


        // =================================================
        // ساخت ساعت‌های پایه
        // =================================================

        var slots = new Set();


        for (
            var minutes = startMinutes;
            minutes < endMinutes;
            minutes += 30
        ) {

            if (
                minutes + duration <=
                endMinutes
            ) {

                slots.add(minutes);

            }

        }


        // =================================================
        // پایان رزروهای قبلی
        // =================================================

        blocked.forEach(function (item) {

            var blockedEnd =
                timeToMinutes(
                    item.end
                );


            if (
                blockedEnd >= startMinutes &&
                blockedEnd < endMinutes &&
                blockedEnd + duration <= endMinutes
            ) {

                slots.add(blockedEnd);

            }

        });


        // =================================================
        // مرتب‌سازی
        // =================================================

        var sortedSlots =
            Array.from(slots).sort(
                function (a, b) {
                    return a - b;
                }
            );


        var hasTime = false;


        // =================================================
        // ساخت ساعت‌ها
        // =================================================

        sortedSlots.forEach(function (minutes) {

            var time =
                minutesToTime(minutes);


            var slotEnd =
                minutes + duration;


            // =================================================
            // ساعت گذشته
            // =================================================

            if (
                isToday &&
                minutes <= currentMinutes
            ) {

                return;

            }


            // =================================================
            // بررسی تداخل
            // =================================================

            var isBlocked = false;


            blocked.forEach(function (item) {

                var blockedStart =
                    timeToMinutes(
                        item.start
                    );


                var blockedEnd =
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
            // ساخت دکمه
            // =================================================

            var button =
                document.createElement(
                    "button"
                );


            button.type = "button";

            button.className = "time-btn";

            button.innerText = time;


            // =================================================
            // ساعت پر
            // =================================================

            if (isBlocked) {

                button.classList.add("booked");

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
                            .forEach(function (btn) {

                                btn.classList.remove(
                                    "active"
                                );

                            });


                        button.classList.add(
                            "active"
                        );


                        hiddenTime.value =
                            time;


                        var schedule =
                            hiddenTime.closest(
                                ".service-schedule"
                            );


                        if (schedule) {

                            var timeButton =
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


                        var modal =
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

        });


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

        var originalGrid =
            serviceItem.querySelector(
                ".service-time-grid"
            );


        var hiddenTime =
            serviceItem.querySelector(
                ".service-hidden-time"
            );


        var selectedTimeBox =
            serviceItem.querySelector(
                ".selected-service-time"
            );


        if (
            !originalGrid ||
            !hiddenTime
        ) {

            return;

        }


        // =================================================
        // بررسی وجود ساعت
        // =================================================

        if (
            !originalGrid.querySelector(
                ".time-btn"
            )
        ) {

            alert(
                "ابتدا تاریخ را انتخاب کنید تا ساعت‌های خالی نمایش داده شوند."
            );

            return;

        }


        // =================================================
        // حذف Popup قبلی
        // =================================================

        var oldModal =
            document.querySelector(
                ".service-time-modal"
            );


        if (oldModal) {

            oldModal.remove();

        }


        // =================================================
        // ساخت Popup
        // =================================================

        var modal =
            document.createElement(
                "div"
            );


        modal.className =
            "service-time-modal";


        // =================================================
        // به جای innerHTML با Template Literal
        // از ساخت مستقیم DOM استفاده می‌کنیم
        // =================================================

        var modalContent =
            document.createElement("div");

        modalContent.className =
            "service-time-modal-content";


        var header =
            document.createElement("div");

        header.className =
            "service-time-modal-header";


        var title =
            document.createElement("h3");

        title.innerText =
            "انتخاب ساعت";


        var closeButton =
            document.createElement("button");

        closeButton.type = "button";

        closeButton.className =
            "close-service-time";

        closeButton.innerText = "✕";


        header.appendChild(title);

        header.appendChild(closeButton);


        var description =
            document.createElement("p");

        description.innerText =
            "ساعت مورد نظر خود را انتخاب کنید";

        description.style.color = "#aaa";

        description.style.marginBottom = "15px";

        description.style.textAlign = "center";


        var slider =
            document.createElement("div");

        slider.className =
            "service-time-slider";


        modalContent.appendChild(header);

        modalContent.appendChild(description);

        modalContent.appendChild(slider);

        modal.appendChild(modalContent);

        document.body.appendChild(modal);


        // =================================================
        // دریافت دکمه‌های ساعت
        // =================================================

        var buttons =
            originalGrid.querySelectorAll(
                ".time-btn"
            );


        // =================================================
        // انتقال دکمه‌ها به Popup
        // =================================================

        buttons.forEach(function (button) {

            var clone =
                button.cloneNode(true);


            if (
                hiddenTime.value ===
                clone.innerText
            ) {

                clone.classList.add(
                    "active"
                );

            }


            // اگر ساعت رزرو شده است
            // دوباره کلیک‌پذیر نشود

            if (clone.disabled) {

                clone.disabled = true;

            }

            else {

                clone.addEventListener(
                    "click",
                    function () {

                        var selectedTime =
                            clone.innerText;


                        hiddenTime.value =
                            selectedTime;


                        buttons.forEach(
                            function (btn) {

                                btn.classList.remove(
                                    "active"
                                );

                            }
                        );


                        clone.classList.add(
                            "active"
                        );


                        var text = null;


                        if (selectedTimeBox) {

                            text =
                                selectedTimeBox.querySelector(
                                    "span"
                                );

                        }


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

            }


            slider.appendChild(
                clone
            );

        });


        // =================================================
        // بستن Popup
        // =================================================

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

        var isDown = false;

        var startX = 0;

        var scrollLeft = 0;


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


                var x =
                    event.pageX -
                    slider.offsetLeft;


                var walk =
                    (x - startX) * 1.5;


                slider.scrollLeft =
                    scrollLeft - walk;

            }
        );


        // =================================================
        // لمس موبایل
        // =================================================

        var touchStartX = 0;

        var touchScrollLeft = 0;


        slider.addEventListener(
            "touchstart",
            function (event) {

                touchStartX =
                    event.touches[0].pageX;

                touchScrollLeft =
                    slider.scrollLeft;

            },
            {
                passive: true
            }
        );


        slider.addEventListener(
            "touchmove",
            function (event) {

                var currentX =
                    event.touches[0].pageX;


                var distance =
                    currentX -
                    touchStartX;


                slider.scrollLeft =
                    touchScrollLeft -
                    distance;

            },
            {
                passive: true
            }
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

        var timeGrid =
            serviceItem.querySelector(
                ".service-time-grid"
            );


        var hiddenTime =
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

            var url =
                "/reservation/blocked-times/" +
                "?barber=" +
                encodeURIComponent(barberId) +
                "&date=" +
                encodeURIComponent(date);


            var response =
                await fetch(url);


            if (!response.ok) {

                throw new Error(
                    "HTTP " +
                    response.status
                );

            }


            var data =
                await response.json();


            console.log(
                "SERVICE RESERVATION DATA:",
                data
            );


            var workingHours =
                data.find(function (item) {

                    return item.type ===
                        "working_hours";

                });


            if (!workingHours) {

                timeGrid.innerHTML =
                    "<p>ساعت کاری آرایشگر پیدا نشد.</p>";

                return;

            }


            var blocked =
                data.filter(function (item) {

                    return item.type ===
                        "blocked";

                });


            var selectedBarberCard =
                serviceItem.querySelector(
                    ".service-barber-card input:checked"
                );


            var duration =
                workingHours.duration;


            if (selectedBarberCard) {

                var barberCard =
                    selectedBarberCard.closest(
                        ".service-barber-card"
                    );


                if (barberCard) {

                    var barberDuration =
                        barberCard.getAttribute(
                            "data-duration"
                        );


                    if (barberDuration) {

                        duration =
                            parseInt(
                                barberDuration,
                                10
                            );

                    }

                }

            }


            createTimes(
                timeGrid,
                hiddenTime,
                blocked,
                workingHours.start,
                workingHours.end,
                duration
            );


            // =================================================
            // ساعت‌ها آماده شدند
            // =================================================

            var selectedTimeBox =
                serviceItem.querySelector(
                    ".selected-service-time"
                );


            if (selectedTimeBox) {

                selectedTimeBox.style.display =
                    "flex";


                var text =
                    selectedTimeBox.querySelector(
                        "span"
                    );


                if (text) {

                    text.innerText =
                        "برای انتخاب ساعت کلیک کنید";

                }


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
        .forEach(function (serviceItem) {

            var serviceCheckbox =
                serviceItem.querySelector(
                    'input[name="services"]'
                );


            var schedule =
                serviceItem.querySelector(
                    ".service-schedule"
                );


            var barberInputs =
                serviceItem.querySelectorAll(
                    ".service-barber-card input"
                );


            var dateInput =
                serviceItem.querySelector(
                    ".service-date-input"
                );


            var selectedDate =
                serviceItem.querySelector(
                    ".service-selected-date"
                );


            var hiddenDate =
                serviceItem.querySelector(
                    ".service-hidden-date"
                );


            var hiddenTime =
                serviceItem.querySelector(
                    ".service-hidden-time"
                );


            var timeGrid =
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
                                function (input) {

                                    input.checked =
                                        false;

                                }
                            );


                            if (hiddenDate) {

                                hiddenDate.value = "";

                            }


                            if (selectedDate) {

                                selectedDate.innerText =
                                    "برای انتخاب تاریخ کلیک کنید";

                            }


                            if (hiddenTime) {

                                hiddenTime.value = "";

                            }


                            if (timeGrid) {

                                timeGrid.innerHTML = "";

                            }


                            resetServiceDetails(
                                serviceItem
                            );

                        }

                    }
                );

            }


            // =================================================
            // انتخاب آرایشگر
            // =================================================

            barberInputs.forEach(
                function (barberInput) {

                    barberInput.addEventListener(
                        "change",
                        function () {

                            console.log(
                                "SELECTED BARBER:",
                                this.value
                            );


                            // =================================================
                            // نمایش قیمت
                            // =================================================

                            var selectedBarberCard =
                                this.closest(
                                    ".service-barber-card"
                                );


                            var selectedBarberPrice =
                                serviceItem.querySelector(
                                    ".selected-barber-price"
                                );


                            var barberPriceValue =
                                serviceItem.querySelector(
                                    ".barber-price-value"
                                );


                            if (
                                selectedBarberCard &&
                                selectedBarberPrice &&
                                barberPriceValue
                            ) {

                                var price =
                                    selectedBarberCard.getAttribute(
                                        "data-price"
                                    );


                                if (price) {

                                    barberPriceValue.innerText =
                                        Number(price)
                                            .toLocaleString(
                                                "fa-IR"
                                            );


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


                            // =================================================
                            // جزئیات مخصوص آرایشگر
                            // =================================================

                            updateServiceDetails(
                                serviceItem,
                                this.value
                            );


                            // =================================================
                            // ریست تاریخ و ساعت
                            // =================================================

                            if (hiddenDate) {

                                hiddenDate.value = "";

                            }


                            if (selectedDate) {

                                selectedDate.innerText =
                                    "برای انتخاب تاریخ کلیک کنید";

                            }


                            if (hiddenTime) {

                                hiddenTime.value = "";

                            }


                            if (timeGrid) {

                                timeGrid.innerHTML = "";

                            }


                            var selectedTimeBox =
                                serviceItem.querySelector(
                                    ".selected-service-time"
                                );


                            if (selectedTimeBox) {

                                selectedTimeBox.style.display =
                                    "flex";


                                var text =
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


            // =====================================================
            // تقویم خدمت
            // =====================================================

            if (dateInput) {

                dateInput.addEventListener(
                    "click",
                    function () {

                        var selectedBarber =
                            serviceItem.querySelector(
                                ".service-barber-card input:checked"
                            );


                        if (!selectedBarber) {

                            alert(
                                "ابتدا آرایشگر این خدمت را انتخاب کنید."
                            );

                            return;

                        }


                        var viewYear =
                            todayJalali.jy;


                        var viewMonth =
                            todayJalali.jm;


                        var modal =
                            document.createElement(
                                "div"
                            );


                        modal.className =
                            "calendar-modal";


                        modal.style.display =
                            "flex";


                        // =================================================
                        // ساخت تقویم بدون Template Literal
                        // =================================================

                        var calendarContent =
                            document.createElement("div");

                        calendarContent.className =
                            "calendar-content";


                        var prev =
                            document.createElement("button");

                        prev.type = "button";

                        prev.className =
                            "service-prev-month";

                        prev.innerText = "❮";


                        var calendarTitle =
                            document.createElement("h3");

                        calendarTitle.className =
                            "service-calendar-title";


                        var next =
                            document.createElement("button");

                        next.type = "button";

                        next.className =
                            "service-next-month";

                        next.innerText = "❯";


                        var close =
                            document.createElement("button");

                        close.type = "button";

                        close.className =
                            "service-close-calendar";

                        close.innerText = "✕";


                        var weekDays =
                            document.createElement("div");

                        weekDays.className =
                            "week-days";


                        var weekNames = [
                            "ش",
                            "ی",
                            "د",
                            "س",
                            "چ",
                            "پ",
                            "ج"
                        ];


                        weekNames.forEach(
                            function (name) {

                                var span =
                                    document.createElement(
                                        "span"
                                    );

                                span.innerText =
                                    name;

                                weekDays.appendChild(
                                    span
                                );

                            }
                        );


                        var calendar =
                            document.createElement("div");

                        calendar.className =
                            "calendar-days service-calendar-days";


                        calendarContent.appendChild(prev);

                        calendarContent.appendChild(
                            calendarTitle
                        );

                        calendarContent.appendChild(next);

                        calendarContent.appendChild(close);

                        calendarContent.appendChild(
                            weekDays
                        );

                        calendarContent.appendChild(
                            calendar
                        );

                        modal.appendChild(
                            calendarContent
                        );


                        document.body.appendChild(
                            modal
                        );


                        // =================================================
                        // نمایش تقویم
                        // =================================================

                        function renderServiceCalendar() {

                            calendar.innerHTML = "";


                            calendarTitle.innerText =
                                monthNames[viewMonth] +
                                " " +
                                viewYear;


                            var monthDays =
                                jalaali.jalaaliMonthLength(
                                    viewYear,
                                    viewMonth
                                );


                            var firstGregorian =
                                jalaali.toGregorian(
                                    viewYear,
                                    viewMonth,
                                    1
                                );


                            var firstDate =
                                new Date(
                                    firstGregorian.gy,
                                    firstGregorian.gm - 1,
                                    firstGregorian.gd
                                );


                            var startDay =
                                firstDate.getDay();


                            startDay =
                                (startDay + 1) % 7;


                            // =================================================
                            // خانه‌های خالی
                            // =================================================

                            for (
                                var i = 0;
                                i < startDay;
                                i++
                            ) {

                                var empty =
                                    document.createElement(
                                        "div"
                                    );


                                empty.className =
                                    "calendar-day empty";


                                calendar.appendChild(
                                    empty
                                );

                            }


                            // =================================================
                            // روزهای ماه
                            // =================================================

                            for (
                                var day = 1;
                                day <= monthDays;
                                day++
                            ) {

                                var dayBox =
                                    document.createElement(
                                        "div"
                                    );


                                dayBox.className =
                                    "calendar-day";


                                dayBox.innerText =
                                    day;


                               let gregorian =
    jalaali.toGregorian(
        viewYear,
        viewMonth,
        day
    );

let selected =
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

let today =
    new Date();

today.setHours(
    0,
    0,
    0,
    0
);

// =================================================
// روز گذشته
// =================================================

if (
    selected < today
) {

    dayBox.style.visibility =
        "hidden";

}

else {

    dayBox.addEventListener(
        "click",
        function () {

            var selectedDay =
                this.innerText;

            var selectedJalaliDate =
                viewYear +
                "/" +
                String(
                    viewMonth
                ).padStart(
                    2,
                    "0"
                ) +
                "/" +
                String(
                    selectedDay
                ).padStart(
                    2,
                    "0"
                );


            if (selectedDate) {

                selectedDate.innerText =
                    selectedJalaliDate;

            }


            if (hiddenDate) {

                hiddenDate.value =
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

            }


            modal.remove();


            var selectedTimeBox =
                serviceItem.querySelector(
                    ".selected-service-time"
                );


            if (
                selectedTimeBox
            ) {

                selectedTimeBox.style.display =
                    "flex";


                var text =
                    selectedTimeBox.querySelector(
                        "span"
                    );


                if (text) {

                    text.innerText =
                        "در حال دریافت ساعت‌ها...";

                }

            }


            if (hiddenDate) {

                loadServiceTimes(
                    serviceItem,
                    selectedBarber.value,
                    hiddenDate.value
                );

            }

        }
    );

}

                                calendar.appendChild(
                                    dayBox
                                );

                            }

                        }


                        // =================================================
                        // ماه قبل
                        // =================================================

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


                        // =================================================
                        // ماه بعد
                        // =================================================

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


                        // =================================================
                        // بستن
                        // =================================================

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

    var params =
        new URLSearchParams(
            window.location.search
        );


    var serviceId =
        params.get("service");


    if (serviceId) {

        var selectedService =
            document.querySelector(
                'input[name="services"][value="' +
                serviceId +
                '"]'
            );


        if (selectedService) {

            selectedService.checked =
                true;


            var content =
                selectedService.closest(
                    ".accordion-content"
                );


            if (content) {

                content.style.display =
                    "block";

            }


            var schedule =
                content
                    ? content.querySelector(
                        ".service-schedule"
                    )
                    : null;


            if (schedule) {

                schedule.style.display =
                    "block";

            }

        }

    }

});