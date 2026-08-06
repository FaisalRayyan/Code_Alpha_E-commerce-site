/* ==================================
   SHOPSPHERE BRAND-FILM MOTION
================================== */

document.addEventListener("DOMContentLoaded", () => {
    const intro = document.querySelector("#ssIntro");
    const hero = document.querySelector("#ssHero");
    const portal = document.querySelector("#ssPortal");

    const progressBar = document.querySelector("#ssProgressBar");
    const progressNumber = document.querySelector("#ssProgressNumber");

    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    if (
        typeof gsap === "undefined"
        || typeof ScrollTrigger === "undefined"
    ) {
        intro?.remove();
        return;
    }

    gsap.registerPlugin(ScrollTrigger);

    if (reducedMotion) {
        intro?.remove();
        return;
    }

    document.body.classList.add("ss-intro-active");


    /* ==================================
       INTRO COUNTER
    ================================== */

    const counter = {
        value: 0,
    };

    const introTimeline = gsap.timeline({
        defaults: {
            ease: "power3.out",
        },
        onComplete: () => {
            document.body.classList.remove(
                "ss-intro-active"
            );

            ScrollTrigger.refresh();
        },
    });

    introTimeline
        .from(
            ".ss-intro__topline span",
            {
                opacity: 0,
                y: -16,
                stagger: 0.08,
                duration: 0.55,
            }
        )
        .from(
            ".ss-intro__mark-wrap",
            {
                opacity: 0,
                scale: 0.42,
                rotation: -18,
                duration: 0.85,
                ease: "back.out(1.7)",
            },
            "-=0.2"
        )
        .from(
            ".ss-intro__ring",
            {
                opacity: 0,
                scale: 0.55,
                duration: 0.7,
            },
            "-=0.55"
        )
        .from(
            ".ss-intro__wordmark",
            {
                yPercent: 120,
                duration: 0.9,
                ease: "power4.out",
            },
            "-=0.4"
        )
        .from(
            ".ss-intro__copy",
            {
                opacity: 0,
                y: 18,
                duration: 0.55,
            },
            "-=0.35"
        )
        .to(
            counter,
            {
                value: 100,
                duration: 1.45,
                ease: "power2.inOut",

                onUpdate: () => {
                    const currentValue = Math.round(
                        counter.value
                    );

                    if (progressBar) {
                        progressBar.style.width =
                            `${currentValue}%`;
                    }

                    if (progressNumber) {
                        progressNumber.textContent =
                            String(currentValue)
                                .padStart(3, "0");
                    }
                },
            },
            "-=0.15"
        )
        .to(
            ".ss-intro__flash",
            {
                opacity: 1,
                duration: 0.12,
                ease: "power4.in",
            }
        )
        .to(
            ".ss-intro__flash",
            {
                opacity: 0,
                duration: 0.3,
            }
        )
        .to(
            ".ss-intro__center",
            {
                opacity: 0,
                scale: 1.15,
                filter: "blur(18px)",
                duration: 0.55,
                ease: "power3.in",
            },
            "-=0.18"
        )
        .to(
            ".ss-intro__topline, .ss-intro__bottom",
            {
                opacity: 0,
                duration: 0.32,
            },
            "<"
        )
        .to(
            intro,
            {
                yPercent: -100,
                duration: 0.92,
                ease: "power4.inOut",
            }
        )
        .set(
            intro,
            {
                display: "none",
            }
        );


    /* ==================================
       HERO ENTRANCE
    ================================== */

    gsap.set(
        [
            ".ss-hero__edition",
            ".ss-title-line",
            ".ss-hero__description",
            ".ss-hero__actions",
            ".ss-hero__footer",
            ".ss-portal",
        ],
        {
            visibility: "visible",
        }
    );

    introTimeline
        .from(
            ".ss-hero__edition",
            {
                opacity: 0,
                x: -35,
                duration: 0.55,
            },
            "-=0.48"
        )
        .from(
            ".ss-title-line",
            {
                opacity: 0,
                y: 100,
                rotateX: -55,
                stagger: 0.09,
                duration: 0.85,
                ease: "power4.out",
            },
            "-=0.35"
        )
        .from(
            ".ss-hero__description",
            {
                opacity: 0,
                y: 25,
                duration: 0.55,
            },
            "-=0.4"
        )
        .from(
            ".ss-hero__actions",
            {
                opacity: 0,
                y: 24,
                duration: 0.5,
            },
            "-=0.38"
        )
        .from(
            ".ss-portal",
            {
                opacity: 0,
                x: 110,
                scale: 0.68,
                rotateY: -28,
                duration: 1.1,
                ease: "power4.out",
            },
            "-=0.8"
        )
        .from(
            ".ss-float-card",
            {
                opacity: 0,
                scale: 0.78,
                y: 25,
                stagger: 0.13,
                duration: 0.55,
                ease: "back.out(1.6)",
            },
            "-=0.45"
        )
        .from(
            ".ss-hero__footer",
            {
                opacity: 0,
                y: 15,
                duration: 0.5,
            },
            "-=0.3"
        );


    /* ==================================
       CONTINUOUS ORBIT MOTION
    ================================== */

    gsap.to(
        ".ss-portal__orbit--outer",
        {
            rotationZ: "+=360",
            duration: 24,
            repeat: -1,
            ease: "none",
        }
    );

    gsap.to(
        ".ss-portal__orbit--middle",
        {
            rotationZ: "-=360",
            duration: 19,
            repeat: -1,
            ease: "none",
        }
    );

    gsap.to(
        ".ss-portal__orbit--inner",
        {
            rotationZ: "+=360",
            duration: 14,
            repeat: -1,
            ease: "none",
        }
    );

    gsap.to(
        ".ss-portal__core",
        {
            y: -13,
            rotation: 2,
            duration: 2.4,
            repeat: -1,
            yoyo: true,
            ease: "sine.inOut",
        }
    );


    /* ==================================
       POINTER PARALLAX
    ================================== */

    if (hero && portal) {
        hero.addEventListener(
            "pointermove",
            (event) => {
                const bounds =
                    hero.getBoundingClientRect();

                const relativeX =
                    (
                        event.clientX
                        - bounds.left
                    )
                    / bounds.width
                    - 0.5;

                const relativeY =
                    (
                        event.clientY
                        - bounds.top
                    )
                    / bounds.height
                    - 0.5;

                gsap.to(
                    portal,
                    {
                        x: relativeX * 25,
                        y: relativeY * 18,
                        rotateY: relativeX * 5,
                        rotateX: relativeY * -4,
                        duration: 0.8,
                        ease: "power3.out",
                    }
                );

                document
                    .querySelectorAll("[data-parallax]")
                    .forEach((element) => {
                        const depth = Number(
                            element.dataset.parallax || 1
                        );

                        gsap.to(
                            element,
                            {
                                x:
                                    relativeX
                                    * 35
                                    * depth,

                                y:
                                    relativeY
                                    * 25
                                    * depth,

                                duration: 1.1,
                                ease: "power3.out",
                            }
                        );
                    });
            }
        );

        hero.addEventListener(
            "pointerleave",
            () => {
                gsap.to(
                    portal,
                    {
                        x: 0,
                        y: 0,
                        rotateX: 0,
                        rotateY: 0,
                        duration: 1,
                        ease: "power3.out",
                    }
                );
            }
        );
    }


    /* ==================================
       SCROLL TRANSITION
    ================================== */

    gsap.to(
        ".ss-portal",
        {
            y: 180,
            scale: 0.78,
            rotateZ: 8,

            scrollTrigger: {
                trigger: ".ss-hero",
                start: "top top",
                end: "bottom top",
                scrub: 1.1,
            },
        }
    );

    gsap.to(
        ".ss-hero__copy",
        {
            y: -100,
            opacity: 0.22,

            scrollTrigger: {
                trigger: ".ss-hero",
                start: "35% top",
                end: "bottom top",
                scrub: 1,
            },
        }
    );





    /* ==================================
       SCENE 02 — PRODUCT STORY
    ================================== */

    const productStory = document.querySelector(
        "#ssProductStory"
    );

    const storyShoe = document.querySelector(
        "#ssStoryShoe"
    );

    const storyCounter = document.querySelector(
        "#ssStoryCounter"
    );

    const storyProgress = document.querySelector(
        "#ssStoryProgress"
    );

    const storySteps = gsap.utils.toArray(
        "[data-story-step]"
    );

    const storyLabels = gsap.utils.toArray(
        "[data-story-label]"
    );

    const storyHotspots = gsap.utils.toArray(
        "[data-story-hotspot]"
    );

    const storyDetails = gsap.utils.toArray(
        "[data-story-detail]"
    );

    const setStoryState = (index) => {
        storySteps.forEach((step, stepIndex) => {
            step.classList.toggle(
                "is-active",
                stepIndex === index
            );
        });

        storyLabels.forEach((label, labelIndex) => {
            label.classList.toggle(
                "is-active",
                labelIndex === index
            );
        });

        storyHotspots.forEach((hotspot) => {
            hotspot.classList.toggle(
                "is-active",
                Number(hotspot.dataset.storyHotspot) === index
            );
        });

        if (storyCounter) {
            storyCounter.textContent = String(
                index + 1
            ).padStart(2, "0");
        }
    };

    if (
        productStory
        && storyShoe
        && window.innerWidth > 700
    ) {
        const storyTimeline = gsap.timeline({
            defaults: {
                ease: "power3.inOut",
            },

            scrollTrigger: {
                trigger: productStory,
                start: "top top+=78",
                end: "bottom bottom",
                scrub: 1,

                onUpdate: (self) => {
                    const progress = self.progress;

                    if (storyProgress) {
                        storyProgress.style.width =
                            `${progress * 100}%`;
                    }

                    const state = Math.min(
                        Math.floor(progress * 4),
                        3
                    );

                    setStoryState(state);
                },
            },
        });

        storyTimeline
            .fromTo(
                storyShoe,
                {
                    xPercent: 28,
                    yPercent: 12,
                    rotation: -15,
                    scale: 0.76,
                    opacity: 0,
                },
                {
                    xPercent: 0,
                    yPercent: 0,
                    rotation: -8,
                    scale: 0.9,
                    opacity: 1,
                    duration: 0.8,
                    ease: "power4.out",
                },
                0
            )
            .to(
                ".ss-product-story__word",
                {
                    xPercent: -28,
                    duration: 4,
                    ease: "none",
                },
                0
            )
            .to(
                storyShoe,
                {
                    xPercent: -6,
                    yPercent: -3,
                    rotation: -3,
                    scale: 1.02,
                    duration: 0.8,
                },
                0.85
            )
            .to(
                '[data-story-detail="1"]',
                {
                    autoAlpha: 1,
                    y: 0,
                    scale: 1,
                    duration: 0.5,
                },
                0.9
            )
            .to(
                '[data-story-detail="1"]',
                {
                    autoAlpha: 0,
                    y: -18,
                    scale: 0.94,
                    duration: 0.35,
                },
                1.65
            )
            .to(
                storyShoe,
                {
                    xPercent: 4,
                    yPercent: 4,
                    rotation: 2,
                    scale: 1.08,
                    duration: 0.8,
                },
                1.7
            )
            .to(
                '[data-story-detail="2"]',
                {
                    autoAlpha: 1,
                    y: 0,
                    scale: 1,
                    duration: 0.5,
                },
                1.75
            )
            .to(
                '[data-story-detail="2"]',
                {
                    autoAlpha: 0,
                    y: -18,
                    scale: 0.94,
                    duration: 0.35,
                },
                2.5
            )
            .to(
                storyShoe,
                {
                    xPercent: -4,
                    yPercent: 9,
                    rotation: 7,
                    scale: 1.02,
                    duration: 0.8,
                },
                2.55
            )
            .to(
                '[data-story-detail="3"]',
                {
                    autoAlpha: 1,
                    y: 0,
                    scale: 1,
                    duration: 0.5,
                },
                2.6
            )
            .to(
                ".ss-product-story__actions",
                {
                    autoAlpha: 1,
                    y: 0,
                    duration: 0.45,
                },
                3.15
            );

        gsap.to(
            ".ss-story-orbit--outer",
            {
                rotationZ: "+=360",
                duration: 28,
                repeat: -1,
                ease: "none",
            }
        );

        gsap.to(
            ".ss-story-orbit--inner",
            {
                rotationZ: "-=360",
                duration: 21,
                repeat: -1,
                ease: "none",
            }
        );
    }



    /* ==================================
       SCENE 03 — COLORWAYS
    ================================== */

    const colorwaySection = document.querySelector(
        "#ssColorways"
    );

    const colorwayStage = document.querySelector(
        "#ssColorwayStage"
    );

    const colorwayShoe = document.querySelector(
        "#ssColorwayShoe"
    );

    const colorwayOptions = gsap.utils.toArray(
        ".ss-colorway-option"
    );

    const colorwayIndex = document.querySelector(
        "#ssColorwayIndex"
    );

    const colorwayName = document.querySelector(
        "#ssColorwayName"
    );

    const colorwayMood = document.querySelector(
        "#ssColorwayMood"
    );

    const colorwayFinish = document.querySelector(
        "#ssColorwayFinish"
    );

    const colorwayUse = document.querySelector(
        "#ssColorwayUse"
    );

    let activeColorway = -1;

    const applyColorway = (
        option,
        index,
        animate = true
    ) => {
        if (!option || index === activeColorway) {
            return;
        }

        activeColorway = index;

        colorwayOptions.forEach((item, itemIndex) => {
            const isActive = itemIndex === index;

            item.classList.toggle(
                "is-active",
                isActive
            );

            item.setAttribute(
                "aria-selected",
                String(isActive)
            );
        });

        const accent =
            option.dataset.colorwayAccent || "#4169ff";

        const secondary =
            option.dataset.colorwaySecondary || "#69dcff";

        colorwaySection?.style.setProperty(
            "--colorway-accent",
            accent
        );

        colorwaySection?.style.setProperty(
            "--colorway-secondary",
            secondary
        );

        if (colorwayIndex) {
            colorwayIndex.textContent =
                option.dataset.colorwayIndex;
        }

        if (colorwayName) {
            colorwayName.textContent =
                option.dataset.colorwayName;
        }

        if (colorwayMood) {
            colorwayMood.textContent =
                option.dataset.colorwayMood;
        }

        if (colorwayFinish) {
            colorwayFinish.textContent =
                option.dataset.colorwayFinish;
        }

        if (colorwayUse) {
            colorwayUse.textContent =
                option.dataset.colorwayUse;
        }

        const newImage =
            option.dataset.colorwayImage;

        if (!colorwayShoe || !newImage) {
            return;
        }

        if (!animate) {
            colorwayShoe.src = newImage;
            colorwayShoe.alt =
                `${option.dataset.colorwayName} ShopSphere shoe`;
            return;
        }

        gsap
            .timeline()
            .to(
                colorwayShoe,
                {
                    opacity: 0,
                    xPercent: index % 2 === 0 ? -16 : 16,
                    rotation: index % 2 === 0 ? -18 : 10,
                    scale: 0.86,
                    filter: "blur(12px)",
                    duration: 0.3,
                    ease: "power3.in",
                }
            )
            .add(() => {
                colorwayShoe.src = newImage;
                colorwayShoe.alt =
                    `${option.dataset.colorwayName} ShopSphere shoe`;
            })
            .fromTo(
                colorwayShoe,
                {
                    opacity: 0,
                    xPercent: index % 2 === 0 ? 18 : -18,
                    rotation: index % 2 === 0 ? 9 : -17,
                    scale: 0.88,
                    filter: "blur(12px)",
                },
                {
                    opacity: 1,
                    xPercent: 0,
                    rotation: -7,
                    scale: 0.98,
                    filter: "blur(0px)",
                    duration: 0.62,
                    ease: "power4.out",
                }
            );

        gsap.fromTo(
            [
                colorwayName,
                colorwayMood,
                colorwayFinish,
                colorwayUse,
            ],
            {
                opacity: 0,
                y: 14,
            },
            {
                opacity: 1,
                y: 0,
                stagger: 0.06,
                duration: 0.42,
                ease: "power3.out",
            }
        );
    };

    colorwayOptions.forEach((option, index) => {
        option.addEventListener("click", () => {
            applyColorway(option, index);
        });

        option.addEventListener(
            "keydown",
            (event) => {
                if (
                    event.key !== "ArrowRight"
                    && event.key !== "ArrowLeft"
                ) {
                    return;
                }

                event.preventDefault();

                const direction =
                    event.key === "ArrowRight"
                        ? 1
                        : -1;

                const nextIndex =
                    (
                        index
                        + direction
                        + colorwayOptions.length
                    )
                    % colorwayOptions.length;

                colorwayOptions[nextIndex].focus();

                applyColorway(
                    colorwayOptions[nextIndex],
                    nextIndex
                );
            }
        );
    });

    if (
        colorwayOptions.length
        && colorwaySection
    ) {
        applyColorway(
            colorwayOptions[0],
            0,
            false
        );

        gsap.from(
            ".ss-colorways__header > *",
            {
                opacity: 0,
                y: 45,
                stagger: 0.12,
                duration: 0.8,

                scrollTrigger: {
                    trigger: ".ss-colorways__header",
                    start: "top 76%",
                },
            }
        );

        gsap.from(
            ".ss-colorways__product",
            {
                opacity: 0,
                scale: 0.72,
                rotationY: -22,
                duration: 1.1,
                ease: "power4.out",

                scrollTrigger: {
                    trigger: ".ss-colorways__stage",
                    start: "top 72%",
                },
            }
        );

        gsap.from(
            ".ss-colorways__details > *",
            {
                opacity: 0,
                x: 45,
                stagger: 0.1,
                duration: 0.65,

                scrollTrigger: {
                    trigger: ".ss-colorways__details",
                    start: "top 76%",
                },
            }
        );

        gsap.from(
            ".ss-colorway-option",
            {
                opacity: 0,
                y: 30,
                stagger: 0.12,
                duration: 0.6,

                scrollTrigger: {
                    trigger: ".ss-colorways__selector",
                    start: "top 84%",
                },
            }
        );

        if (window.innerWidth > 700) {
            ScrollTrigger.create({
                trigger: colorwaySection,
                start: "top 35%",
                end: "bottom 65%",

                onUpdate: (self) => {
                    const index = Math.min(
                        Math.floor(
                            self.progress
                            * colorwayOptions.length
                        ),
                        colorwayOptions.length - 1
                    );

                    applyColorway(
                        colorwayOptions[index],
                        index
                    );
                },
            });

            gsap.to(
                ".ss-colorways__ring--one",
                {
                    rotationZ: "+=360",
                    duration: 28,
                    repeat: -1,
                    ease: "none",
                }
            );

            gsap.to(
                ".ss-colorways__ring--two",
                {
                    rotationZ: "-=360",
                    duration: 22,
                    repeat: -1,
                    ease: "none",
                }
            );

            if (colorwayStage) {
                colorwayStage.addEventListener(
                    "pointermove",
                    (event) => {
                        const bounds =
                            colorwayStage.getBoundingClientRect();

                        const x =
                            (
                                event.clientX
                                - bounds.left
                            )
                            / bounds.width
                            - 0.5;

                        const y =
                            (
                                event.clientY
                                - bounds.top
                            )
                            / bounds.height
                            - 0.5;

                        gsap.to(
                            colorwayShoe,
                            {
                                x: x * 24,
                                y: y * 16,
                                rotateY: x * 5,
                                rotateX: y * -4,
                                duration: 0.8,
                                ease: "power3.out",
                            }
                        );
                    }
                );

                colorwayStage.addEventListener(
                    "pointerleave",
                    () => {
                        gsap.to(
                            colorwayShoe,
                            {
                                x: 0,
                                y: 0,
                                rotateX: 0,
                                rotateY: 0,
                                duration: 0.9,
                                ease: "power3.out",
                            }
                        );
                    }
                );
            }
        }
    }


    /* ==================================
       SCENE 04 — FEATURED PRODUCTS
    ================================== */

    const featuredCards = gsap.utils.toArray(
        "[data-featured-card]"
    );

    if (featuredCards.length) {
        gsap.from(
            ".ss-featured__header > *",
            {
                opacity: 0,
                y: 44,
                stagger: 0.12,
                duration: 0.75,

                scrollTrigger: {
                    trigger: ".ss-featured__header",
                    start: "top 78%",
                },
            }
        );

        const featuredEntrances = [
            {
                x: -150,
                y: 80,
                rotation: -10,
                scale: 0.88,
            },
            {
                x: 20,
                y: 150,
                rotation: 7,
                scale: 0.9,
            },
            {
                x: 130,
                y: -30,
                rotation: -5,
                scale: 0.9,
            },
            {
                x: 170,
                y: 110,
                rotation: 9,
                scale: 0.86,
            },
        ];

        featuredCards.forEach((card, index) => {
            const entrance =
                featuredEntrances[
                    index % featuredEntrances.length
                ];

            gsap.from(
                card,
                {
                    ...entrance,
                    opacity: 0,
                    duration: 0.95,
                    ease: "power4.out",

                    scrollTrigger: {
                        trigger: card,
                        start: "top 88%",
                    },
                }
            );
        });
    }

    /* ==================================
       VIDEO FALLBACK
    ================================== */

    const heroVideo = document.querySelector(
        ".ss-hero__video"
    );

    if (heroVideo) {
        heroVideo
            .play()
            .catch(() => {
                heroVideo.style.display = "none";
            });
    }
});