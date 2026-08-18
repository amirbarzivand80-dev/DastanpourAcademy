document.addEventListener("DOMContentLoaded", () => {

    const buttons = document.querySelectorAll(".services-filter button");
    const cards = document.querySelectorAll(".service-link");
    const searchInput = document.getElementById("serviceSearch");


    /* =========================
       FILTER + SEARCH
    ========================= */

    function filterCards(category, search = "") {

        cards.forEach(link => {

            const card = link.querySelector(".service-card");

            const cardCategory = card.dataset.category;
            const title = card.querySelector("h3").innerText.toLowerCase();

            const categoryMatch =
                category === "all" ||
                cardCategory === category;

            const searchMatch =
                title.includes(search.toLowerCase());


            if (categoryMatch && searchMatch) {

                link.style.display = "block";

                setTimeout(() => {

                    link.classList.remove("hide");
                    link.classList.add("show");

                }, 20);

            } else {

                link.classList.remove("show");
                link.classList.add("hide");

                setTimeout(() => {

                    link.style.display = "none";

                }, 300);

            }

        });

    }


    buttons.forEach(button => {

        button.addEventListener("click", () => {

            buttons.forEach(btn =>
                btn.classList.remove("active")
            );

            button.classList.add("active");

            filterCards(
                button.dataset.filter,
                searchInput.value
            );

        });

    });


    searchInput.addEventListener("keyup", () => {

        const active =
            document.querySelector(
                ".services-filter .active"
            );

        filterCards(
            active.dataset.filter,
            searchInput.value
        );

    });


    /* =========================
       SERVICE IMAGE SLIDER
    ========================= */

    cards.forEach(link => {

        const card =
            link.querySelector(".service-card");

        const slides =
            card.querySelectorAll(".service-slide");

        const next =
            card.querySelector(".service-next");

        const prev =
            card.querySelector(".service-prev");

        let current = 0;


        function showSlide(index) {

            if (!slides.length) {
                return;
            }

            slides.forEach(slide => {
                slide.classList.remove("active");
            });

            slides[index].classList.add("active");

        }


        /* =========================
           NEXT
        ========================= */

        if (next) {

            next.addEventListener("click", event => {

                event.preventDefault();
                event.stopPropagation();

                current++;

                if (current >= slides.length) {
                    current = 0;
                }

                showSlide(current);

            });

        }


        /* =========================
           PREVIOUS
        ========================= */

        if (prev) {

            prev.addEventListener("click", event => {

                event.preventDefault();
                event.stopPropagation();

                current--;

                if (current < 0) {
                    current = slides.length - 1;
                }

                showSlide(current);

            });

        }


        /* =========================
           BOOK BUTTON
        ========================= */

        const bookButton =
            card.querySelector(".service-book-btn");

        if (bookButton) {

            bookButton.addEventListener("click", event => {

                event.stopPropagation();

            });

        }


        /* =========================
           CARD CLICK
        ========================= */

        card.addEventListener("click", event => {

            if (
                event.target.closest(".service-slider-btn") ||
                event.target.closest(".service-book-btn")
            ) {
                return;
            }

            window.location.href =
                link.dataset.serviceUrl;

        });

    });

});