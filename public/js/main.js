/*
 * Main JavaScript Entry Point - Green Tech
 * Initializes all components and utilities
 */

import { ImpactMeter } from "./components/ImpactMeter.js";
import { SpaceCard } from "./components/SpaceCard.js";
import { ScrollReveal } from "./components/ScrollReveal.js";
import { DOM } from "./utils/dom.js";

// =============================================================================
// GLOBAL INITIALIZATION
// =============================================================================

document.addEventListener("DOMContentLoaded", () => {
  // Initialize all components
  initializeComponents();

  // Initialize utilities
  initializeUtilities();

  // Mark page as loaded for CSS transitions
  document.body.classList.add("page-loaded");

  console.log("🌿 Green Tech - Initialized");
});

// =============================================================================
// COMPONENT INITIALIZATION
// =============================================================================

function initializeComponents() {
  // Impact Meter
  const impactMeters = document.querySelectorAll("[data-impact-meter]");
  impactMeters.forEach((el) => {
    try {
      new ImpactMeter(el);
    } catch (e) {
      console.warn("ImpactMeter init failed:", e);
    }
  });

  // Space Cards
  const spaceCards = document.querySelectorAll("[data-space-card]");
  spaceCards.forEach((el) => {
    try {
      new SpaceCard(el);
    } catch (e) {
      console.warn("SpaceCard init failed:", e);
    }
  });

  // Scroll Reveal
  const revealElements = document.querySelectorAll("[data-scroll-reveal]");
  if (revealElements.length > 0) {
    try {
      new ScrollReveal(revealElements);
    } catch (e) {
      console.warn("ScrollReveal init failed:", e);
    }
  }

  // Smooth scroll for anchor links
  initializeSmoothScroll();

  // Mobile menu toggle
  initializeMobileMenu();

  // Hero image comparison
  initializeHeroComparison();

  // Navbar scroll effect
  initializeNavbarScroll();
}

// =============================================================================
// UTILITY INITIALIZATION
// =============================================================================

function initializeUtilities() {
  // Add loaded class to images for fade-in
  document.querySelectorAll("img").forEach((img) => {
    if (img.complete) {
      img.classList.add("loaded");
    } else {
      img.addEventListener("load", () => img.classList.add("loaded"), { once: true });
    }
  });

  // Initialize tooltips
  initializeTooltips();

  // Initialize lazy loading for images (fallback for browsers without native support)
  initializeLazyImages();
}

// =============================================================================
// SPECIFIC FEATURE INITIALIZERS
// =============================================================================

function initializeSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", (e) => {
      const targetId = anchor.getAttribute("href");
      if (targetId === "#") return;

      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const header = document.querySelector(".header");
        const headerHeight = header ? header.offsetHeight : 0;
        const targetPosition = target.getBoundingClientRect().top + window.scrollY - headerHeight;

        window.scrollTo({
          top: targetPosition,
          behavior: "smooth",
        });

        // Update URL without scrolling
        history.pushState(null, "", targetId);

        // Focus for accessibility
        target.setAttribute("tabindex", "-1");
        target.focus({ preventScroll: true });
      }
    });
  });
}

function initializeMobileMenu() {
  const menuBtn = document.querySelector("[data-mobile-menu-btn]");
  const nav = document.querySelector("[data-mobile-nav]");

  if (menuBtn && nav) {
    menuBtn.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", isOpen);
      menuBtn.setAttribute("aria-label", isOpen ? "Cerrar menú" : "Abrir menú");
      document.body.style.overflow = isOpen ? "hidden" : "";
    });

    // Close on nav link click
    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        nav.classList.remove("open");
        menuBtn.setAttribute("aria-expanded", "false");
        document.body.style.overflow = "";
      });
    });

    // Close on escape
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        nav.classList.remove("open");
        menuBtn.setAttribute("aria-expanded", "false");
        document.body.style.overflow = "";
        menuBtn.focus();
      }
    });
  }
}

function initializeHeroComparison() {
  const comparison = document.querySelector("[data-hero-comparison]");
  if (!comparison) return;

  let isHovered = false;

  comparison.addEventListener("mouseenter", () => {
    isHovered = true;
  });

  comparison.addEventListener("mouseleave", () => {
    isHovered = false;
  });

  // Touch support for mobile
  comparison.addEventListener("touchstart", () => {
    isHovered = !isHovered;
  }, { passive: true });
}

function initializeNavbarScroll() {
  const header = document.querySelector(".header");
  if (!header) return;

  let lastScrollY = window.scrollY;
  let ticking = false;

  const updateHeader = () => {
    const scrollY = window.scrollY;

    if (scrollY > 100) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }

    if (scrollY > lastScrollY && scrollY > 200) {
      header.classList.add("hidden");
    } else {
      header.classList.remove("hidden");
    }

    lastScrollY = scrollY;
    ticking = false;
  };

  window.addEventListener("scroll", () => {
    if (!ticking) {
      requestAnimationFrame(updateHeader);
      ticking = true;
    }
  }, { passive: true });
}

function initializeTooltips() {
  // Simple CSS-based tooltips are handled in CSS
  // This is for any JS-enhanced tooltips if needed
  document.querySelectorAll("[data-tooltip]").forEach((el) => {
    el.addEventListener("focus", () => el.classList.add("tooltip-visible"));
    el.addEventListener("blur", () => el.classList.remove("tooltip-visible"));
  });
}

function initializeLazyImages() {
  // Native lazy loading is preferred (loading="lazy")
  // This is a fallback for older browsers
  if ("loading" in HTMLImageElement.prototype) return;

  const lazyImages = document.querySelectorAll("img[loading='lazy']");
  if (!lazyImages.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target;
        if (img.dataset.src) {
          img.src = img.dataset.src;
          img.removeAttribute("data-src");
        }
        observer.unobserve(img);
      }
    });
  }, { rootMargin: "100px" });

  lazyImages.forEach((img) => observer.observe(img));
}

// =============================================================================
// EXPORTS (for module usage)
// =============================================================================

export {
  initializeComponents,
  initializeUtilities,
};

// Make globally available for inline scripts if needed
window.TramaUrbanaVerde = {
  ImpactMeter,
  SpaceCard,
  ScrollReveal,
  DOM,
};
