const searchInput = document.getElementById("searchInput");
const filterButtons = document.querySelectorAll(".shop-filter button");
const sortSelect = document.getElementById("sortProducts");

const productsGrid = document.querySelector(".products-grid");

const originalCards = Array.from(document.querySelectorAll(".product-link"));

let activeFilter = "all";

function updateProducts() {

    let cards = [...originalCards];

    // ---------- جستجو ----------

    const searchValue = searchInput.value.trim().toLowerCase();

    cards = cards.filter(card => {

        const product = card.querySelector(".product-card");

        const name = product.dataset.name.toLowerCase();

        return name.includes(searchValue);

    });

    // ---------- فیلتر ----------

    if (activeFilter !== "all") {

        cards = cards.filter(card => {

            const product = card.querySelector(".product-card");

            return product.dataset.category === activeFilter;

        });

    }

    // ---------- مرتب سازی ----------

    switch (sortSelect.value) {

        case "cheap":

            cards.sort((a, b) => {

                return Number(a.querySelector(".price").dataset.price) -

                       Number(b.querySelector(".price").dataset.price);

            });

            break;

        case "expensive":

            cards.sort((a, b) => {

                return Number(b.querySelector(".price").dataset.price) -

                       Number(a.querySelector(".price").dataset.price);

            });

            break;

        case "name":

            cards.sort((a, b) => {

                return a.querySelector("h3").innerText.localeCompare(

                    b.querySelector("h3").innerText,

                    "fa"

                );

            });

            break;

        case "available":

            cards.sort((a, b) => {

                const stockA = a.querySelector(".stock").classList.contains("available");

                const stockB = b.querySelector(".stock").classList.contains("available");

                return stockB - stockA;

            });

            break;

    }

    // ---------- نمایش ----------

    productsGrid.innerHTML = "";

    cards.forEach(card => {

        productsGrid.appendChild(card);

    });

}

// ---------- سرچ ----------

searchInput.addEventListener("keyup", updateProducts);

// ---------- فیلتر ----------

filterButtons.forEach(button => {

    button.addEventListener("click", function () {

        filterButtons.forEach(btn => btn.classList.remove("active"));

        this.classList.add("active");

        activeFilter = this.dataset.filter;

        updateProducts();

    });

});

// ---------- مرتب سازی ----------

sortSelect.addEventListener("change", updateProducts);
document.querySelectorAll(".favorite-btn").forEach(btn => {

    btn.addEventListener("click", function (e) {

        e.preventDefault();
        e.stopPropagation();

        const id = this.dataset.id;

        fetch("/shop/favorite/" + id + "/")
        .then(response => {

            if(response.ok){

                this.classList.toggle("active");

                const icon = this.querySelector("i");

                if(this.classList.contains("active")){

                    icon.classList.replace(
                        "fa-regular",
                        "fa-solid"
                    );

                }else{

                    icon.classList.replace(
                        "fa-solid",
                        "fa-regular"
                    );

                }

            }

        });

    });

});