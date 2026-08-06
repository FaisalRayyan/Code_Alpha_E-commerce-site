/* =========================================================
   SHOPSPHERE — REFERENCE-VIDEO SCROLL MOTION
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    const stage = document.querySelector("#ssLaunchStage");
    const skip = document.querySelector("#ssLaunchSkip");
    const progressBar = document.querySelector("#ssLaunchProgress");
    const scenes = Array.from(document.querySelectorAll(".ss-scene"));
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (!stage || reducedMotion) {
        return;
    }

    if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined") {
        scenes.forEach((scene, index) => {
            scene.classList.toggle("is-active", index === scenes.length - 1);
        });
        return;
    }

    gsap.registerPlugin(ScrollTrigger);

    const sceneCount = scenes.length;
    const sceneDuration = 1.25;
    const totalDuration = sceneCount * sceneDuration;

    const setScene = (index) => {
        scenes.forEach((scene, sceneIndex) => {
            scene.classList.toggle("is-active", sceneIndex === index);
        });
    };

    scenes.forEach((scene, index) => {
        gsap.set(scene, {
            autoAlpha: index === 0 ? 1 : 0,
            scale: index === 0 ? 1 : 1.025,
        });
    });

    const timeline = gsap.timeline({
        paused: true,
        defaults: {
            ease: "power3.inOut",
        },
    });

    const addSceneTransition = (fromIndex, toIndex, position) => {
        const current = scenes[fromIndex];
        const next = scenes[toIndex];

        timeline
            .to(
                current,
                {
                    autoAlpha: 0,
                    scale: 0.96,
                    filter: "blur(14px)",
                    duration: 0.42,
                },
                position
            )
            .set(
                current,
                {
                    visibility: "hidden",
                },
                position + 0.42
            )
            .set(
                next,
                {
                    visibility: "visible",
                },
                position + 0.2
            )
            .fromTo(
                next,
                {
                    autoAlpha: 0,
                    scale: 1.035,
                    filter: "blur(16px)",
                },
                {
                    autoAlpha: 1,
                    scale: 1,
                    filter: "blur(0px)",
                    duration: 0.62,
                },
                position + 0.2
            );
    };

    /* Scene 01 */
    timeline
        .from(".ss-opening-copy > *", {
            opacity: 0,
            y: 45,
            stagger: 0.12,
            duration: 0.65,
        }, 0)
        .from(".ss-opening-object span", {
            opacity: 0,
            y: -70,
            rotation: -28,
            scale: 0.4,
            stagger: 0.09,
            duration: 0.75,
            ease: "back.out(1.8)",
        }, 0.05)
        .to(".ss-opening-object", {
            y: 24,
            rotation: 7,
            duration: 0.8,
            yoyo: true,
            repeat: 1,
            ease: "sine.inOut",
        }, 0.7);

    addSceneTransition(0, 1, 1.05);

    /* Scene 02 */
    timeline
        .from(".ss-statement-kicker", {
            opacity: 0,
            y: 24,
            duration: 0.45,
        }, 1.4)
        .from(".ss-scene--statement h2", {
            opacity: 0,
            y: 60,
            scale: 0.92,
            duration: 0.7,
        }, 1.5)
        .from(".ss-statement-line", {
            scaleX: 0,
            transformOrigin: "left center",
            duration: 0.6,
        }, 1.7);

    addSceneTransition(1, 2, 2.25);

    /* Scene 03 */
    timeline
        .from(".ss-brand-mesh", {
            scale: 1.55,
            rotation: -8,
            duration: 1.1,
        }, 2.45)
        .from(".ss-brand-reveal", {
            opacity: 0,
            scale: 0.62,
            rotation: -5,
            duration: 0.85,
            ease: "back.out(1.45)",
        }, 2.55)
        .from(".ss-brand-reveal__mark", {
            rotation: -25,
            scale: 0.5,
            duration: 0.72,
        }, 2.65)
        .from(".ss-brand-reveal div > *", {
            opacity: 0,
            y: 24,
            stagger: 0.08,
            duration: 0.5,
        }, 2.75);

    addSceneTransition(2, 3, 3.65);

    /* Scene 04 */
    timeline
        .from(".ss-identity-copy > *", {
            opacity: 0,
            x: -45,
            stagger: 0.08,
            duration: 0.55,
        }, 3.85)
        .from(".ss-product-card--blue", {
            x: -260,
            y: 150,
            rotation: -32,
            opacity: 0,
            duration: 0.8,
            ease: "back.out(1.4)",
        }, 3.9)
        .from(".ss-product-card--lime", {
            x: 280,
            y: -120,
            rotation: 34,
            opacity: 0,
            duration: 0.8,
            ease: "back.out(1.4)",
        }, 4.0)
        .from(".ss-product-card--orange", {
            y: 280,
            rotation: -20,
            opacity: 0,
            duration: 0.78,
            ease: "back.out(1.5)",
        }, 4.1)
        .to(".ss-product-card img", {
            y: -9,
            duration: 0.9,
            yoyo: true,
            repeat: 1,
            ease: "sine.inOut",
        }, 4.45);

    addSceneTransition(3, 4, 5.0);

    /* Scene 05 */
    timeline
        .from(".ss-assembly-copy > *", {
            opacity: 0,
            y: 30,
            stagger: 0.09,
            duration: 0.5,
        }, 5.2)
        .from(".ss-assembly-card--hero", {
            opacity: 0,
            scale: 0.55,
            rotation: -8,
            duration: 0.78,
            ease: "back.out(1.5)",
        }, 5.25)
        .from(".ss-assembly-card--comfort", {
            opacity: 0,
            x: -230,
            y: -120,
            rotation: -24,
            duration: 0.72,
        }, 5.35)
        .from(".ss-assembly-card--upper", {
            opacity: 0,
            x: 220,
            y: -130,
            rotation: 26,
            duration: 0.72,
        }, 5.44)
        .from(".ss-assembly-card--grip", {
            opacity: 0,
            x: 260,
            y: 140,
            rotation: 18,
            duration: 0.72,
        }, 5.53)
        .from(".ss-assembly-card--stock", {
            opacity: 0,
            x: -220,
            y: 130,
            rotation: -20,
            duration: 0.72,
        }, 5.62)
        .from(".ss-assembly-card--rating", {
            opacity: 0,
            y: 220,
            scale: 0.7,
            duration: 0.72,
        }, 5.71);

    addSceneTransition(4, 5, 6.55);

    /* Scene 06 */
    timeline
        .from(".ss-campaign-copy > *", {
            opacity: 0,
            x: -55,
            stagger: 0.1,
            duration: 0.58,
        }, 6.78)
        .from(".ss-campaign-products article:nth-child(1)", {
            opacity: 0,
            x: -300,
            rotation: -36,
            duration: 0.82,
        }, 6.83)
        .from(".ss-campaign-products article:nth-child(2)", {
            opacity: 0,
            y: -260,
            rotation: 22,
            duration: 0.82,
        }, 6.93)
        .from(".ss-campaign-products article:nth-child(3)", {
            opacity: 0,
            x: 300,
            y: 120,
            rotation: 34,
            duration: 0.82,
        }, 7.03);

    addSceneTransition(5, 6, 7.85);

    /* Scene 07 */
    timeline
        .from(".ss-workflow-copy > *", {
            opacity: 0,
            x: -45,
            stagger: 0.1,
            duration: 0.55,
        }, 8.05)
        .from(".ss-workflow-step", {
            opacity: 0,
            x: 90,
            stagger: 0.1,
            duration: 0.55,
        }, 8.12)
        .from(".ss-verification-card", {
            opacity: 0,
            y: 100,
            scale: 0.85,
            duration: 0.7,
            ease: "back.out(1.35)",
        }, 8.52)
        .to(".ss-workflow-step > i.is-current", {
            scale: 1.35,
            duration: 0.45,
            yoyo: true,
            repeat: 2,
            ease: "sine.inOut",
        }, 8.75);

    addSceneTransition(6, 7, 9.25);

    /* Scene 08 */
    timeline
        .from(".ss-final-mesh", {
            scale: 1.55,
            rotation: 8,
            duration: 1.2,
        }, 9.45)
        .from(".ss-final-brand img", {
            opacity: 0,
            scale: 0.4,
            rotation: -30,
            duration: 0.78,
            ease: "back.out(1.7)",
        }, 9.52)
        .from(".ss-final-brand h2", {
            opacity: 0,
            y: 55,
            duration: 0.68,
        }, 9.68)
        .from(".ss-final-brand p, .ss-final-brand a", {
            opacity: 0,
            y: 25,
            stagger: 0.12,
            duration: 0.48,
        }, 9.82);

    const maxTimelineTime = timeline.duration();

    const trigger = ScrollTrigger.create({
        trigger: stage,
        start: "top top+=78",
        end: `+=${Math.max(window.innerHeight * 8.5, 6200)}`,
        pin: true,
        scrub: 0.75,
        anticipatePin: 1,
        onUpdate: (self) => {
            timeline.progress(self.progress);

            if (progressBar) {
                progressBar.style.width = `${self.progress * 100}%`;
            }

            const sceneIndex = Math.min(
                Math.floor(self.progress * sceneCount),
                sceneCount - 1
            );

            setScene(sceneIndex);
        },
    });

    skip?.addEventListener("click", () => {
        const afterLaunch = document.querySelector("#ssAfterLaunch");

        if (afterLaunch) {
            trigger.kill(false);
            timeline.progress(1);
            setScene(sceneCount - 1);
            afterLaunch.scrollIntoView({
                behavior: "smooth",
                block: "start",
            });
        }
    });

    window.addEventListener("resize", () => {
        ScrollTrigger.refresh();
    });
});
