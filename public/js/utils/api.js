/*
 * API Utilities - Green Tech
 * Helper functions for API requests
 */

const DEFAULT_BASE_URL = ""; // Same origin

/**
 * Default headers for API requests
 */
const defaultHeaders = {
  "Content-Type": "application/json",
  Accept: "application/json",
};

/**
 * Build URL with query parameters
 * @param {string} path - API path
 * @param {Object} params - Query parameters
 * @returns {string}
 */
function buildUrl(path, params = {}) {
  const url = new URL(path, window.location.origin);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.append(key, value);
    }
  });
  return url.toString();
}

/**
 * Generic fetch wrapper with error handling
 * @param {string} path - API path
 * @param {Object} options - Fetch options
 * @returns {Promise<any>}
 */
async function fetchApi(path, options = {}) {
  const url = buildUrl(path, options.params);

  const config = {
    method: options.method || "GET",
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
    credentials: "same-origin",
    ...options,
  };

  if (config.body && typeof config.body === "object") {
    config.body = JSON.stringify(config.body);
  }

  try {
    const response = await fetch(url, config);

    // Handle non-JSON responses
    const contentType = response.headers.get("content-type");
    const isJson = contentType && contentType.includes("application/json");

    let data;
    if (isJson) {
      data = await response.json();
    } else {
      data = await response.text();
    }

    if (!response.ok) {
      throw new ApiError(response.status, data.message || "Error en la petición", data);
    }

    return data;
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new ApiError(0, "Error de red o conexión", { originalError: error.message });
  }
}

/**
 * Custom error class for API errors
 */
export class ApiError extends Error {
  constructor(status, message, data = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

/**
 * GET request
 * @param {string} path - API path
 * @param {Object} params - Query parameters
 * @returns {Promise<any>}
 */
export function get(path, params = {}) {
  return fetchApi(path, { method: "GET", params });
}

/**
 * POST request
 * @param {string} path - API path
 * @param {Object} body - Request body
 * @returns {Promise<any>}
 */
export function post(path, body = {}) {
  return fetchApi(path, { method: "POST", body });
}

/**
 * PUT request
 * @param {string} path - API path
 * @param {Object} body - Request body
 * @returns {Promise<any>}
 */
export function put(path, body = {}) {
  return fetchApi(path, { method: "PUT", body });
}

/**
 * PATCH request
 * @param {string} path - API path
 * @param {Object} body - Request body
 * @returns {Promise<any>}
 */
export function patch(path, body = {}) {
  return fetchApi(path, { method: "PATCH", body });
}

/**
 * DELETE request
 * @param {string} path - API path
 * @returns {Promise<any>}
 */
export function del(path) {
  return fetchApi(path, { method: "DELETE" });
}

/**
 * Upload file(s)
 * @param {string} path - API path
 * @param {FormData} formData - Form data with files
 * @returns {Promise<any>}
 */
export function upload(path, formData) {
  return fetchApi(path, {
    method: "POST",
    body: formData,
    headers: {}, // Let browser set Content-Type with boundary
  });
}

// =============================================================================
 * SPECIFIC API ENDPOINTS
 * =============================================================================

/**
 * Spaces API
 */
export const spacesApi = {
  /**
   * List spaces with filters
   * @param {Object} filters - Filter options
   * @returns {Promise<{data: Space[], total: number}>}
   */
  list: (filters = {}) => get("/api/spaces", filters),

  /**
   * Get single space
   * @param {number} id - Space ID
   * @returns {Promise<Space>}
   */
  get: (id) => get(`/api/spaces/${id}`),

  /**
   * Create space (requires auth)
   * @param {Object} data - Space data
   * @returns {Promise<Space>}
   */
  create: (data) => post("/api/spaces", data),

  /**
   * Update space (requires auth)
   * @param {number} id - Space ID
   * @param {Object} data - Space data
   * @returns {Promise<Space>}
   */
  update: (id, data) => patch(`/api/spaces/${id}`, data),

  /**
   * Delete space (requires auth)
   * @param {number} id - Space ID
   * @returns {Promise<void>}
   */
  delete: (id) => del(`/api/spaces/${id}`),
};

/**
 * Partners API
 */
export const partnersApi = {
  list: (filters = {}) => get("/api/partners", filters),
  get: (id) => get(`/api/partners/${id}`),
};

/**
 * Impact Metrics API
 */
export const metricsApi = {
  list: () => get("/api/metrics"),
  get: (key) => get(`/api/metrics/${key}`),
};

/**
 * Communities API
 */
export const communitiesApi = {
  list: (filters = {}) => get("/api/communities", filters),
  get: (id) => get(`/api/communities/${id}`),
};

/**
 * Dashboard/Stats API
 */
export const dashboardApi = {
  stats: () => get("/api/dashboard/stats"),
};

// =============================================================================
 * UTILITY FUNCTIONS
 * =============================================================================

/**
 * Check if error is a specific status
 * @param {Error} error - Error to check
 * @param {number} status - HTTP status
 * @returns {boolean}
 */
export function isStatus(error, status) {
  return error instanceof ApiError && error.status === status;
}

/**
 * Check if error is network error
 * @param {Error} error - Error to check
 * @returns {boolean}
 */
export function isNetworkError(error) {
  return error instanceof ApiError && error.status === 0;
}

/**
 * Get error message for user display
 * @param {Error} error - Error
 * @returns {string}
 */
export function getErrorMessage(error) {
  if (error instanceof ApiError) {
    if (error.status === 0) return "Sin conexión. Verifica tu internet.";
    if (error.status === 401) return "Sesión expirada. Inicia sesión nuevamente.";
    if (error.status === 403) return "No tienes permisos para esta acción.";
    if (error.status === 404) return "Recurso no encontrado.";
    if (error.status >= 500) return "Error del servidor. Intenta más tarde.";
    return error.message;
  }
  return "Error inesperado. Intenta nuevamente.";
}

/**
 * Retry function with exponential backoff
 * @param {Function} fn - Async function to retry
 * @param {Object} options - Retry options
 * @returns {Promise<any>}
 */
export async function withRetry(fn, options = {}) {
  const {
    retries = 3,
    delay = 1000,
    maxDelay = 10000,
    backoff = 2,
    shouldRetry = () => true,
  } = options;

  let lastError;
  let currentDelay = delay;

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      if (attempt === retries) break;
      if (!shouldRetry(error)) break;

      await new Promise((resolve) => setTimeout(resolve, currentDelay));
      currentDelay = Math.min(currentDelay * backoff, maxDelay);
    }
  }

  throw lastError;
}

// Export all as API namespace
export const API = {
  get,
  post,
  put,
  patch,
  delete: del,
  upload,
  spaces: spacesApi,
  partners: partnersApi,
  metrics: metricsApi,
  communities: communitiesApi,
  dashboard: dashboardApi,
  ApiError,
  isStatus,
  isNetworkError,
  getErrorMessage,
  withRetry,
};