document.addEventListener("DOMContentLoaded", () => {

    const buttons = document.querySelectorAll(".services-filter button");
    const cards = document.querySelectorAll(".service-link");
    const searchInput = document.getElementById("serviceSearch");

    function filterCards(category, search=""){

        cards.forEach(link=>{

            const card = link.querySelector(".service-card");

            const cardCategory = card.dataset.category;
            const title = card.querySelector("h3").innerText.toLowerCase();

            const categoryMatch =
                category==="all" ||
                cardCategory===category;

            const searchMatch =
                title.includes(search.toLowerCase());

            if(categoryMatch && searchMatch){

                link.style.display="block";

                setTimeout(()=>{
                    link.classList.remove("hide");
                    link.classList.add("show");
                },20);

            }else{

                link.classList.remove("show");
                link.classList.add("hide");

                setTimeout(()=>{
                    link.style.display="none";
                },300);

            }

        });

    }

    buttons.forEach(button=>{

        button.addEventListener("click",()=>{

            buttons.forEach(btn=>btn.classList.remove("active"));

            button.classList.add("active");

            filterCards(
                button.dataset.filter,
                searchInput.value
            );

        });

    });

    searchInput.addEventListener("keyup",()=>{

        const active =
            document.querySelector(".services-filter .active");

        filterCards(
            active.dataset.filter,
            searchInput.value
        );

    });

});