// =====================================================
// USER PANEL
// =====================================================

const toggle = document.getElementById("menu-toggle");
const sidebar = document.getElementById("sidebar");
const content = document.getElementById("content-area");


// =====================================================
// MOBILE SIDEBAR
// =====================================================

if (toggle && sidebar) {

    toggle.addEventListener("click", () => {

        sidebar.classList.toggle("collapsed");

    });

}


// =====================================================
// SIDEBAR BUTTONS
// =====================================================

const dashboardBtn = document.getElementById("dashboard-btn");
const bookingsBtn = document.getElementById("bookings-btn");
const ordersBtn = document.getElementById("orders-btn");
const coursesBtn = document.getElementById("courses-btn");
const favoritesBtn = document.getElementById("favorites-btn");
const settingsBtn = document.getElementById("settings-btn");


// =====================================================
// ACTIVE MENU
// =====================================================

function removeActive() {

    document
        .querySelectorAll(".sidebar-menu li")
        .forEach(item => {

            item.classList.remove("active");

        });

}


// =====================================================
// CHANGE CONTENT
// =====================================================

function changeContent(html) {

    content.style.opacity = "0";
    content.style.transform = "translateY(20px)";

    setTimeout(() => {

        content.innerHTML = html;

        document
            .querySelectorAll(".progress-fill")
            .forEach(bar => {

                const progress =
                    bar.dataset.progress || 0;

                bar.style.width =
                    progress + "%";

            });

        /*
         * اگر صفحه تنظیمات است،
         * تقویم‌ها را بعد از ساخته شدن HTML فعال کن
         */

        if (
            document.querySelector(".profile-date-input")
        ) {

            initializeProfileCalendars();

        }

        content.style.opacity = "1";
        content.style.transform = "translateY(0)";

    }, 180);

}


// =====================================================
// DASHBOARD
// =====================================================

function loadDashboard() {

    localStorage.setItem(
        "userPage",
        "dashboard"
    );

    changeContent(`

        <div class="dashboard-cards">

            <div class="card">

                <h3>
                    رزروهای من
                </h3>

                <span>
                    ${userStats.reservations}
                </span>

            </div>


            <div class="card">

                <h3>
                    سفارش‌های من
                </h3>

                <span>
                    ${userStats.orders}
                </span>

            </div>


            <div class="card">

                <h3>
                    دوره‌های من
                </h3>

                <span>
                    ${userStats.courses}
                </span>

            </div>


            <div class="card">

                <h3>
                    علاقه‌مندی‌ها
                </h3>

                <span>
                    ${userStats.favorites}
                </span>

            </div>

        </div>


        <div class="dashboard-latest">


            <div class="card">

                <h3>
                    آخرین رزرو
                </h3>


                <p>
                    💈 ${latestData.reservation.service}
                </p>


                <p>
                    👤 ${latestData.reservation.barber || "ندارد"}
                </p>


                <p>
                    📅 ${latestData.reservation.date || "ندارد"}
                </p>


                <p>
                    🕒 ${latestData.reservation.time || "ندارد"}
                </p>

            </div>



            <div class="card">

                <h3>
                    آخرین سفارش
                </h3>


                <p>
                    🛍 شماره سفارش:
                    ${latestData.order.id || "ندارد"}
                </p>


                <p>
                    💰 ${latestData.order.price || "0"} تومان
                </p>


                <p>
                    📅 ${latestData.order.date || "ندارد"}
                </p>

            </div>


        </div>

    `);

}


// =====================================================
// BOOKINGS
// =====================================================

function loadBookings() {

    localStorage.setItem(
        "userPage",
        "bookings"
    );

    fetch("/my-bookings/")

        .then(response => {

            if (!response.ok) {
                throw new Error(
                    "خطا در دریافت رزروها"
                );
            }

            return response.text();

        })

        .then(data => {

            changeContent(data);

        })

        .catch(error => {

            console.error(error);

            changeContent(`

                <div class="details-card">

                    <h3>
                        خطا در دریافت رزروها
                    </h3>

                    <p>
                        لطفاً دوباره تلاش کنید.
                    </p>

                </div>

            `);

        });

}


// =====================================================
// ORDERS
// =====================================================

function loadOrders() {

    localStorage.setItem(
        "userPage",
        "orders"
    );

    fetch("/my-orders/")

        .then(response => {

            if (!response.ok) {
                throw new Error(
                    "خطا در دریافت سفارش‌ها"
                );
            }

            return response.text();

        })

        .then(data => {

            changeContent(data);

        })

        .catch(error => {

            console.error(error);

            changeContent(`

                <div class="details-card">

                    <h3>
                        خطا در دریافت سفارش‌ها
                    </h3>

                    <p>
                        لطفاً دوباره تلاش کنید.
                    </p>

                </div>

            `);

        });

}


// =====================================================
// COURSES
// =====================================================

function loadCourses() {

    localStorage.setItem(
        "userPage",
        "courses"
    );

    fetch("/my-courses/")

        .then(response => {

            if (!response.ok) {
                throw new Error(
                    "خطا در دریافت دوره‌ها"
                );
            }

            return response.text();

        })

        .then(data => {

            changeContent(data);

        })

        .catch(error => {

            console.error(error);

            changeContent(`

                <div class="details-card">

                    <h3>
                        خطا در دریافت دوره‌ها
                    </h3>

                    <p>
                        لطفاً دوباره تلاش کنید.
                    </p>

                </div>

            `);

        });

}


// =====================================================
// FAVORITES
// =====================================================

function loadFavorites() {

    localStorage.setItem(
        "userPage",
        "favorites"
    );

    fetch("/my-favorites/")

        .then(response => {

            if (!response.ok) {
                throw new Error(
                    "خطا در دریافت علاقه‌مندی‌ها"
                );
            }

            return response.text();

        })

        .then(data => {

            changeContent(data);

        })

        .catch(error => {

            console.error(error);

            changeContent(`

                <div class="details-card">

                    <h3>
                        خطا در دریافت علاقه‌مندی‌ها
                    </h3>

                    <p>
                        لطفاً دوباره تلاش کنید.
                    </p>

                </div>

            `);

        });

}


// =====================================================
// SETTINGS
// =====================================================

function loadSettings() {

    localStorage.setItem(
        "userPage",
        "settings"
    );


    changeContent(`

        <h2 class="page-title">
            تنظیمات حساب
        </h2>


        <div class="details-card">


            <form
                action="/update-profile/"
                method="POST"
            >

                <input
                    type="hidden"
                    name="csrfmiddlewaretoken"
                    value="${
                        document.querySelector(
                            '[name=csrfmiddlewaretoken]'
                        ).value
                    }"
                >


                <div class="detail-row">

                    <span>
                        👤 نام و نام خانوادگی
                    </span>

                    <input
                        id="settings_full_name"
                        type="text"
                        name="full_name"
                    >

                </div>


                <div class="detail-row">

                    <span>
                        📱 شماره موبایل
                    </span>

                    <input
                        id="settings_phone"
                        type="text"
                        name="phone"
                    >

                </div>


                <div class="detail-row">

                    <span>
                        📍 آدرس
                    </span>

                    <input
                        id="settings_address"
                        type="text"
                        name="address"
                    >

                </div>


                <!-- =========================
                     تاریخ تولد
                ========================== -->

                <div class="detail-row">

                    <span>
                        🎂 تاریخ تولد
                    </span>

                    <div
                        class="profile-date-input"
                        data-target="settings_birth_date"
                    >

                        <span>
                            برای انتخاب تاریخ کلیک کنید
                        </span>

                        <i class="fa-solid fa-calendar-days"></i>

                    </div>

                    <input
                        type="hidden"
                        name="birth_date"
                        id="settings_birth_date"
                    >

                </div>


                <!-- =========================
                     تاریخ ازدواج
                ========================== -->

                <div class="detail-row">

                    <span>
                        💍 تاریخ ازدواج
                    </span>

                    <div
                        class="profile-date-input"
                        data-target="settings_marriage_date"
                    >

                        <span>
                            برای انتخاب تاریخ کلیک کنید
                        </span>

                        <i class="fa-solid fa-calendar-days"></i>

                    </div>

                    <input
                        type="hidden"
                        name="marriage_date"
                        id="settings_marriage_date"
                    >

                </div>


                <!-- =========================
                     تاریخ تولد فرزند
                ========================== -->

                <div class="detail-row">

                    <span>
                        👶 تاریخ تولد فرزند
                    </span>

                    <div
                        class="profile-date-input"
                        data-target="settings_child_birth"
                    >

                        <span>
                            برای انتخاب تاریخ کلیک کنید
                        </span>

                        <i class="fa-solid fa-calendar-days"></i>

                    </div>

                    <input
                        type="hidden"
                        name="child_birth"
                        id="settings_child_birth"
                    >

                </div>


                <div class="detail-row">

                    <button
                        type="submit"
                        class="details-btn save-btn"
                    >

                        ذخیره تغییرات

                    </button>

                </div>

            </form>


            <hr>


            <!-- =========================
                 عکس پروفایل
            ========================== -->

            <form
                id="uploadForm"
                action="/upload-profile-image/"
                method="POST"
                enctype="multipart/form-data"
            >

                <input
                    type="hidden"
                    name="csrfmiddlewaretoken"
                    value="${
                        document.querySelector(
                            '[name=csrfmiddlewaretoken]'
                        ).value
                    }"
                >


                <input
                    type="file"
                    name="profile_image"
                    id="realUpload"
                    hidden
                    accept="image/*"
                    onchange="this.form.submit()"
                >

            </form>


            <div class="detail-row">

                <span>
                    📷 عکس پروفایل
                </span>

                <button
                    type="button"
                    class="details-btn"
                    onclick="
                        document
                        .getElementById('realUpload')
                        .click()
                    "
                >

                    تغییر عکس

                </button>

            </div>


            <!-- =========================
                 تغییر رمز
            ========================== -->

            <div class="detail-row">

                <span>
                    🔒 رمز عبور
                </span>

                <button
                    type="button"
                    class="details-btn"
                    onclick="changePassword()"
                >

                    تغییر رمز

                </button>

            </div>


            <!-- =========================
                 خروج
            ========================== -->

            <div class="detail-row">

                <span>
                    🚪 خروج از حساب
                </span>

                <a
                    href="/logout/"
                    class="details-btn logout-btn"
                >

                    خروج

                </a>

            </div>


        </div>

    `);


    // گرفتن اطلاعات کاربر
    fetch("/profile-data/")

        .then(response => {

            if (!response.ok) {
                throw new Error(
                    "خطا در دریافت اطلاعات کاربر"
                );
            }

            return response.json();

        })

        .then(data => {

            const fullName =
                document.getElementById(
                    "settings_full_name"
                );

            const phone =
                document.getElementById(
                    "settings_phone"
                );

            const address =
                document.getElementById(
                    "settings_address"
                );

            const birth =
                document.getElementById(
                    "settings_birth_date"
                );

            const marriage =
                document.getElementById(
                    "settings_marriage_date"
                );

            const child =
                document.getElementById(
                    "settings_child_birth"
                );


            if (fullName) {
                fullName.value =
                    data.full_name || "";
            }


            if (phone) {
                phone.value =
                    data.phone || "";
            }


            if (address) {
                address.value =
                    data.address || "";
            }


            if (birth) {
                birth.value =
                    data.birth_date || "";
            }


            if (marriage) {
                marriage.value =
                    data.marriage_date || "";
            }


            if (child) {
                child.value =
                    data.child_birth || "";
            }


            // نمایش تاریخ‌های ذخیره شده
            initializeProfileCalendars();

        })

        .catch(error => {

            console.error(error);

        });

}


// =====================================================
// تقویم شمسی پنل کاربر
// =====================================================

function initializeProfileCalendars() {

    console.log("CALENDAR INIT");


    if (!window.jalaali) {

        console.error(
            "Jalaali library پیدا نشد."
        );

        return;

    }


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


    const weekDays = [

        "ش",
        "ی",
        "د",
        "س",
        "چ",
        "پ",
        "ج"

    ];


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


        if (!gy || !gm || !gd) {
            return null;
        }


        return jalaali.toJalaali(
            gy,
            gm,
            gd
        );

    }


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


    function openCalendar(
        displayBox,
        hiddenInput
    ) {

        const now =
            new Date();


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


        const modal =
            document.createElement(
                "div"
            );


        modal.className =
            "profile-calendar-modal";


        modal.innerHTML = `

            <div class="profile-calendar-content">

                <div class="profile-calendar-header">

                    <button
                        type="button"
                        class="profile-prev"
                    >
                        ❮
                    </button>


                    <div class="profile-calendar-title">

                        <select
                            class="profile-year-select"
                        ></select>


                        <span
                            class="profile-month-title"
                        ></span>

                    </div>


                    <button
                        type="button"
                        class="profile-next"
                    >
                        ❯
                    </button>


                    <button
                        type="button"
                        class="profile-calendar-close"
                    >
                        ✕
                    </button>

                </div>


                <div class="profile-calendar-week">

                    ${weekDays.map(
                        day =>
                            `<span>${day}</span>`
                    ).join("")}

                </div>


                <div class="profile-calendar-days"></div>

            </div>

        `;


        document.body.appendChild(
            modal
        );


        const title =
            modal.querySelector(
                ".profile-month-title"
            );


        const yearSelect =
            modal.querySelector(
                ".profile-year-select"
            );


        const daysContainer =
            modal.querySelector(
                ".profile-calendar-days"
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
        // ساخت لیست سال‌ها
        // =================================================

        const currentYear =
            todayJalali.jy;


        const minYear = 1300;
        const maxYear = currentYear + 10;


        for (
            let year = maxYear;
            year >= minYear;
            year--
        ) {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                year;


            option.textContent =
                year;


            yearSelect.appendChild(
                option
            );

        }


        yearSelect.value =
            viewYear;


        // =================================================
        // تغییر سال
        // =================================================

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


        // =================================================
        // نمایش تقویم
        // =================================================

        function renderCalendar() {

            daysContainer.innerHTML =
                "";


            title.innerText =
                monthNames[viewMonth];


            yearSelect.value =
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
                    "profile-calendar-day empty";


                daysContainer.appendChild(
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
                    "profile-calendar-day";


                dayBox.innerText =
                    day;


                const gregorian =
                    jalaali.toGregorian(
                        viewYear,
                        viewMonth,
                        day
                    );


                const isoDate =

                    gregorian.gy +
                    "-" +
                    String(
                        gregorian.gm
                    ).padStart(2, "0") +
                    "-" +
                    String(
                        gregorian.gd
                    ).padStart(2, "0");


                if (
                    hiddenInput.value ===
                    isoDate
                ) {

                    dayBox.classList.add(
                        "selected"
                    );

                }


                dayBox.addEventListener(
                    "click",
                    function () {

                        hiddenInput.value =
                            isoDate;


                        displayBox
                            .querySelector(
                                "span"
                            )
                            .innerText =

                            formatJalali(
                                viewYear,
                                viewMonth,
                                day
                            );


                        modal.remove();

                    }
                );


                daysContainer.appendChild(
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


                yearSelect.value =
                    viewYear;


                renderCalendar();

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


                yearSelect.value =
                    viewYear;


                renderCalendar();

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


        renderCalendar();

    }


    document
        .querySelectorAll(
            ".profile-date-input"
        )
        .forEach(
            function (displayBox) {

                // جلوگیری از اتصال دوباره
                if (
                    displayBox.dataset.calendarReady === "true"
                ) {

                    return;

                }


                displayBox.dataset.calendarReady =
                    "true";


                const target =
                    displayBox.dataset.target;


                const hiddenInput =
                    document.getElementById(
                        target
                    );


                if (!hiddenInput) {
                    return;
                }


                const existing =
                    gregorianToJalali(
                        hiddenInput.value
                    );


                if (existing) {

                    displayBox
                        .querySelector(
                            "span"
                        )
                        .innerText =

                        formatJalali(

                            existing.jy,
                            existing.jm,
                            existing.jd

                        );

                }


                displayBox.addEventListener(
                    "click",
                    function (event) {

                        event.preventDefault();
                        event.stopPropagation();

                        console.log(
                            "DATE BOX CLICKED"
                        );

                        openCalendar(
                            displayBox,
                            hiddenInput
                        );

                    },
                    true
                );

            }
        );

}


// =====================================================
// CHANGE PASSWORD
// =====================================================

function changePassword() {

    changeContent(`

        <h2 class="page-title">
            تغییر رمز عبور
        </h2>


        <div class="details-card">


            <form
                method="POST"
                action="/change-password/"
            >

                <input
                    type="hidden"
                    name="csrfmiddlewaretoken"
                    value="${
                        document.querySelector(
                            '[name=csrfmiddlewaretoken]'
                        ).value
                    }"
                >


                <div class="detail-row">

                    <span>
                        🔑 رمز فعلی
                    </span>

                    <input
                        type="password"
                        name="old_password"
                        required
                    >

                </div>


                <div class="detail-row">

                    <span>
                        🔒 رمز جدید
                    </span>

                    <input
                        type="password"
                        name="new_password1"
                        required
                    >

                </div>


                <div class="detail-row">

                    <span>
                        🔒 تکرار رمز جدید
                    </span>

                    <input
                        type="password"
                        name="new_password2"
                        required
                    >

                </div>


                <div class="detail-row">

                    <button
                        class="details-btn save-btn"
                        type="submit"
                    >

                        ذخیره رمز جدید

                    </button>

                </div>


            </form>


            <button
                class="back-btn"
                onclick="loadSettings()"
            >

                ← بازگشت

            </button>


        </div>

    `);

}


// =====================================================
// ORDER DETAIL
// =====================================================

function showOrderDetail(id) {

    fetch(
        "/order/" + id + "/"
    )

        .then(res => res.text())

        .then(data => {

            changeContent(data);

        })

        .catch(error => {

            console.error(error);

        });

}


// =====================================================
// RESERVATION DETAIL
// =====================================================

function showReservationDetail(id) {

    fetch(
        "/reservation/" + id + "/"
    )

        .then(res => res.text())

        .then(data => {

            changeContent(data);

        })

        .catch(error => {

            console.error(error);

        });

}


// =====================================================
// COURSE DETAIL
// =====================================================

function showCourseDetail(id) {

    fetch(
        "/my-course/" + id + "/"
    )

        .then(res => res.text())

        .then(data => {

            changeContent(data);

        })

        .catch(error => {

            console.error(error);

        });

}


// =====================================================
// SESSION DETAIL
// =====================================================

function showSessionDetail(id) {

    fetch(
        "/session/" + id + "/"
    )

        .then(res => res.text())

        .then(data => {

            changeContent(data);

        })

        .catch(error => {

            console.error(error);

        });

}


// =====================================================
// COURSE DETAIL
// =====================================================

function loadCourseDetail(id) {

    fetch(
        "/my-course/" + id + "/"
    )

        .then(res => res.text())

        .then(data => {

            changeContent(data);

        })

        .catch(error => {

            console.error(error);

        });

}


// =====================================================
// MENU EVENTS
// =====================================================

if (dashboardBtn) {

    dashboardBtn.onclick = () => {

        removeActive();

        dashboardBtn.classList.add(
            "active"
        );

        loadDashboard();

    };

}


if (bookingsBtn) {

    bookingsBtn.onclick = () => {

        removeActive();

        bookingsBtn.classList.add(
            "active"
        );

        loadBookings();

    };

}


if (ordersBtn) {

    ordersBtn.onclick = () => {

        removeActive();

        ordersBtn.classList.add(
            "active"
        );

        loadOrders();

    };

}


if (coursesBtn) {

    coursesBtn.onclick = () => {

        removeActive();

        coursesBtn.classList.add(
            "active"
        );

        loadCourses();

    };

}


if (favoritesBtn) {

    favoritesBtn.onclick = () => {

        removeActive();

        favoritesBtn.classList.add(
            "active"
        );

        loadFavorites();

    };

}


if (settingsBtn) {

    settingsBtn.onclick = () => {

        removeActive();

        settingsBtn.classList.add(
            "active"
        );

        loadSettings();

    };

}


// =====================================================
// RESTORE LAST PAGE
// =====================================================

const savedPage =
    localStorage.getItem(
        "userPage"
    );


switch (savedPage) {

    case "bookings":

        removeActive();

        bookingsBtn?.classList.add("active");

        loadBookings();

        break;


    case "orders":

        removeActive();

        ordersBtn?.classList.add("active");

        loadOrders();

        break;


    case "courses":

        removeActive();

        coursesBtn?.classList.add("active");

        loadCourses();

        break;


    case "favorites":

        removeActive();

        favoritesBtn?.classList.add("active");

        loadFavorites();

        break;


    case "settings":

        removeActive();

        settingsBtn?.classList.add("active");

        loadSettings();

        break;


    default:

        removeActive();

        dashboardBtn?.classList.add("active");

        loadDashboard();

}


// =====================================================
// PROGRESS BAR
// =====================================================

document
    .querySelectorAll(".progress-fill")
    .forEach(bar => {

        const progress =
            bar.dataset.progress || 0;

        bar.style.width =
            progress + "%";

    });