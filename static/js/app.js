"use strict";

const exploreButton = document.querySelector("#exploreButton");

if (exploreButton) {
    exploreButton.addEventListener("click", () => {
        exploreButton.textContent = "Day 1 Foundation Ready";
    });
}

console.log("ShopSphere frontend initialized.");


/* ==================================
   PRODUCT DETAILS PAGE
================================== */

const sizeButtons = document.querySelectorAll(
    ".product-option__size"
);

const quantityInput = document.querySelector(
    "#productQuantity"
);

/* YAHAN NAYA CODE ADD KARNA HAI */

const selectedVariantInput = document.querySelector(
    "#selectedVariantId"
);

const addToCartForm = document.querySelector(
    "#addToCartForm"
);

/* NAYA CODE YAHAN END HUA */

const decreaseQuantityButton = document.querySelector(
    "#decreaseQuantity"
);

const increaseQuantityButton = document.querySelector(
    "#increaseQuantity"
);

const selectionMessage = document.querySelector(
    "#productSelectionMessage"
);

let selectedSize = null;
let selectedVariantStock = 0;

sizeButtons.forEach((button) => {
    button.addEventListener("click", () => {
        sizeButtons.forEach((item) => {
            item.classList.remove("is-selected");
        });

        button.classList.add("is-selected");

        selectedSize = button.dataset.size;

        if (selectedVariantInput) {
            selectedVariantInput.value = button.dataset.variantId;
        }

        selectedVariantStock = Number(button.dataset.stock);

        if (quantityInput) {
            quantityInput.value = 1;
            quantityInput.max = selectedVariantStock;
        }

        if (selectionMessage) {
            selectionMessage.textContent =
                `Size ${selectedSize} selected. ` +
                `${selectedVariantStock} available.`;
        }
    });
});

if (decreaseQuantityButton && quantityInput) {
    decreaseQuantityButton.addEventListener("click", () => {
        const currentQuantity = Number(quantityInput.value);

        if (currentQuantity > 1) {
            quantityInput.value = currentQuantity - 1;
        }
    });
}

if (increaseQuantityButton && quantityInput) {
    increaseQuantityButton.addEventListener("click", () => {
        const currentQuantity = Number(quantityInput.value);
        const maximumQuantity =
            selectedVariantStock || Number(quantityInput.max);

        if (currentQuantity < maximumQuantity) {
            quantityInput.value = currentQuantity + 1;
        }
    });
}

const galleryThumbnails = document.querySelectorAll(
    ".product-gallery__thumbnail"
);

const mainProductImage = document.querySelector(
    "#mainProductImage"
);

galleryThumbnails.forEach((thumbnail) => {
    thumbnail.addEventListener("click", () => {
        if (!mainProductImage) {
            return;
        }

        mainProductImage.src = thumbnail.dataset.image;

        galleryThumbnails.forEach((item) => {
            item.classList.remove("is-active");
        });

        thumbnail.classList.add("is-active");
    });
});

if (addToCartForm) {
    addToCartForm.addEventListener("submit", (event) => {
        if (
            !selectedVariantInput
            || !selectedVariantInput.value
        ) {
            event.preventDefault();

            if (selectionMessage) {
                selectionMessage.textContent =
                    "Please select a size before adding to cart.";
            }
        }
    });
}

/* ==================================
   PASSWORD SHOW / HIDE TOGGLE
================================== */

const passwordInputs = document.querySelectorAll(
    'input[type="password"]'
);

const eyeIcon = `
    <svg
        viewBox="0 0 24 24"
        width="20"
        height="20"
        aria-hidden="true"
    >
        <path
            d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12Z"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
        />
        <circle
            cx="12"
            cy="12"
            r="3"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
        />
    </svg>
`;

const eyeOffIcon = `
    <svg
        viewBox="0 0 24 24"
        width="20"
        height="20"
        aria-hidden="true"
    >
        <path
            d="M3 3l18 18"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
        />
        <path
            d="M10.6 6.2A9.8 9.8 0 0 1 12 6c6.5 0 10 6 10 6a17 17 0 0 1-3 3.8"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
        />
        <path
            d="M6.6 6.7C3.6 8.5 2 12 2 12s3.5 6 10 6a10 10 0 0 0 4.2-.9"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
        />
        <path
            d="M9.9 9.9a3 3 0 0 0 4.2 4.2"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
        />
    </svg>
`;

passwordInputs.forEach((input) => {
    if (input.closest(".password-input-wrapper")) {
        return;
    }

    const wrapper = document.createElement("div");
    wrapper.className = "password-input-wrapper";

    input.parentNode.insertBefore(wrapper, input);
    wrapper.appendChild(input);

    const toggleButton = document.createElement("button");

    toggleButton.type = "button";
    toggleButton.className = "password-toggle-button";
    toggleButton.innerHTML = eyeIcon;
    toggleButton.setAttribute("aria-label", "Show password");
    toggleButton.setAttribute("aria-pressed", "false");
    toggleButton.title = "Show password";

    wrapper.appendChild(toggleButton);

    toggleButton.addEventListener("click", () => {
        const passwordIsHidden = input.type === "password";

        input.type = passwordIsHidden
            ? "text"
            : "password";

        toggleButton.innerHTML = passwordIsHidden
            ? eyeOffIcon
            : eyeIcon;

        toggleButton.setAttribute(
            "aria-label",
            passwordIsHidden
                ? "Hide password"
                : "Show password"
        );

        toggleButton.setAttribute(
            "aria-pressed",
            String(passwordIsHidden)
        );

        toggleButton.title = passwordIsHidden
            ? "Hide password"
            : "Show password";

        input.focus();
    });
});