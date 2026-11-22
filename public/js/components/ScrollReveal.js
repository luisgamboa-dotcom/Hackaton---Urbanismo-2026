

export class ScrollReveal {
  
  constructor(elements, options = {}) {
    this.elements = Array.isArray(elements) ? elements : Array.from(elements);
    this.options = {
      threshold: options.threshold || 0.1,
      rootMargin: options.rootMargin || "0px 0px -50px 0px",
      delay: options.delay || 0,
      stagger: options.stagger || 100,
      once: options.once !== false,
      ...options,
    };

    this.observer = null;
    this.animatedElements = new WeakSet();

    this.init();
  }

  init() {
    
    this.elements.forEach((el, index) => {
      el.classList.add("scroll-reveal");
      el.style.transitionDelay = `${this.options.delay + index * this.options.stagger}ms`;
    });

    
    if ("IntersectionObserver" in window) {
      this.observer = new IntersectionObserver(
        (entries) => this.handleIntersection(entries),
        {
          rootMargin: this.options.rootMargin,
          threshold: this.options.threshold,
        }
      );

      this.elements.forEach((el) => this.observer.observe(el));
    } else {
      
      this.elements.forEach((el) => el.classList.add("visible"));
    }
  }

  handleIntersection(entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const el = entry.target;
        el.classList.add("visible");
        this.animatedElements.add(el);

        if (this.options.once) {
          this.observer.unobserve(el);
        }
      } else if (!this.options.once) {
        
        entry.target.classList.remove("visible");
      }
    });
  }

  
  add(elements) {
    const newElements = Array.isArray(elements) ? elements : Array.from(elements);
    newElements.forEach((el, index) => {
      const totalIndex = this.elements.length + index;
      el.classList.add("scroll-reveal");
      el.style.transitionDelay = `${this.options.delay + totalIndex * this.options.stagger}ms`;
      this.elements.push(el);
      if (this.observer) {
        this.observer.observe(el);
      }
    });
  }

  
  remove(elements) {
    const toRemove = Array.isArray(elements) ? elements : Array.from(elements);
    toRemove.forEach((el) => {
      const index = this.elements.indexOf(el);
      if (index > -1) {
        this.elements.splice(index, 1);
        if (this.observer) {
          this.observer.unobserve(el);
        }
      }
    });
  }

  
  refresh() {
    if (this.observer) {
      this.observer.disconnect();
      this.elements.forEach((el) => this.observer.observe(el));
    }
  }

  
  destroy() {
    if (this.observer) {
      this.observer.disconnect();
      this.observer = null;
    }
    this.elements = [];
    this.animatedElements = new WeakSet();
  }
}


if (typeof window !== "undefined" && !window.TramaUrbanaVerde) {
  document.addEventListener("DOMContentLoaded", () => {
    const elements = document.querySelectorAll("[data-scroll-reveal]");
    if (elements.length > 0) {
      new ScrollReveal(elements);
    }
  });
}