


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


export function $(selector, context = document) {
  return context.querySelector(selector);
}


export function $$(selector, context = document) {
  return Array.from(context.querySelectorAll(selector));
}


export function addClass(el, ...classes) {
  el.classList.add(...classes);
}


export function removeClass(el, ...classes) {
  el.classList.remove(...classes);
}


export function toggleClass(el, className, force) {
  return el.classList.toggle(className, force);
}


export function hasClass(el, className) {
  return el.classList.contains(className);
}


export function setAttrs(el, attrs) {
  Object.entries(attrs).forEach(([key, value]) => {
    if (value === null || value === undefined) {
      el.removeAttribute(key);
    } else {
      el.setAttribute(key, value);
    }
  });
}


export function getData(el) {
  return { ...el.dataset };
}


export function setHTML(el, html) {
  el.innerHTML = html;
}


export function appendHTML(el, html) {
  el.insertAdjacentHTML("beforeend", html);
}


export function remove(el) {
  el.remove();
}


export function empty(el) {
  el.innerHTML = "";
}


export function closest(el, selector) {
  return el.closest(selector);
}


export function siblings(el) {
  return Array.from(el.parentNode.children).filter((child) => child !== el);
}


export function index(el) {
  return Array.from(el.parentNode.children).indexOf(el);
}


export function debounce(fn, wait) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn.apply(this, args), wait);
  };
}


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


export async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    
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


export function uniqueId(prefix = "id") {
  return `${prefix}-${Math.random().toString(36).slice(2, 9)}`;
}


export function inViewport(el, threshold = 0) {
  const rect = el.getBoundingClientRect();
  const windowHeight = window.innerHeight || document.documentElement.clientHeight;
  const windowWidth = window.innerWidth || document.documentElement.clientWidth;

  const vertInView = rect.top <= windowHeight * (1 - threshold) && rect.bottom >= windowHeight * threshold;
  const horInView = rect.left <= windowWidth * (1 - threshold) && rect.right >= windowWidth * threshold;

  return vertInView && horInView;
}


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


export function lockScroll(lock) {
  if (lock) {
    document.body.style.overflow = "hidden";
    document.body.style.paddingRight = `${window.innerWidth - document.documentElement.clientWidth}px`;
  } else {
    document.body.style.overflow = "";
    document.body.style.paddingRight = "";
  }
}


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