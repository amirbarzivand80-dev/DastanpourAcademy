const swiper = new Swiper(".productSwiper", {
    loop: true,

    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },

    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});

const thumbs = document.querySelectorAll(".product-thumbs img");

thumbs.forEach((thumb, index) => {

    thumb.addEventListener("click", () => {

        swiper.slideToLoop(index);

    });

});