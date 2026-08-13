document.addEventListener("DOMContentLoaded", function () {

    const dropdown =
        document.querySelector(".about-dropdown");

    const link =
        document.querySelector(".about-link");


    if (!dropdown || !link) {
        return;
    }


    /* =================================
       Click روی درباره ما
    ================================= */

    link.addEventListener("click", function (event) {

        /*
        در دسکتاپ هم Click باعث باز شدن
        می‌شود و لینک about فعلاً
        مستقیماً اجرا نمی‌شود.
        */

        event.preventDefault();

        dropdown.classList.toggle("open");

    });


    /* =================================
       کلیک بیرون از Dropdown
    ================================= */

    document.addEventListener("click", function (event) {

        if (!dropdown.contains(event.target)) {

            dropdown.classList.remove("open");

        }

    });


    /* =================================
       جلوگیری از بسته شدن هنگام
       کلیک داخل Dropdown
    ================================= */

    const menu =
        document.querySelector(".about-menu");

    if (menu) {

        menu.addEventListener("click", function (event) {

            event.stopPropagation();

        });

    }

});