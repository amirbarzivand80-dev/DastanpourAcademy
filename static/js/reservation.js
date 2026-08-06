document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".accordion").forEach(button => {

        button.addEventListener("click", function () {

            const content = this.nextElementSibling;

            document.querySelectorAll(".accordion-content").forEach(item => {

                if (item !== content) {
                    item.style.display = "none";
                }

            });

            content.style.display =
                content.style.display === "block"
                    ? "none"
                    : "block";

        });

    });

    const openCalendar = document.getElementById("openCalendar");
    const calendarModal = document.getElementById("calendarModal");
    const closeCalendar = document.getElementById("closeCalendar");

    const calendar = document.getElementById("calendar-days");
    const selectedDate = document.getElementById("selectedDate");

    const hiddenDate = document.getElementById("hiddenDate");
    const hiddenTime = document.getElementById("hiddenTime");

    const timeSection = document.getElementById("timeSection");
    const timeGrid = document.getElementById("timeGrid");

    openCalendar.onclick = function () {
        calendarModal.style.display = "flex";
    };

    closeCalendar.onclick = function () {
        calendarModal.style.display = "none";
    };

    window.onclick = function (e) {

        if (e.target === calendarModal) {
            calendarModal.style.display = "none";
        }

    };

    function createTimes(blocked = []) {

        timeGrid.innerHTML = "";

        let hour = 9;
        let minute = 0;

        while (hour < 21) {

            let time =
                String(hour).padStart(2, "0") +
                ":" +
                String(minute).padStart(2, "0");

            let hide = false;

            blocked.forEach(item => {

                if (
                    time >= item.start &&
                    time < item.end
                ) {
                    hide = true;
                }

            });

            if (!hide) {

                const btn = document.createElement("button");

                btn.type = "button";

                btn.className = "time-btn";

                btn.innerText = time;

                btn.addEventListener("click", function () {

                    document
                        .querySelectorAll(".time-btn")
                        .forEach(b => {

                            b.classList.remove("active");

                        });

                    btn.classList.add("active");

                    hiddenTime.value = time;

                });

                timeGrid.appendChild(btn);

            }

            minute += 30;

            if (minute === 60) {

                minute = 0;
                hour++;

            }

        }

    }

    async function loadBlockedTimes() {

        const barber = document.querySelector(
            "input[name='barber']:checked"
        );

        if (!barber || !hiddenDate.value) {

            createTimes([]);
            return;

        }

        const response = await fetch(
            `/reservation/blocked-times/?barber=${barber.value}&date=${hiddenDate.value}`
        );

        const blocked = await response.json();

        createTimes(blocked);

    }

    calendar.innerHTML = "";

    for (let i = 1; i <= 31; i++) {

        const day = document.createElement("div");

        day.className = "calendar-day";

        day.innerText = i;

        day.addEventListener("click", function () {

            document
                .querySelectorAll(".calendar-day")
                .forEach(d => {

                    d.classList.remove("active");

                });

            day.classList.add("active");

           const jalaliDate =
    "1405/05/" +
    String(i).padStart(2, "0");

const gregorianDates = {
    "1405/05/01":"2026-07-23",
    "1405/05/02":"2026-07-24",
    "1405/05/03":"2026-07-25",
    "1405/05/04":"2026-07-26",
    "1405/05/05":"2026-07-27",
    "1405/05/06":"2026-07-28",
    "1405/05/07":"2026-07-29",
    "1405/05/08":"2026-07-30",
    "1405/05/09":"2026-07-31",
    "1405/05/10":"2026-08-01",
    "1405/05/11":"2026-08-02",
    "1405/05/12":"2026-08-03",
    "1405/05/13":"2026-08-04",
    "1405/05/14":"2026-08-05",
    "1405/05/15":"2026-08-06",
    "1405/05/16":"2026-08-07",
    "1405/05/17":"2026-08-08",
    "1405/05/18":"2026-08-09",
    "1405/05/19":"2026-08-10",
    "1405/05/20":"2026-08-11",
    "1405/05/21":"2026-08-12",
    "1405/05/22":"2026-08-13",
    "1405/05/23":"2026-08-14",
    "1405/05/24":"2026-08-15",
    "1405/05/25":"2026-08-16",
    "1405/05/26":"2026-08-17",
    "1405/05/27":"2026-08-18",
    "1405/05/28":"2026-08-19",
    "1405/05/29":"2026-08-20",
    "1405/05/30":"2026-08-21",
    "1405/05/31":"2026-08-22"
};

selectedDate.innerText = jalaliDate;

hiddenDate.value = gregorianDates[jalaliDate];

            calendarModal.style.display = "none";

            timeSection.style.display = "block";

            loadBlockedTimes();

        });

        calendar.appendChild(day);

    }

    document
        .querySelectorAll("input[name='barber']")
        .forEach(item => {

            item.addEventListener(
                "change",
                loadBlockedTimes
            );

        });

});