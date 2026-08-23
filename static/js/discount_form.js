document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // ساخت Dropdown چند انتخابی
    // =====================================================

    function createMultiSelect(selectId) {

        const select = document.getElementById(selectId);

        if (!select) {
            console.error("SELECT پیدا نشد:", selectId);
            return;
        }

        if (select.dataset.dropdownReady === "true") {
            return;
        }

        select.dataset.dropdownReady = "true";


        // =================================================
        // Wrapper
        // =================================================

        const wrapper = document.createElement("div");

        wrapper.className = "discount-multi-select";


        // =================================================
        // دکمه اصلی
        // =================================================

        const button = document.createElement("button");

        button.type = "button";

        button.className = "discount-multi-select-button";

        button.innerHTML = `
            <span class="discount-multi-select-text">
                انتخاب کنید
            </span>

            <i class="fa-solid fa-chevron-down"></i>
        `;


        // =================================================
        // منو
        // =================================================

        const menu = document.createElement("div");

        menu.className = "discount-multi-select-menu";


        // =================================================
        // گزینه‌ها
        // =================================================

        Array.from(select.options).forEach(function (option) {

            const item = document.createElement("label");

            item.className = "discount-multi-select-item";


            const checkbox = document.createElement("input");

            checkbox.type = "checkbox";

            checkbox.value = option.value;

            checkbox.checked = option.selected;


            const checkmark = document.createElement("span");

            checkmark.className = "discount-multi-select-check";


            const text = document.createElement("span");

            text.className = "discount-multi-select-label";

            text.textContent = option.textContent;


            checkbox.addEventListener("change", function () {

                option.selected = checkbox.checked;

                updateButton();

                select.dispatchEvent(
                    new Event("change", {
                        bubbles: true
                    })
                );

            });


            item.appendChild(checkbox);

            item.appendChild(checkmark);

            item.appendChild(text);

            menu.appendChild(item);

        });


        // =================================================
        // بروزرسانی متن دکمه
        // =================================================

        function updateButton() {

            const selected = Array.from(select.options)
                .filter(function (option) {

                    return option.selected;

                });


            const textElement =
                button.querySelector(
                    ".discount-multi-select-text"
                );


            if (!selected.length) {

                textElement.textContent =
                    "انتخاب کنید";

            }

            else if (selected.length === 1) {

                textElement.textContent =
                    selected[0].textContent;

            }

            else {

                textElement.textContent =
                    selected.length +
                    " مورد انتخاب شده";

            }

        }


        // =================================================
        // باز / بسته شدن
        // =================================================

        button.addEventListener("click", function (event) {

            event.preventDefault();

            event.stopPropagation();


            // بستن بقیه منوها

            document
                .querySelectorAll(
                    ".discount-multi-select.open"
                )
                .forEach(function (other) {

                    if (other !== wrapper) {

                        other.classList.remove("open");

                    }

                });


            wrapper.classList.toggle("open");

        });


        // جلوگیری از بسته شدن هنگام کلیک داخل منو

        menu.addEventListener(
            "click",
            function (event) {

                event.stopPropagation();

            }
        );


        // =================================================
        // کلیک بیرون
        // =================================================

        document.addEventListener(
            "click",
            function () {

                wrapper.classList.remove("open");

            }
        );


        // =================================================
        // قرار دادن در صفحه
        // =================================================

        wrapper.appendChild(button);

        wrapper.appendChild(menu);


        select.parentNode.insertBefore(
            wrapper,
            select
        );


        // Select اصلی مخفی شود

        select.style.display = "none";


        updateButton();

    }


    // =====================================================
    // نمایش / مخفی کردن انتخاب خاص
    // =====================================================

    function setupTarget(
        radioName,
        boxId,
        selectId
    ) {

        const radios = document.querySelectorAll(
            'input[name="' + radioName + '"]'
        );


        const box =
            document.getElementById(boxId);


        if (!box) {

            console.error(
                "BOX پیدا نشد:",
                boxId
            );

            return;

        }


        if (!radios.length) {

            console.error(
                "RADIO پیدا نشد:",
                radioName
            );

            return;

        }


        createMultiSelect(selectId);


        function update() {

            let selected = "";


            radios.forEach(function (radio) {

                if (radio.checked) {

                    selected = radio.value;

                }

            });


            if (selected === "selected") {

                box.style.display = "block";

            }

            else {

                box.style.display = "none";

            }

        }


        radios.forEach(function (radio) {

            radio.addEventListener(
                "change",
                update
            );

        });


        update();

    }


    // =====================================================
    // محصولات
    // =====================================================

    setupTarget(
        "product_target",
        "products-selection",
        "id_products"
    );


    // =====================================================
    // دوره‌ها
    // =====================================================

    setupTarget(
        "course_target",
        "courses-selection",
        "id_courses"
    );


    // =====================================================
    // خدمات
    // =====================================================

    setupTarget(
        "service_target",
        "services-selection",
        "id_services"
    );


    // =====================================================
    // کاربران
    // =====================================================

    setupTarget(
        "user_target",
        "users-selection",
        "id_users"
    );

});