

// =======================
// Reveal Cards
// =======================
console.log("JS OK");

const cards = document.querySelectorAll(".card");

const observer = new IntersectionObserver((entries)=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            entry.target.classList.add("show");

        }

    });

},{
    threshold:.2
});

cards.forEach(card=>{
    observer.observe(card);
});
// =======================
// HOME STATS COUNTER
// =======================

const counters = document.querySelectorAll(".home-achievement-card .counter");

const counterObserver = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (!entry.isIntersecting) return;

        const counter = entry.target;
        const target = Number(counter.dataset.target);

        const duration = 1500;
        const startTime = performance.now();

        const updateCounter = (currentTime) => {

            const progress = Math.min(
                (currentTime - startTime) / duration,
                1
            );

            const current = Math.floor(target * progress);

            counter.innerText = current.toLocaleString("fa-IR");

            if (progress < 1) {

                requestAnimationFrame(updateCounter);

            } else {

                counter.innerText =
                    target.toLocaleString("fa-IR") + "+";

            }

        };

        requestAnimationFrame(updateCounter);

        counterObserver.unobserve(counter);

    });

}, {
    threshold: 0.3
});


counters.forEach(counter => {
    counterObserver.observe(counter);
});
// =====================================================
// HOME SHOWCASE - TRUE INFINITE RAIL
// 3 CARDS MOVE -> 3 CARDS ENTER
// =====================================================

document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".showcase-slider").forEach(slider => {

        const track = slider.querySelector(".showcase-track");

        if (!track) return;

        const cards = Array.from(
            track.querySelectorAll(".showcase-card")
        );

        const total = cards.length;

        if (total <= 3) return;


        // =================================================
        // STATE
        // =================================================

        let moving = false;
        let timer = null;


        // =================================================
        // CARD STEP
        // =================================================

        function getStep() {

            const card = track.querySelector(".showcase-card");

            if (!card) return 0;

            const cardWidth =
                card.getBoundingClientRect().width;

            const gap =
                parseFloat(
                    getComputedStyle(track).gap
                ) || 0;

            return cardWidth + gap;
        }


        // =================================================
        // MOVE TRACK
        // =================================================

        function move(distance, animate = true) {

            track.style.transition = animate
                ? "transform 900ms ease-in-out"
                : "none";

            track.style.transform =
                `translate3d(${distance}px, 0, 0)`;
        }


        // =================================================
        // NEXT
        // =================================================

        function next() {

            if (moving) return;

            moving = true;

            const step = getStep();

            if (!step) {

                moving = false;

                return;

            }


            // ---------------------------------------------
            // سه کارت اول را مشخص می‌کنیم
            // ---------------------------------------------

            const leavingCards =
                Array.from(
                    track.children
                ).slice(0, 3);


            // ---------------------------------------------
            // حرکت 3 کارت
            // ---------------------------------------------

            move(step * 3, true);


            // ---------------------------------------------
            // بعد از تمام شدن انیمیشن
            // ---------------------------------------------

            setTimeout(() => {

                /*
                 * کارت‌هایی که از صفحه خارج شدند
                 * واقعاً می‌روند انتهای صف.
                 */

                leavingCards.forEach(card => {

                    track.appendChild(card);

                });


                /*
                 * حالا چون 3 کارت اول حذف شده‌اند،
                 * موقعیت track را بدون انیمیشن
                 * به صفر برمی‌گردانیم.
                 *
                 * بنابراین پرش دیده نمی‌شود.
                 */

                move(0, false);


                moving = false;

            }, 930);

        }


        // =================================================
        // PREVIOUS
        // =================================================

        function previous() {

            if (moving) return;

            moving = true;

            const step = getStep();

            if (!step) {

                moving = false;

                return;

            }


            // ---------------------------------------------
            // سه کارت آخر را می‌آوریم ابتدای صف
            // ---------------------------------------------

            const allCards =
                Array.from(
                    track.querySelectorAll(".showcase-card")
                );

            const enteringCards =
                allCards.slice(-3);


            enteringCards.reverse().forEach(card => {

                track.prepend(card);

            });


            /*
             * چون سه کارت جدید را اول صف گذاشتیم،
             * ابتدا track را 3 کارت جابه‌جا می‌کنیم
             * تا آن‌ها خارج از دید باشند.
             */

            move(-step * 3, false);


            // ---------------------------------------------
            // حالا انیمیشن ورود
            // ---------------------------------------------

            requestAnimationFrame(() => {

                requestAnimationFrame(() => {

                    move(0, true);

                });

            });


            setTimeout(() => {

                moving = false;

            }, 930);

        }


        // =================================================
        // AUTO PLAY
        // =================================================

        function startAuto() {

            stopAuto();

            timer = setInterval(() => {

                next();

            }, 3900);

        }


        function stopAuto() {

            if (timer) {

                clearInterval(timer);

                timer = null;

            }

        }


        // =================================================
        // NEXT BUTTON
        // =================================================

        const nextButton =
            slider.parentElement.querySelector(
                ".showcase-next"
            );


        if (nextButton) {

            nextButton.addEventListener("click", () => {

                stopAuto();

                next();

                setTimeout(() => {

                    startAuto();

                }, 1000);

            });

        }


        // =================================================
        // PREVIOUS BUTTON
        // =================================================

        const prevButton =
            slider.parentElement.querySelector(
                ".showcase-prev"
            );


        if (prevButton) {

            prevButton.addEventListener("click", () => {

                stopAuto();

                previous();

                setTimeout(() => {

                    startAuto();

                }, 1000);

            });

        }


        // =================================================
        // HOVER
        // =================================================

        slider.addEventListener(
            "mouseenter",
            stopAuto
        );


        slider.addEventListener(
            "mouseleave",
            startAuto
        );


        // =================================================
        // START
        // =================================================

        move(0, false);

        startAuto();

    });

});

// =======================
// CLICK ON PRODUCT CARD
// =======================

document.querySelectorAll(".showcase-card").forEach(card => {

    card.addEventListener("click", function (e) {

        // اگر روی خرید سریع کلیک شد، رفتار قبلی حفظ شود
        if (e.target.closest(".quick-buy")) {
            return;
        }

        const url = card.dataset.productUrl;

        if (url) {
            window.location.href = url;
        }

    });

});