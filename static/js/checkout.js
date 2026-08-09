document.addEventListener("DOMContentLoaded", function () {

```
const deliveryOptions = document.querySelectorAll(
    'input[name="delivery_type"]'
);

const receiverBox = document.getElementById(
    "receiverBox"
);

const receiverName = document.getElementById(
    "receiverName"
);

const receiverPhone = document.getElementById(
    "receiverPhone"
);


deliveryOptions.forEach(function (option) {

    option.addEventListener("change", function () {

        if (this.value === "other") {

            receiverBox.classList.add("active");

            receiverName.required = true;
            receiverPhone.required = true;

        } else {

            receiverBox.classList.remove("active");

            receiverName.required = false;
            receiverPhone.required = false;

            receiverName.value = "";
            receiverPhone.value = "";

        }

    });

});
```

});
