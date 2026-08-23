document.addEventListener("DOMContentLoaded", function () {

    const recipientTypes = document.querySelectorAll(
        'input[name="recipient_type"]'
    );

    const recipientCount = document.getElementById(
        "recipient-count"
    );

    const message = document.getElementById(
        "sms-message"
    );

    const characterCount = document.getElementById(
        "sms-character-count"
    );

    const manualBox = document.getElementById(
        "manual-recipient-box"
    );

    const manualSearch = document.getElementById(
        "manual-recipient-search"
    );

    const manualList = document.getElementById(
        "manual-recipient-list"
    );


    const allUsersCount = parseInt(
        document.body.dataset.usersCount || "0"
    );

    const reservationUsersCount = parseInt(
        document.body.dataset.reservationUsersCount || "0"
    );


    // =========================================
    // تغییر نوع گیرندگان
    // =========================================

    recipientTypes.forEach(function (radio) {

        radio.addEventListener("change", function () {

            if (this.value === "all") {

                manualBox.style.display = "none";

                recipientCount.textContent =
                    allUsersCount;

            }

            else if (this.value === "reservation") {

                manualBox.style.display = "none";

                recipientCount.textContent =
                    reservationUsersCount;

            }

            else if (this.value === "manual") {

                manualBox.style.display = "block";

                recipientCount.textContent = "0";

                manualSearch.focus();

            }

        });

    });


    // =========================================
    // شمارش کاراکتر
    // =========================================

    if (message && characterCount) {

        message.addEventListener("input", function () {

            characterCount.textContent =
                this.value.length;

        });

    }


    // =========================================
    // جستجوی کاربران
    // =========================================

    if (manualSearch) {

        manualSearch.addEventListener(
            "input",
            async function () {

                const search =
                    this.value.trim();


                if (!search) {

                    manualList.innerHTML = `
                        <p>
                            برای نمایش کاربران، جستجو کنید.
                        </p>
                    `;

                    recipientCount.textContent = "0";

                    return;
                }


                manualList.innerHTML = `
                    <p>
                        در حال جستجو...
                    </p>
                `;


                try {

                    const response = await fetch(
                        "/superadmin/sms/search-users/?search=" +
                        encodeURIComponent(search),
                        {
                            headers: {
                                "X-Requested-With":
                                    "XMLHttpRequest"
                            }
                        }
                    );


                    if (!response.ok) {

                        throw new Error(
                            "خطا در دریافت کاربران"
                        );

                    }


                    const data =
                        await response.json();


                    manualList.innerHTML = "";


                    if (!data.users.length) {

                        manualList.innerHTML = `
                            <p>
                                کاربری پیدا نشد.
                            </p>
                        `;

                        recipientCount.textContent = "0";

                        return;
                    }


                    data.users.forEach(function (user) {

                        const label =
                            document.createElement("label");

                        label.className =
                            "sms-user-option";


                        label.innerHTML = `

                            <input
                                type="checkbox"
                                name="manual_users"
                                value="${user.id}"
                            >

                            <span>
                                ${user.name}
                            </span>

                            <small>
                                ${user.phone}
                            </small>

                        `;


                        manualList.appendChild(label);

                    });


                }

                catch (error) {

                    console.error(
                        "SMS USER SEARCH ERROR:",
                        error
                    );


                    manualList.innerHTML = `
                        <p>
                            خطا در دریافت کاربران.
                        </p>
                    `;

                }

            }
        );

    }


    // =========================================
    // شمارش کاربران انتخاب‌شده
    // =========================================

    if (manualList) {

        manualList.addEventListener(
            "change",
            function (event) {

                if (
                    event.target.matches(
                        'input[name="manual_users"]'
                    )
                ) {

                    const selected =
                        manualList.querySelectorAll(
                            'input[name="manual_users"]:checked'
                        );


                    recipientCount.textContent =
                        selected.length;

                }

            }
        );

    }

});