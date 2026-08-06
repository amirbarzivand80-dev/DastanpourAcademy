const productsTab = document.getElementById("products-tab");
const coursesTab = document.getElementById("courses-tab");

const productsSection = document.getElementById("products-section");
const coursesSection = document.getElementById("courses-section");

productsTab.addEventListener("click", () => {

    productsTab.classList.add("active");
    coursesTab.classList.remove("active");

    productsSection.style.display = "block";
    coursesSection.style.display = "none";

});

coursesTab.addEventListener("click", () => {

    coursesTab.classList.add("active");
    productsTab.classList.remove("active");

    productsSection.style.display = "none";
    coursesSection.style.display = "block";

});


document.addEventListener("DOMContentLoaded", () => {

    const favorites = JSON.parse(localStorage.getItem("favorites")) || [];

    const productBox = document.getElementById("favorites-products");
    const courseBox = document.getElementById("favorites-courses");
    const counter = document.querySelector(".cart-title p");
counter.textContent = `${favorites.length} مورد در علاقه‌مندی‌های شما`;
    productBox.innerHTML = "";
    courseBox.innerHTML = "";

    favorites.forEach(item => {

    const card = `
        <a href="${item.url}" class="product-link">

            <div class="product-card">

                <div class="product-image">

    <button class="remove-favorite" data-id="${item.id}">
        <i class="fa-solid fa-heart"></i>
    </button>

    <img src="${item.image}" alt="">

</div>
                <div class="product-info">

                    <h3>${item.name}</h3>

                    <span class="price">
                        ${Number(item.price).toLocaleString("fa-IR")} تومان
                    </span>

                </div>

            </div>

        </a>
    `;

    if(item.type === "product"){
        productBox.innerHTML += card;
    }

    if(item.type === "course"){
        courseBox.innerHTML += card;
    }

});
document.addEventListener("click", function(e){

    const btn = e.target.closest(".remove-favorite");

    if(!btn) return;

    e.preventDefault();
    e.stopPropagation();

    // ادامه کد حذف...

    const id = btn.dataset.id;

    let favorites = JSON.parse(localStorage.getItem("favorites")) || [];

    favorites = favorites.filter(item => item.id != id);

    localStorage.setItem("favorites", JSON.stringify(favorites));

    btn.closest(".product-link").remove();

});
});