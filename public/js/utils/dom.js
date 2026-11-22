/*
 * DOM Utilities - Green Tech
 * Helper functions for DOM manipulation and queries
 */

/**
 * Create element with attributes and children
 * @param {string} tag - HTML tag name
 * @param {Object} attrs - Attributes object
 * @param {...(string|HTMLElement)} children - Child nodes
 * @returns {HTMLElement}
 */
export function createElement(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);

  Object.entries(attrs).forEach(([key, value]) => {
    if (key === "class") {
      el.className = value;
    } else if (key === "dataset") {
      Object.entries(value).forEach(([k, v]) => {
        el.dataset[k] = v;
      });
    } else if (key === "style" && typeof value === "object") {
      Object.assign(el.style, value);
    } else if (key.startsWith("on") && typeof value === "function") {
      el.addEventListener(key.slice(2).toLowerCase(), value);
    } else {
      el.setAttribute(key, value);
    }
  });

  children.forEach((child) => {
    if (typeof child === "string") {
      el.appendChild(document.createTextNode(child));
    } else if (child instanceof Node) {
      el.appendChild(child);
    }
  });

  return el;
}

/**
 * Query selector with optional context
 * @param {string} selector - CSS selector
 * @param {Element|Document} context - Context element
 * @returns {Element|null}
 */
export function $(selector, context = document) {
  return context.querySelector(selector);
}

/**
 * Query selector all with optional context
 * @param {string} selector - CSS selector
 * @param {Element|Document} context - Context element
 * @returns {Element[]}
 */
export function $$(selector, context = document) {
  return Array.from(context.querySelectorAll(selector));
}

/**
 * Add class(es) to element
 * @param {HTMLElement} el - Element
 * @param {...string} classes - Classes to add
 */
export function addClass(el, ...classes) {
  el.classList.add(...classes);
}

/**
 * Remove class(es) from element
 * @param {HTMLElement} el - Element
 * @param {...string} classes - Classes to remove
 */
export function removeClass(el, ...classes) {
  el.classList.remove(...classes);
}

/**
 * Toggle class on element
 * @param {HTMLElement} el - Element
 * @param {string} className - Class to toggle
 * @param {boolean} force - Force add/remove
 * @returns {boolean} - New state
 */
export function toggleClass(el, className, force) {
  return el.classList.toggle(className, force);
}

/**
 * Check if element has class
 * @param {HTMLElement} el - Element
 * @param {string} className - Class to check
 * @returns {boolean}
 */
export function hasClass(el, className) {
  return el.classList.contains(className);
}

/**
 * Set multiple attributes at once
 * @param {HTMLElement} el - Element
 * @param {Object} attrs - Attributes object
 */
export function setAttrs(el, attrs) {
  Object.entries(attrs).forEach(([key, value]) => {
    if (value === null || value === undefined) {
      el.removeAttribute(key);
    } else {
      el.setAttribute(key, value);
    }
  });
}

/**
 * Get data attributes as object
 * @param {HTMLElement} el - Element
 * @returns {Object}
 */
export function getData(el) {
  return { ...el.dataset };
}

/**
 * Set HTML content safely
 * @param {HTMLElement} el - Element
 * @param {string} html - HTML string
 */
export function setHTML(el, html) {
  el.innerHTML = html;
}

/**
 * Append HTML content safely
 * @param {HTMLElement} el - Element
 * @param {string} html - HTML string
 */
export function appendHTML(el, html) {
  el.insertAdjacentHTML("beforeend", html);
}

/**
 * Remove element from DOM
 * @param {HTMLElement} el - Element
 */
export function remove(el) {
  el.remove();
}

/**
 * Empty element content
 * @param {HTMLElement} el - Element
 */
export function empty(el) {
  el.innerHTML = "";
}

/**
 * Find closest ancestor matching selector
 * @param {HTMLElement} el - Element
 * @param {string} selector - CSS selector
 * @returns {Element|null}
 */
export function closest(el, selector) {
  return el.closest(selector);
}

/**
 * Get siblings of element
 * @param {HTMLElement} el - Element
 * @returns {Element[]}
 */
export function siblings(el) {
  return Array.from(el.parentNode.children).filter((child) => child !== el);
}

/**
 * Get index of element among siblings
 * @param {HTMLElement} el - Element
 * @returns {number}
 */
export function index(el) {
  return Array.from(el.parentNode.children).indexOf(el);
}

/**
 * Debounce function
 * @param {Function} fn - Function to debounce
 * @param {number} wait - Wait time in ms
 * @returns {Function}
 */
export function debounce(fn, wait) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn.apply(this, args), wait);
  };
}

/**
 * Throttle function
 * @param {Function} fn - Function to throttle
 * @param {number} limit - Limit time in ms
 * @returns {Function}
 */
export function throttle(fn, limit) {
  let inThrottle;
  return function (...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

/**
 * Wait for element to exist in DOM
 * @param {string} selector - CSS selector
 * @param {number} timeout - Timeout in ms
 * @returns {Promise<Element>}
 */
export function waitForElement(selector, timeout = 5000) {
  return new Promise((resolve, reject) => {
    const element = document.querySelector(selector);
    if (element) return resolve(element);

    const observer = new MutationObserver(() => {
      const element = document.querySelector(selector);
      if (element) {
        observer.disconnect();
        resolve(element);
      }
    });

    observer.observe(document.body, { childList: true, subtree: true });

    setTimeout(() => {
      observer.disconnect();
      reject(new Error(`Element ${selector} not found within ${timeout}ms`));
    }, timeout);
  });
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 * @returns {Promise<boolean>}
 */
export async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // Fallback for older browsers
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand("copy");
      document.body.removeChild(textarea);
      return true;
    } catch {
      document.body.removeChild(textarea);
      return false;
    }
  }
}

/**
 * Generate unique ID
 * @param {string} prefix - Prefix for ID
 * @returns {string}
 */
export function uniqueId(prefix = "id") {
  return `${prefix}-${Math.random().toString(36).slice(2, 9)}`;
}

/**
 * Check if element is in viewport
 * @param {HTMLElement} el - Element
 * @param {number} threshold - Threshold (0-1)
 * @returns {boolean}
 */
export function inViewport(el, threshold = 0) {
  const rect = el.getBoundingClientRect();
  const windowHeight = window.innerHeight || document.documentElement.clientHeight;
  const windowWidth = window.innerWidth || document.documentElement.clientWidth;

  const vertInView = rect.top <= windowHeight * (1 - threshold) && rect.bottom >= windowHeight * threshold;
  const horInView = rect.left <= windowWidth * (1 - threshold) && rect.right >= windowWidth * threshold;

  return vertInView && horInView;
}

/**
 * Smooth scroll to element
 * @param {HTMLElement|string} target - Element or selector
 * @param {Object} options - Scroll options
 */
export function scrollTo(target, options = {}) {
  const el = typeof target === "string" ? document.querySelector(target) : target;
  if (!el) return;

  const header = document.querySelector(".header");
  const headerHeight = header ? header.offsetHeight : 0;

  const targetPosition = el.getBoundingClientRect().top + window.scrollY - headerHeight;

  window.scrollTo({
    top: targetPosition,
    behavior: options.behavior || "smooth",
    ...options,
  });
}

/**
 * Lock/unlock body scroll
 * @param {boolean} lock - Whether to lock
 */
export function lockScroll(lock) {
  if (lock) {
    document.body.style.overflow = "hidden";
    document.body.style.paddingRight = `${window.innerWidth - document.documentElement.clientWidth}px`;
  } else {
    document.body.style.overflow = "";
    document.body.style.paddingRight = "";
  }
}

// Export all as DOM namespace
export const DOM = {
  create: createElement,
  $,
  $$,
  addClass,
  removeClass,
  toggleClass,
  hasClass,
  setAttrs,
  getData,
  setHTML,
  appendHTML,
  remove,
  empty,
  closest,
  siblings,
  index,
  debounce,
  throttle,
  waitForElement,
  copyToClipboard,
  uniqueId,
  inViewport,
  scrollTo,
  lockScroll,
};