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
// Counter
// =======================

const counters = document.querySelectorAll(".counter");

const counterObserver = new IntersectionObserver((entries)=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            const counter = entry.target;

            const number = counter.querySelector("span");

            const target = +counter.dataset.target;

            let count = 0;

            const speed = target / 100;

            const update = ()=>{

                count += speed;

                if(count < target){

                    number.innerText = Math.floor(count);

                    requestAnimationFrame(update);

                }else{

                    number.innerText = target + "+";

                }

            }

            update();

            counterObserver.unobserve(counter);

        }

    });

},{
    threshold:.5
});

counters.forEach(counter=>{

    counterObserver.observe(counter);

});