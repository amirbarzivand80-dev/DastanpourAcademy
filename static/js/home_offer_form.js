document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // PRODUCTS
    // =====================================================

    const productButton = document.getElementById("productSelectButton");
    const productMenu = document.getElementById("productSelectMenu");
    const productSearch = document.getElementById("productSearch");
    const productText = document.getElementById("productSelectText");
    const selectedProducts = document.getElementById("selectedProducts");


    // =====================================================
    // COURSES
    // =====================================================

    const courseButton = document.getElementById("courseSelectButton");
    const courseMenu = document.getElementById("courseSelectMenu");
    const courseSearch = document.getElementById("courseSearch");
    const courseText = document.getElementById("courseSelectText");
    const selectedCourses = document.getElementById("selectedCourses");


    // =====================================================
    // PRODUCTS MENU
    // =====================================================

    if (productButton && productMenu) {

        productButton.addEventListener("click", function (event) {

            event.stopPropagation();

            productMenu.classList.toggle("show");

            if (courseMenu) {
                courseMenu.classList.remove("show");
            }

        });


        productMenu.addEventListener("click", function (event) {
            event.stopPropagation();
        });

    }


    // =====================================================
    // COURSES MENU
    // =====================================================

    if (courseButton && courseMenu) {

        courseButton.addEventListener("click", function (event) {

            event.stopPropagation();

            courseMenu.classList.toggle("show");

            if (productMenu) {
                productMenu.classList.remove("show");
            }

        });


        courseMenu.addEventListener("click", function (event) {
            event.stopPropagation();
        });

    }


    // =====================================================
    // CLOSE MENUS
    // =====================================================

    document.addEventListener("click", function () {

        if (productMenu) {
            productMenu.classList.remove("show");
        }

        if (courseMenu) {
            courseMenu.classList.remove("show");
        }

    });


    // =====================================================
    // PRODUCT SEARCH
    // =====================================================

    if (productSearch) {

        productSearch.addEventListener("input", function () {

            const search = this.value
                .trim()
                .toLowerCase();


            document
                .querySelectorAll("#productItems .offer-item")
                .forEach(function (item) {

                    const name =
                        item.dataset.search ||
                        item.textContent ||
                        "";


                    if (
                        name
                            .trim()
                            .toLowerCase()
                            .includes(search)
                    ) {

                        item.style.display = "flex";

                    } else {

                        item.style.display = "none";

                    }

                });

        });

    }


    // =====================================================
    // COURSE SEARCH
    // =====================================================

    if (courseSearch) {

        courseSearch.addEventListener("input", function () {

            const search = this.value
                .trim()
                .toLowerCase();


            document
                .querySelectorAll("#courseItems .offer-item")
                .forEach(function (item) {

                    const name =
                        item.dataset.search ||
                        item.textContent ||
                        "";


                    if (
                        name
                            .trim()
                            .toLowerCase()
                            .includes(search)
                    ) {

                        item.style.display = "flex";

                    } else {

                        item.style.display = "none";

                    }

                });

        });

    }


    // =====================================================
    // PRODUCT CHECKBOXES
    // =====================================================

    document
        .querySelectorAll('input[name="products"]')
        .forEach(function (checkbox) {

            checkbox.addEventListener(
                "change",
                updateProducts
            );

        });


    // =====================================================
    // COURSE CHECKBOXES
    // =====================================================

    document
        .querySelectorAll('input[name="courses"]')
        .forEach(function (checkbox) {

            checkbox.addEventListener(
                "change",
                updateCourses
            );

        });


    // =====================================================
    // UPDATE PRODUCTS
    // =====================================================

    function updateProducts() {

        if (!productText || !selectedProducts) {
            return;
        }


        const checked = document.querySelectorAll(
            'input[name="products"]:checked'
        );


        if (checked.length === 0) {

            productText.textContent =
                "انتخاب محصولات";

        } else {

            productText.textContent =
                `${checked.length} محصول انتخاب شد`;

        }


        selectedProducts.innerHTML = "";


        checked.forEach(function (checkbox) {

            const tag = document.createElement("span");

            tag.className = "offer-selected-tag";


            const name =
                checkbox.dataset.name ||
                checkbox.parentElement.textContent.trim();


            tag.innerHTML = `
                ${name}
                <button
                    type="button"
                    class="remove-offer-item"
                    data-id="${checkbox.value}"
                >
                    ×
                </button>
            `;


            const removeButton =
                tag.querySelector(".remove-offer-item");


            removeButton.addEventListener(
                "click",
                function (event) {

                    event.stopPropagation();

                    checkbox.checked = false;

                    updateProducts();

                }
            );


            selectedProducts.appendChild(tag);

        });

    }


    // =====================================================
    // UPDATE COURSES
    // =====================================================

    function updateCourses() {

        if (!courseText || !selectedCourses) {
            return;
        }


        const checked = document.querySelectorAll(
            'input[name="courses"]:checked'
        );


        if (checked.length === 0) {

            courseText.textContent =
                "انتخاب دوره‌ها";

        } else {

            courseText.textContent =
                `${checked.length} دوره انتخاب شد`;

        }


        selectedCourses.innerHTML = "";


        checked.forEach(function (checkbox) {

            const tag = document.createElement("span");

            tag.className = "offer-selected-tag";


            const name =
                checkbox.dataset.name ||
                checkbox.parentElement.textContent.trim();


            tag.innerHTML = `
                ${name}
                <button
                    type="button"
                    class="remove-offer-item"
                    data-id="${checkbox.value}"
                >
                    ×
                </button>
            `;


            const removeButton =
                tag.querySelector(".remove-offer-item");


            removeButton.addEventListener(
                "click",
                function (event) {

                    event.stopPropagation();

                    checkbox.checked = false;

                    updateCourses();

                }
            );


            selectedCourses.appendChild(tag);

        });

    }


    // =====================================================
    // INITIAL STATE
    // =====================================================

    updateProducts();
    updateCourses();

});