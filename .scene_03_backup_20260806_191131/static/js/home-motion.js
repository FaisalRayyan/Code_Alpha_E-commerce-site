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

    gsap.to(
        ".ss-transition__track",
        {
            xPercent: -45,

            scrollTrigger: {
                trigger: ".ss-transition",
                start: "top bottom",
                end: "bottom top",
                scrub: 1.2,
            },
        }
    );

    gsap.from(
        ".ss-transition__content > *",
        {
            opacity: 0,
            y: 65,
            stagger: 0.12,
            duration: 0.9,

            scrollTrigger: {
                trigger: ".ss-transition__content",
                start: "top 75%",
            },
        }
    );


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