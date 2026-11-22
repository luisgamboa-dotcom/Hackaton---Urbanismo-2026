

export class SpaceCard {
  
  constructor(element) {
    this.element = element;
    this.imageEl = element.querySelector("[data-space-image]");
    this.beforeEl = element.querySelector("[data-space-before]");
    this.afterEl = element.querySelector("[data-space-after]");
    this.statusEl = element.querySelector("[data-space-status]");
    this.categoryEl = element.querySelector("[data-space-category]");
    this.comparisonEl = element.querySelector("[data-space-comparison]");

    
    this.isComparing = false;

    this.init();
  }

  init() {
    
    if (this.comparisonEl && this.beforeEl && this.afterEl) {
      this.initComparison();
    }

    
    this.initKeyboard();

    
    this.initFocus();

    
    this.initLazyImages();
  }

  initComparison() {
    
    this.comparisonEl.addEventListener("mouseenter", () => this.showAfter());
    this.comparisonEl.addEventListener("mouseleave", () => this.showBefore());

    
    this.comparisonEl.addEventListener("touchstart", (e) => {
      e.preventDefault();
      this.toggleComparison();
    }, { passive: false });

    
    this.comparisonEl.addEventListener("click", (e) => {
      
      if (e.target.closest("a, button")) return;
      this.toggleComparison();
    });
  }

  initKeyboard() {
    this.element.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        if (this.comparisonEl) {
          e.preventDefault();
          this.toggleComparison();
        }
      }
    });

    
    if (this.element.querySelector("a, button")) {
      this.element.setAttribute("tabindex", "0");
    }
  }

  initFocus() {
    this.element.addEventListener("focusin", () => {
      this.element.classList.add("card--focused");
    });

    this.element.addEventListener("focusout", () => {
      this.element.classList.remove("card--focused");
    });
  }

  initLazyImages() {
    const images = this.element.querySelectorAll("img[loading='lazy']");
    images.forEach((img) => {
      if (img.complete) {
        img.classList.add("loaded");
      } else {
        img.addEventListener("load", () => img.classList.add("loaded"), { once: true });
      }
    });
  }

  showBefore() {
    if (!this.isComparing) return;
    this.isComparing = false;
    this.beforeEl.style.opacity = "1";
    this.afterEl.style.opacity = "0";
    this.updateComparisonLabel("Antes");
  }

  showAfter() {
    if (this.isComparing) return;
    this.isComparing = true;
    this.beforeEl.style.opacity = "0";
    this.afterEl.style.opacity = "1";
    this.updateComparisonLabel("Después");
  }

  toggleComparison() {
    if (this.isComparing) {
      this.showBefore();
    } else {
      this.showAfter();
    }
  }

  updateComparisonLabel(state) {
    const labelEl = this.element.querySelector("[data-comparison-label]");
    if (labelEl) {
      labelEl.textContent = state;
    }
  }

  
  updateStatus(status) {
    if (!this.statusEl) return;

    const statusClasses = {
      identified: "status-identified",
      in_progress: "status-in_progress",
      completed: "status-completed",
      maintained: "status-maintained",
    };

    
    Object.values(statusClasses).forEach((cls) => {
      this.statusEl.classList.remove(cls);
    });

    
    if (statusClasses[status]) {
      this.statusEl.classList.add(statusClasses[status]);
    }

    
    const labels = {
      identified: "Identificado",
      in_progress: "En Progreso",
      completed: "Completado",
      maintained: "En Mantenimiento",
    };
    this.statusEl.textContent = labels[status] || status;
  }

  
  destroy() {
    
    this.element.classList.remove("card--focused");
  }
}


if (typeof window !== "undefined" && !window.TramaUrbanaVerde) {
  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-space-card]").forEach((el) => {
      new SpaceCard(el);
    });
  });
}