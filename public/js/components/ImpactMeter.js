

export class ImpactMeter {
  
  constructor(element) {
    this.element = element;
    this.fillEl = element.querySelector("[data-impact-fill]");
    this.markerEl = element.querySelector("[data-impact-marker]");
    this.valueEl = element.querySelector("[data-impact-value]");
    this.targetEl = element.querySelector("[data-impact-target]");

    
    this.targetValue = parseFloat(this.element.dataset.impactTarget || "100");
    this.currentValue = parseFloat(this.element.dataset.impactValue || "0");
    this.unit = this.element.dataset.impactUnit || "";
    this.duration = parseInt(this.element.dataset.impactDuration || "1500", 10);
    this.easing = this.element.dataset.impactEasing || "ease-out";

    
    this.animated = false;
    this.animationFrame = null;

    this.init();
  }

  init() {
    
    this.setProgress(0);

    
    if ("IntersectionObserver" in window) {
      this.observer = new IntersectionObserver(
        (entries) => this.handleIntersection(entries),
        {
          rootMargin: "0px 0px -50px 0px",
          threshold: 0.3,
        }
      );
      this.observer.observe(this.element);
    } else {
      
      this.animate();
    }
  }

  handleIntersection(entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting && !this.animated) {
        this.animate();
        this.observer.unobserve(this.element);
      }
    });
  }

  animate() {
    if (this.animated) return;
    this.animated = true;

    const startTime = performance.now();
    const startValue = 0;
    const endValue = this.currentValue;
    const percentage = Math.min((this.currentValue / this.targetValue) * 100, 100);

    const animateFrame = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / this.duration, 1);

      
      const easedProgress = this.applyEasing(progress);

      
      const currentVal = startValue + (endValue - startValue) * easedProgress;
      const currentPct = percentage * easedProgress;

      this.setProgress(currentPct, currentVal);

      if (progress < 1) {
        this.animationFrame = requestAnimationFrame(animateFrame);
      } else {
        this.setProgress(percentage, endValue);
        this.onComplete();
      }
    };

    this.animationFrame = requestAnimationFrame(animateFrame);
  }

  applyEasing(t) {
    switch (this.easing) {
      case "ease-out":
        return 1 - Math.pow(1 - t, 3); 
      case "ease-in-out":
        return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
      case "linear":
      default:
        return t;
    }
  }

  setProgress(percentage, displayValue = null) {
    
    const pct = Math.max(0, Math.min(100, percentage));

    
    if (this.fillEl) {
      this.fillEl.style.width = `${pct}%`;
    }

    
    if (this.markerEl) {
      this.markerEl.style.left = `${pct}%`;
    }

    
    if (this.valueEl && displayValue !== null) {
      this.valueEl.textContent = this.formatValue(displayValue);
    }
  }

  formatValue(value) {
    
    const formatted = Math.round(value).toLocaleString("es-CL");
    return this.unit ? `${formatted} ${this.unit}` : formatted;
  }

  onComplete() {
    
    this.element.dispatchEvent(
      new CustomEvent("impactmeter:complete", {
        detail: { value: this.currentValue, target: this.targetValue },
        bubbles: true,
      })
    );

    
    this.element.classList.add("impact-meter--completed");
  }

  
  update(newValue, newTarget = null) {
    this.currentValue = newValue;
    if (newTarget !== null) this.targetValue = newTarget;
    this.animated = false;
    this.setProgress(0);
    this.animate();
  }

  
  destroy() {
    if (this.animationFrame) {
      cancelAnimationFrame(this.animationFrame);
    }
    if (this.observer) {
      this.observer.disconnect();
    }
  }
}


if (typeof window !== "undefined" && !window.TramaUrbanaVerde) {
  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-impact-meter]").forEach((el) => {
      new ImpactMeter(el);
    });
  });
}