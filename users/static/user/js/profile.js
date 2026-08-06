const toggle = document.getElementById("menu-toggle");
const sidebar = document.getElementById("sidebar");

toggle.addEventListener("click", () => {
    sidebar.classList.toggle("collapsed");
});

const content = document.getElementById("content-area");

const dashboardBtn = document.getElementById("dashboard-btn");
const bookingsBtn = document.getElementById("bookings-btn");
const ordersBtn = document.getElementById("orders-btn");
const coursesBtn = document.getElementById("courses-btn");
const favoritesBtn = document.getElementById("favorites-btn");
const settingsBtn = document.getElementById("settings-btn");

function removeActive() {
    document.querySelectorAll(".sidebar-menu li").forEach(item => {
        item.classList.remove("active");
    });
}
function loadDashboard() { 

    localStorage.setItem("userPage", "dashboard");

    changeContent (`

        <div class="dashboard-cards">

            <div class="card">
                <h3>رزروهای من</h3>
                <span>${userStats.reservations}</span>
            </div>


            <div class="card">
                <h3>سفارش‌های من</h3>
                <span>${userStats.orders}</span>
            </div>


            <div class="card">
                <h3>دوره‌های من</h3>
                <span>${userStats.courses}</span>
            </div>

            <div class="card">
                <h3>علاقه‌مندی‌ها</h3>
                <span>${userStats.favorites}</span>
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
                    👤 ${latestData.reservation.barber}
                </p>


                <p>
                    📅 ${latestData.reservation.date}
                </p>


                <p>
                    🕒 ${latestData.reservation.time}
                </p>


            </div>




            <div class="card">

                <h3>
                    آخرین سفارش
                </h3>


                <p>
                    🛍 شماره سفارش: ${latestData.order.id || "ندارد"}
                </p>


                <p>
                    💰 ${latestData.order.price} تومان
                </p>


                <p>
                    📅 ${latestData.order.date}
                </p>


            </div>


        </div>

    `);

}
function loadBookings(){
   localStorage.setItem("userPage", "bookings");
fetch("/my-bookings/")
.then(res => res.text())
.then(data => {

    changeContent(data);

});

}
function loadOrders(){
    localStorage.setItem("userPage", "orders");
fetch("/my-orders/")
.then(res => res.text())
.then(data => {

    changeContent(data);

});

}
function loadCourses(){
    localStorage.setItem("userPage", "courses");
fetch("/my-courses/")
.then(res => res.text())
.then(data => {

    changeContent(data);

});

}
function loadFavorites(){

    localStorage.setItem("userPage", "favorites");

    fetch("/my-favorites/")
    .then(res => res.text())
    .then(data => {

        changeContent(data);

    });

}
function loadSettings() {
    localStorage.setItem("userPage", "settings");
changeContent(`

<h2 class="page-title">تنظیمات حساب</h2>

<div class="details-card">

<form action="/update-profile/" method="POST">

<input
type="hidden"
name="csrfmiddlewaretoken"
value="${document.querySelector('[name=csrfmiddlewaretoken]').value}">

<div class="detail-row">
<span>📷 عکس پروفایل</span>

<button
type="button"
class="details-btn"
onclick="document.getElementById('realUpload').click()">

تغییر عکس

</button>

</div>

<div class="detail-row">
<span>👤 نام و نام خانوادگی</span>

<input
id="settings_full_name"
type="text"
name="full_name">

</div>

<div class="detail-row">
<span>📱 شماره موبایل</span>

<input
id="settings_phone"
type="text"
name="phone">

</div>

<div class="detail-row">
<span>📍 آدرس</span>

<input
id="settings_address"
type="text"
name="address">

</div>

<div class="detail-row">
<span>🎂 تاریخ تولد</span>

<input
id="settings_birth_date"
type="date"
name="birth_date">

</div>

<div class="detail-row">
<span>💍 تاریخ ازدواج</span>

<input
id="settings_marriage_date"
type="date"
name="marriage_date">

</div>

<div class="detail-row">
<span>👶 تاریخ تولد فرزند</span>

<input
id="settings_child_birth"
type="date"
name="child_birth">

</div>

<div class="detail-row">

<button
type="submit"
class="details-btn save-btn">

ذخیره تغییرات

</button>

</div>

</form>

<hr>

<form
id="uploadForm"
action="/upload-profile-image/"
method="POST"
enctype="multipart/form-data">

<input
type="hidden"
name="csrfmiddlewaretoken"
value="${document.querySelector('[name=csrfmiddlewaretoken]').value}">

<input
type="file"
name="profile_image"
id="realUpload"
hidden
accept="image/*"
onchange="this.form.submit()">

</form>

<div class="detail-row">
<span>🔒 رمز عبور</span>

<button
class="details-btn"
onclick="changePassword()">

تغییر رمز

</button>

</div>

<div class="detail-row">
<span>🚪 خروج از حساب</span>

<button
class="details-btn logout-btn">

خروج

</button>

</div>

</div>



`);
fetch("/profile-data/")
.then(res => res.json())
.then(data => {

    document.getElementById("settings_full_name").value = data.full_name || "";
    document.getElementById("settings_phone").value = data.phone || "";
    document.getElementById("settings_address").value = data.address || "";
    document.getElementById("settings_birth_date").value = data.birth_date || "";
    document.getElementById("settings_marriage_date").value = data.marriage_date || "";
    document.getElementById("settings_child_birth").value = data.child_birth || "";

});

fetch("/profile-data/")
.then(res => res.json())
.then(data => {

    document.getElementById("settings_full_name").value = data.full_name;
    document.getElementById("settings_phone").value = data.phone;
    document.getElementById("settings_address").value = data.address;
    document.getElementById("settings_birth_date").value = data.birth_date;
    document.getElementById("settings_marriage_date").value = data.marriage_date;
    document.getElementById("settings_child_birth").value = data.child_birth;

});

}
dashboardBtn.onclick = () => {
    removeActive();
    dashboardBtn.classList.add("active");
    loadDashboard();
};

bookingsBtn.onclick = () => {
    removeActive();
    bookingsBtn.classList.add("active");
    loadBookings();
};

ordersBtn.onclick = () => {
    removeActive();
    ordersBtn.classList.add("active");
    loadOrders();
};

coursesBtn.onclick = () => {
    removeActive();
    coursesBtn.classList.add("active");
    loadCourses();
};

favoritesBtn.onclick = () => {
    removeActive();
    favoritesBtn.classList.add("active");
    loadFavorites();
};

settingsBtn.onclick = () => {
    removeActive();
    settingsBtn.classList.add("active");
    loadSettings();
};

let savedPage = localStorage.getItem("userPage");

switch(savedPage){

    case "bookings":
        loadBookings();
        break;

    case "orders":
        loadOrders();
        break;

    case "courses":
        loadCourses();
        break;

    case "favorites":
        loadFavorites();
        break;

    case "settings":
        loadSettings();
        break;

    default:
        loadDashboard();

}

function changeContent(html){

    content.style.opacity = "0";

    content.style.transform = "translateY(20px)";

    setTimeout(()=>{

        content.innerHTML = html;


        document.querySelectorAll(".progress-fill").forEach(bar => {

            let progress = bar.dataset.progress;

            bar.style.width = progress + "%";

        });


        content.style.opacity = "1";

        content.style.transform = "translateY(0)";

    },180);

}
function changeContent(html){

    content.style.opacity = "0";

    content.style.transform = "translateY(20px)";

    setTimeout(()=>{

        content.innerHTML = html;


        document.querySelectorAll(".progress-fill").forEach(bar => {

            let progress = bar.dataset.progress;

            bar.style.width = progress + "%";

        });


        content.style.opacity = "1";

        content.style.transform = "translateY(0)";

    },180);

}

function showBookingDetails(){

changeContent(`

<div class="booking-details">

    <button class="back-btn" onclick="loadBookings()">
        ← بازگشت
    </button>

    <h2>جزئیات رزرو</h2>

    <div class="details-card">

        <div class="detail-row">
            <span>💈 سرویس</span>
            <strong>اصلاح مو</strong>
        </div>

        <div class="detail-row">
            <span>👤 آرایشگر</span>
            <strong>احمد داستانپور</strong>
        </div>

        <div class="detail-row">
            <span>📅 تاریخ</span>
            <strong>1406/05/12</strong>
        </div>

        <div class="detail-row">
            <span>🕒 ساعت</span>
            <strong>18:30</strong>
        </div>

        <div class="detail-row">
            <span>💰 مبلغ</span>
            <strong>350,000 تومان</strong>
        </div>

        <div class="detail-row">
            <span>📌 وضعیت</span>
            <strong style="color:#43e97b;">انجام شده</strong>
        </div>

    </div>

`);

}

function showOrderDetails(){

changeContent(`

<div class="booking-details">

<button class="back-btn" onclick="loadOrders()">

← بازگشت

</button>

<h2>جزئیات سفارش</h2>

<div class="details-card">

<div class="detail-row">
<span>🛍 محصول</span>
<strong>واکس مو حرفه‌ای</strong>
</div>

<div class="detail-row">
<span>🔢 کد سفارش</span>
<strong>#2541</strong>
</div>

<div class="detail-row">
<span>💰 مبلغ</span>
<strong>420,000 تومان</strong>
</div>

<div class="detail-row">
<span>📅 تاریخ خرید</span>
<strong>1406/05/10</strong>
</div>

<div class="detail-row">
<span>🚚 وضعیت</span>
<strong style="color:#ffcf5a;">در حال آماده سازی</strong>
</div>

</div>

`);

}

function showCourse(){

changeContent(`

<div class="booking-details">

<button class="back-btn" onclick="loadCourses()">

← بازگشت

</button>

<h2>دوره آموزش اصلاح حرفه‌ای</h2>

<div class="details-card">

<div class="detail-row">
<span>👨‍🏫 مدرس</span>
<strong>احمد داستانپور</strong>
</div>

<div class="detail-row">
<span>📚 تعداد جلسات</span>
<strong>25 جلسه</strong>
</div>

<div class="detail-row">
<span>⏱ مدت زمان</span>
<strong>18 ساعت</strong>
</div>

<div class="detail-row">
<span>📈 پیشرفت</span>
<strong>45%</strong>
</div>

</div>

`);

}
function showFavoriteDetails(){

changeContent(`

<div class="booking-details">

<button class="back-btn" onclick="loadFavorites()">

← بازگشت

</button>

<h2>جزئیات محصول</h2>

<div class="details-card">

<div class="detail-row">
<span>🛍 محصول</span>
<strong>واکس مو حرفه‌ای</strong>
</div>

<div class="detail-row">
<span>🏷 برند</span>
<strong>VGR</strong>
</div>

<div class="detail-row">
<span>💰 قیمت</span>
<strong>420,000 تومان</strong>
</div>

<div class="detail-row">
<span>⭐ امتیاز</span>
<strong>4.9</strong>
</div>

<div class="detail-row">
<span>📦 وضعیت</span>
<strong style="color:#43e97b;">موجود</strong>
</div>

<button class="details-btn" style="margin-top:25px;width:100%;">

افزودن به سبد خرید

</button>

</div>

`);

}

function changeAvatar(){

alert("بعداً به آپلود عکس واقعی وصل می‌شود.");

}
function changePassword(){

changeContent(`

<h2 class="page-title">
تغییر رمز عبور
</h2>


<div class="details-card">


<form method="POST" action="/change-password/">


<input
type="hidden"
name="csrfmiddlewaretoken"
value="${document.querySelector('[name=csrfmiddlewaretoken]').value}">



<div class="detail-row">

<span>
🔑 رمز فعلی
</span>

<input
type="password"
name="old_password"
required>

</div>



<div class="detail-row">

<span>
🔒 رمز جدید
</span>

<input
type="password"
name="new_password1"
required>

</div>



<div class="detail-row">

<span>
🔒 تکرار رمز جدید
</span>

<input
type="password"
name="new_password2"
required>

</div>



<div class="detail-row">


<button
class="details-btn save-btn"
type="submit">

ذخیره رمز جدید

</button>


</div>


</form>


<button
class="back-btn"
onclick="loadSettings()">

← بازگشت

</button>


</div>


`);

}
function showOrderDetail(id){

    fetch("/order/" + id + "/")
    .then(res => res.text())
    .then(data => {

        changeContent(data);

    });

}

function showReservationDetail(id){

    fetch("/reservation/" + id + "/")
    .then(res => res.text())
    .then(data => {

        changeContent(data);

    });

}
function showCourseDetail(id){

    fetch("/my-course/" + id + "/")
    .then(res => res.text())
    .then(data => {

        changeContent(data);

    });

}

function showSessionDetail(id){

    fetch("/session/" + id + "/")
    .then(res => res.text())
    .then(data => {

        changeContent(data);

    });

}

function loadCourseDetail(id){

    fetch("/my-course/" + id + "/")
    .then(res => res.text())
    .then(data => {

        changeContent(data);

    });

}

document.querySelectorAll(".progress-fill").forEach(bar => {

    let progress = bar.dataset.progress;

    bar.style.width = progress + "%";

});