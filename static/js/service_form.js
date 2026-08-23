document.addEventListener("DOMContentLoaded", function () {

    const addButton = document.getElementById("add-detail-btn");
    const container = document.getElementById("service-details");

    if (!addButton || !container) {
        return;
    }


    // =====================================================
    // شماره Detail بعدی
    // =====================================================

    let detailIndex = 0;

    document.querySelectorAll(".detail-row").forEach(function (row) {

        const indexInput = row.querySelector(
            'input[name="detail_indexes"]'
        );

        if (indexInput) {

            const index = parseInt(
                indexInput.value,
                10
            );

            if (!isNaN(index) && index > detailIndex) {
                detailIndex = index;
            }
        }

    });


    // =====================================================
    // دریافت آرایشگرهای اصلی خدمت
    // =====================================================

    function getBarbers() {

        const barberInputs = document.querySelectorAll(
            'input[name="barbers"]'
        );

        const barbers = [];

        barberInputs.forEach(function (input) {

            const label = input.closest("label");

            let name = "";

            if (label) {
                name = label.textContent.trim();
            }

            barbers.push({

                id: input.value,

                name: name,

                selected: input.checked

            });

        });

        return barbers;
    }


    // =====================================================
    // ساخت HTML آرایشگر برای Detail
    // =====================================================

    function createBarberHTML(
        detailIndex,
        barber,
        selected = false,
        price = "",
        duration = 10
    ) {

        return `

            <div
                class="detail-barber-row"
                data-barber-id="${barber.id}"
                style="
                    display:flex;
                    gap:15px;
                    align-items:center;
                    margin-top:10px;
                    flex-wrap:wrap;
                "
            >

                <label>

                    <input
                        type="checkbox"
                        name="detail_barber_${detailIndex}_${barber.id}"
                        ${selected ? "checked" : ""}
                    >

                    ${barber.name}

                </label>


                <input
                    type="number"
                    name="detail_price_${detailIndex}_${barber.id}"
                    value="${price}"
                    placeholder="قیمت"
                    min="0"
                    style="
                        width:120px;
                        padding:7px;
                    "
                >

                <span>
                    تومان
                </span>


                <input
                    type="number"
                    name="detail_duration_${detailIndex}_${barber.id}"
                    value="${duration}"
                    placeholder="مدت"
                    min="1"
                    style="
                        width:100px;
                        padding:7px;
                    "
                >

                <span>
                    دقیقه
                </span>

            </div>

        `;
    }


    // =====================================================
    // اضافه کردن آرایشگر جدید به Detailهای قبلی
    // =====================================================

    function addBarberToExistingDetails(barber) {

        document.querySelectorAll(".detail-row").forEach(function (row) {

            const indexInput = row.querySelector(
                'input[name="detail_indexes"]'
            );

            if (!indexInput) {
                return;
            }

            const currentIndex = indexInput.value;

            const barberSection = row.querySelector(
                ".detail-barbers-container"
            );

            if (!barberSection) {
                return;
            }

            // اگر قبلاً وجود دارد، دوباره اضافه نکن
            if (
                barberSection.querySelector(
                    `[data-barber-id="${barber.id}"]`
                )
            ) {
                return;
            }

            barberSection.insertAdjacentHTML(
                "beforeend",
                createBarberHTML(
                    currentIndex,
                    barber,
                    false,
                    "",
                    10
                )
            );

        });

    }


    // =====================================================
    // حذف آرایشگر از Detailهای قبلی
    // =====================================================

    function removeBarberFromExistingDetails(barberId) {

        document.querySelectorAll(".detail-row").forEach(function (row) {

            const barberRow = row.querySelector(
                `.detail-barber-row[data-barber-id="${barberId}"]`
            );

            if (barberRow) {
                barberRow.remove();
            }

        });

    }


    // =====================================================
    // وقتی آرایشگر اصلی تغییر کرد
    // =====================================================

    document
        .querySelectorAll('input[name="barbers"]')
        .forEach(function (barberInput) {

            barberInput.addEventListener(
                "change",
                function () {

                    const label = barberInput.closest("label");

                    let name = "";

                    if (label) {
                        name = label.textContent.trim();
                    }

                    const barber = {

                        id: barberInput.value,

                        name: name,

                        selected: barberInput.checked

                    };


                    if (barberInput.checked) {

                        addBarberToExistingDetails(
                            barber
                        );

                    } else {

                        removeBarberFromExistingDetails(
                            barber.id
                        );

                    }

                }
            );

        });


    // =====================================================
    // افزودن Detail جدید
    // =====================================================

    addButton.addEventListener(
        "click",
        function () {

            detailIndex++;

            const row = document.createElement("div");

            row.className = "detail-row";

            row.style.cssText = `
                border:1px solid #ddd;
                border-radius:8px;
                padding:15px;
                margin:10px 0;
            `;


            // -------------------------------------------------
            // ساخت آرایشگرهای Detail
            // -------------------------------------------------

            let barberHTML = "";

            const barbers = getBarbers();

            barbers
                .filter(function (barber) {
                    return barber.selected;
                })
                .forEach(function (barber) {

                    barberHTML += createBarberHTML(
                        detailIndex,
                        barber,
                        false,
                        "",
                        10
                    );

                });


            // -------------------------------------------------
            // HTML کامل Detail
            // -------------------------------------------------

            row.innerHTML = `

                <input
                    type="hidden"
                    name="detail_indexes"
                    value="${detailIndex}"
                >


                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                ">

                    <h4>
                        جزئیات ${detailIndex}
                    </h4>


                    <button
                        type="button"
                        class="remove-detail-btn"
                        style="
                            padding:6px 12px;
                            cursor:pointer;
                        "
                    >
                        حذف جزئیات
                    </button>

                </div>


                <div>

                    <label>
                        نام جزئیات:
                    </label>

                    <input
                        type="text"
                        name="detail_name_${detailIndex}"
                        placeholder="مثلاً اصلاح ریش"
                        style="
                            width:200px;
                            padding:8px;
                        "
                    >

                </div>


                <div style="margin-top:10px;">

                    <label>
                        توضیحات:
                    </label>

                    <input
                        type="text"
                        name="detail_description_${detailIndex}"
                        placeholder="توضیح کوتاه"
                        style="
                            width:300px;
                            padding:8px;
                        "
                    >

                </div>


                <div style="margin-top:10px;">

                    <label>
                        ترتیب:
                    </label>

                    <input
                        type="number"
                        name="detail_order_${detailIndex}"
                        value="0"
                        min="0"
                        style="
                            width:100px;
                            padding:8px;
                        "
                    >

                </div>


                <div style="margin-top:10px;">

                    <label>

                        <input
                            type="checkbox"
                            name="detail_active_${detailIndex}"
                            checked
                        >

                        فعال

                    </label>

                </div>


                <div
                    class="detail-barbers-container"
                    style="margin-top:20px;"
                >

                    <strong>
                        آرایشگر، قیمت و زمان این جزئیات
                    </strong>

                    ${barberHTML}

                </div>

            `;


            container.appendChild(row);

        }
    );


    // =====================================================
    // حذف Detail
    // =====================================================

    container.addEventListener(
        "click",
        function (event) {

            const button = event.target.closest(
                ".remove-detail-btn"
            );

            if (!button) {
                return;
            }

            const row = button.closest(
                ".detail-row"
            );

            if (!row) {
                return;
            }

            row.remove();

        }
    );


    // =====================================================
    // اضافه کردن container به Detailهای قبلی
    //
    // چون HTML فعلی Detailهای قدیمی این کلاس را ندارد،
    // اینجا خودمان بخش آرایشگر را پیدا می‌کنیم.
    // =====================================================

    document.querySelectorAll(".detail-row").forEach(
        function (row) {

            const existingSection = Array.from(
                row.children
            ).find(function (element) {

                return (
                    element.tagName === "DIV" &&
                    element.textContent.includes(
                        "آرایشگر، قیمت و زمان این جزئیات"
                    )
                );

            });

            if (existingSection) {

                existingSection.classList.add(
                    "detail-barbers-container"
                );

            }

        }
    );

});