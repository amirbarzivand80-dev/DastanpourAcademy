document.addEventListener("DOMContentLoaded", function () {

    const openCalendar =
        document.getElementById("openCalendar");

    const calendarModal =
        document.getElementById("calendarModal");

    const calendar =
        document.getElementById("calendar-days");

    const calendarTitle =
        document.getElementById("calendarTitle");

    const prevMonth =
        document.getElementById("prevMonth");

    const nextMonth =
        document.getElementById("nextMonth");

    const selectedDate =
        document.getElementById("selectedDate");

    const hiddenDate =
        document.getElementById("hiddenDate");


    if (!window.jalaali) {

        console.error("JALAALI NOT FOUND");

        return;
    }


    const now = new Date();

    const todayJalali =
        jalaali.toJalaali(
            now.getFullYear(),
            now.getMonth() + 1,
            now.getDate()
        );


    let viewYear =
        todayJalali.jy;

    let viewMonth =
        todayJalali.jm;


    const monthNames = [

        "",
        "فروردین",
        "اردیبهشت",
        "خرداد",
        "تیر",
        "مرداد",
        "شهریور",
        "مهر",
        "آبان",
        "آذر",
        "دی",
        "بهمن",
        "اسفند"

    ];


    function renderCalendar() {

        calendar.innerHTML = "";

        calendarTitle.innerText =
            monthNames[viewMonth] +
            " " +
            viewYear;


        const monthDays =
            jalaali.jalaaliMonthLength(
                viewYear,
                viewMonth
            );


        const firstGregorian =
            jalaali.toGregorian(
                viewYear,
                viewMonth,
                1
            );


        const firstDate =
            new Date(
                firstGregorian.gy,
                firstGregorian.gm - 1,
                firstGregorian.gd
            );


        let startDay =
            firstDate.getDay();

        startDay =
            (startDay + 1) % 7;


        for (
            let i = 0;
            i < startDay;
            i++
        ) {

            const empty =
                document.createElement("div");

            empty.className =
                "calendar-day empty";

            calendar.appendChild(empty);
        }


        for (
            let day = 1;
            day <= monthDays;
            day++
        ) {

            const dayBox =
                document.createElement("div");

            dayBox.className =
                "calendar-day";

            dayBox.innerText =
                day;


            const gregorian =
                jalaali.toGregorian(
                    viewYear,
                    viewMonth,
                    day
                );


            const selected =
                new Date(
                    gregorian.gy,
                    gregorian.gm - 1,
                    gregorian.gd
                );


            const today =
                new Date();

            today.setHours(
                0,
                0,
                0,
                0
            );


            if (selected < today) {

                dayBox.classList.add(
                    "disabled"
                );

            } else {

                dayBox.addEventListener(
                    "click",
                    function () {

                        document
                            .querySelectorAll(
                                ".calendar-day"
                            )
                            .forEach(
                                function (item) {

                                    item.classList.remove(
                                        "active"
                                    );

                                }
                            );


                        dayBox.classList.add(
                            "active"
                        );


                        selectedDate.innerText =
                            viewYear +
                            "/" +
                            String(viewMonth)
                                .padStart(2, "0") +
                            "/" +
                            String(day)
                                .padStart(2, "0");


                        hiddenDate.value =
                            gregorian.gy +
                            "-" +
                            String(gregorian.gm)
                                .padStart(2, "0") +
                            "-" +
                            String(gregorian.gd)
                                .padStart(2, "0");


                        calendarModal.style.display =
                            "none";

                    }
                );

            }


            calendar.appendChild(dayBox);

        }

    }


    openCalendar.addEventListener(
        "click",
        function () {

            calendarModal.style.display =
                "flex";

            renderCalendar();

        }
    );


    prevMonth.addEventListener(
        "click",
        function (e) {

            e.preventDefault();

            viewMonth--;

            if (viewMonth < 1) {

                viewMonth = 12;
                viewYear--;

            }

            renderCalendar();

        }
    );


    nextMonth.addEventListener(
        "click",
        function (e) {

            e.preventDefault();

            viewMonth++;

            if (viewMonth > 12) {

                viewMonth = 1;
                viewYear++;

            }

            renderCalendar();

        }
    );


    window.addEventListener(
        "click",
        function (e) {

            if (
                e.target === calendarModal
            ) {

                calendarModal.style.display =
                    "none";

            }

        }
    );

});