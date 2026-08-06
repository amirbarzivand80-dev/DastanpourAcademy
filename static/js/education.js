const tabs = document.querySelectorAll(".tab-btn");
const contents = document.querySelectorAll(".tab-content");


tabs.forEach(tab => {

    tab.addEventListener("click", () => {

        tabs.forEach(btn => btn.classList.remove("active"));
        contents.forEach(content => content.classList.remove("active"));

        tab.classList.add("active");

        document
            .getElementById(tab.dataset.tab)
            .classList.add("active");

    });

});



document.querySelectorAll(".favorite-btn").forEach(btn => {


    btn.addEventListener("click", function (e) {


        e.preventDefault();
        e.stopPropagation();


        const id = this.dataset.id;


        fetch("/academy/course-favorite/" + id + "/")


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