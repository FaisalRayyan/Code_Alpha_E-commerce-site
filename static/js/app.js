"use strict";

const exploreButton = document.querySelector("#exploreButton");

if (exploreButton) {
    exploreButton.addEventListener("click", () => {
        exploreButton.textContent = "Day 1 Foundation Ready";
    });
}

console.log("ShopSphere frontend initialized.");