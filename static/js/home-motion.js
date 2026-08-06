/* ==================================
   SHOPSPHERE HOMEPAGE MOTION
================================== */

document.addEventListener("DOMContentLoaded", () => {
    const loader = document.querySelector("#brandLoader");
    const loaderProgress = document.querySelector("#loaderProgress");
    const loaderPercentage = document.querySelector("#loaderPercentage");

    const hero = document.querySelector("#motionHero");
    const productStage = document.querySelector("#productStage");
    const heroProduct = document.querySelector("#heroProduct");

    const floatingCards = document.querySelectorAll(
        "[data-floating-card]"
    );

    const revealElements = document.querySelectorAll(
        "[data-reveal]"
    );

    const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;


    /* ==================================
       BRAND LOADER
    ================================== */

    const runLoader = () => {
        if (!loader || reduceMotion) {
            loader?.classList.add("is-hidden");
            return;
        }

        let progress = 0;

        const loaderTimer = window.setInterval(() => {
            const increment = Math.floor(
                Math.random() * 9
            ) + 3;

            progress = Math.min(
                progress + increment,
                100
            );

            if (loaderProgress) {
                loaderProgress.style.width = `${progress}%`;
            }

            if (loaderPercentage) {
                loaderPercentage.textContent = `${progress}%`;
            }

            if (progress >= 100) {
                window.clearInterval(loaderTimer);

                window.setTimeout(() => {
                    loader.classList.add("is-hidden");

                    document.body.classList.add(
                        "homepage-loaded"
                    );
                }, 520);
            }
        }, 85);
    };

    runLoader();


    /* ==================================
       INTERSECTION REVEAL
    ================================== */

    const revealObserver = new IntersectionObserver(
        (entries, observer) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    return;
                }

                entry.target.classList.add(
                    "is-visible"
                );

                observer.unobserve(entry.target);
            });
        },
        {
            threshold: 0.16,
            rootMargin: "0px 0px -6% 0px",
        }
    );

    revealElements.forEach((element) => {
        revealObserver.observe(element);
    });


    /* ==================================
       HERO POINTER PARALLAX
    ================================== */

    if (
        !reduceMotion
        && hero
        && productStage
        && heroProduct
    ) {
        let pointerX = 0;
        let pointerY = 0;
        let targetX = 0;
        let targetY = 0;

        const animatePointer = () => {
            pointerX += (
                targetX - pointerX
            ) * 0.075;

            pointerY += (
                targetY - pointerY
            ) * 0.075;

            productStage.style.setProperty(
                "--stage-x",
                `${pointerX}px`
            );

            productStage.style.setProperty(
                "--stage-y",
                `${pointerY}px`
            );

            floatingCards.forEach((card) => {
                const depth = Number(
                    card.dataset.depth || 1
                );

                card.style.translate = `
                    ${pointerX * depth}px
                    ${pointerY * depth}px
                `;
            });

            window.requestAnimationFrame(
                animatePointer
            );
        };

        hero.addEventListener(
            "pointermove",
            (event) => {
                const heroBounds =
                    hero.getBoundingClientRect();

                const relativeX =
                    (
                        event.clientX
                        - heroBounds.left
                    )
                    / heroBounds.width
                    - 0.5;

                const relativeY =
                    (
                        event.clientY
                        - heroBounds.top
                    )
                    / heroBounds.height
                    - 0.5;

                targetX = relativeX * 24;
                targetY = relativeY * 17;
            }
        );

        hero.addEventListener(
            "pointerleave",
            () => {
                targetX = 0;
                targetY = 0;
            }
        );

        animatePointer();


        /* ==================================
           SCROLL PRODUCT TRANSFORMATION
        ================================== */

        let scrollFrameRequested = false;

        const updateProductOnScroll = () => {
            const heroBounds =
                hero.getBoundingClientRect();

            const scrollDistance =
                Math.max(
                    0,
                    -heroBounds.top
                );

            const progress =
                Math.min(
                    scrollDistance
                    / Math.max(
                        hero.offsetHeight,
                        1
                    ),
                    1
                );

            const moveY = progress * 110;
            const moveX = progress * 44;
            const rotation = -7 + progress * 10;
            const scale = 1 - progress * 0.08;

            heroProduct.style.transform = `
                translate3d(
                    ${moveX + pointerX}px,
                    ${moveY + pointerY}px,
                    0
                )
                rotate(${rotation}deg)
                scale(${scale})
            `;

            scrollFrameRequested = false;
        };

        window.addEventListener(
            "scroll",
            () => {
                if (scrollFrameRequested) {
                    return;
                }

                scrollFrameRequested = true;

                window.requestAnimationFrame(
                    updateProductOnScroll
                );
            },
            {
                passive: true,
            }
        );

        updateProductOnScroll();
    }


    /* ==================================
       VIDEO FALLBACK
    ================================== */

    const heroVideo = document.querySelector(
        ".motion-hero__video"
    );

    if (heroVideo) {
        heroVideo
            .play()
            .catch(() => {
                heroVideo.style.display = "none";
            });
    }
});