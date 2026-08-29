document.addEventListener("DOMContentLoaded", function () {

    const images = document.querySelectorAll(".course-gallery-image");

    const lightbox = document.getElementById("imageLightbox");

    const lightboxImage = document.getElementById("lightboxImage");

    const closeButton = document.querySelector(".lightbox-close");


    images.forEach(function (image) {

        image.addEventListener("click", function () {

            lightboxImage.src = this.src;

            lightboxImage.alt = this.alt;

            lightbox.classList.add("active");

        });

    });


    closeButton.addEventListener("click", function () {

        lightbox.classList.remove("active");

    });


    lightbox.addEventListener("click", function (event) {

        if (event.target === lightbox) {

            lightbox.classList.remove("active");

        }

    });


    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {

            lightbox.classList.remove("active");

        }

    });

});