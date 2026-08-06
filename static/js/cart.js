document.querySelectorAll(".cart-item").forEach(item => {

    const minus = item.querySelector(".minus");
    const plus = item.querySelector(".plus");
    const remove = item.querySelector(".cart-remove");

    const quantity = item.querySelector(".quantity");
    const price = item.querySelector(".item-price");

    const basePrice = Number(price.dataset.price);


    if (plus) {

        plus.addEventListener("click", () => {

            let count = Number(quantity.innerText);

            count++;

            quantity.innerText = count;


            const newPrice = basePrice * count;

            price.innerText = newPrice.toLocaleString("fa-IR");
            price.dataset.price = newPrice;


            updateCartDatabase(
                plus.dataset.id,
                count
            );


            updateTotal();

        });

    }



    if (minus) {

        minus.addEventListener("click", () => {

            let count = Number(quantity.innerText);


            if (count > 1) {

                count--;


                quantity.innerText = count;


                const newPrice = basePrice * count;


                price.innerText = newPrice.toLocaleString("fa-IR");
                price.dataset.price = newPrice;


                updateCartDatabase(
                    minus.dataset.id,
                    count
                );


                updateTotal();

            }

        });

    }



    if (remove) {

        remove.addEventListener("click", () => {

            item.remove();

            updateTotal();

            updateCartState();

        });

    }


});





function updateCartDatabase(itemId, quantity) {


    fetch(`/shop/cart/update/${itemId}/`, {

        method: "POST",

        headers: {

            "X-CSRFToken": getCookie("csrftoken"),

            "Content-Type": "application/x-www-form-urlencoded",

        },


        body: `quantity=${quantity}`

    });

}





function getCookie(name) {


    let cookieValue = null;


    if (document.cookie && document.cookie !== "") {


        const cookies = document.cookie.split(";");


        for (let i = 0; i < cookies.length; i++) {


            const cookie = cookies[i].trim();


            if (cookie.startsWith(name + "=")) {


                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );


                break;

            }

        }

    }


    return cookieValue;

}





function updateTotal() {


    let total = 0;


    document.querySelectorAll(".item-price").forEach(item => {


        total += Number(item.dataset.price);


    });



    const subtotal = document.querySelector(".subtotal-price");


    if (subtotal) {

        subtotal.innerText =
            total.toLocaleString("fa-IR") + " تومان";

    }



    const goodsRow = document.querySelector(
        ".summary-row:first-of-type span:last-child"
    );


    if (goodsRow) {

        goodsRow.innerText =
            total.toLocaleString("fa-IR") + " تومان";

    }


}





function updateCartState() {


    const cartLayout = document.querySelector(".cart-layout");

    const emptyCart = document.querySelector(".empty-cart");

    const title = document.querySelector(".cart-title p");



    if (!cartLayout || !emptyCart || !title) {

        return;

    }



    const items = document.querySelectorAll(".cart-item");



    if (items.length === 0) {


        cartLayout.style.display = "none";

        emptyCart.classList.remove("hidden");

        title.innerText =
            "0 محصول در سبد خرید شما";


    } else {


        cartLayout.style.display = "grid";

        emptyCart.classList.add("hidden");


        title.innerText =
            items.length + " محصول در سبد خرید شما";


    }

}





if (document.querySelector(".cart-layout")) {

    updateCartState();

    updateTotal();

}