"use strict";

const exploreButton = document.querySelector("#exploreButton");

if (exploreButton) {
    exploreButton.addEventListener("click", () => {
        exploreButton.textContent = "Day 1 Foundation Ready";
    });
}

console.log("ShopSphere frontend initialized.");

const sizeButtons = document.querySelectorAll(
    ".product-option__size"
);

const quantityInput = document.querySelector(
    "#productQuantity"
);

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