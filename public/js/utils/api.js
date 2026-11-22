

const DEFAULT_BASE_URL = ""; 


const defaultHeaders = {
  "Content-Type": "application/json",
  Accept: "application/json",
};


function buildUrl(path, params = {}) {
  const url = new URL(path, window.location.origin);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.append(key, value);
    }
  });
  return url.toString();
}


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


export class ApiError extends Error {
  constructor(status, message, data = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}


export function get(path, params = {}) {
  return fetchApi(path, { method: "GET", params });
}


export function post(path, body = {}) {
  return fetchApi(path, { method: "POST", body });
}


export function put(path, body = {}) {
  return fetchApi(path, { method: "PUT", body });
}


export function patch(path, body = {}) {
  return fetchApi(path, { method: "PATCH", body });
}


export function del(path) {
  return fetchApi(path, { method: "DELETE" });
}


export function upload(path, formData) {
  return fetchApi(path, {
    method: "POST",
    body: formData,
    headers: {}, 
  });
}


 * SPECIFIC API ENDPOINTS
 * =============================================================================


export const spacesApi = {
  
  list: (filters = {}) => get("/api/spaces", filters),

  
  get: (id) => get(`/api/spaces/${id}`),

  
  create: (data) => post("/api/spaces", data),

  
  update: (id, data) => patch(`/api/spaces/${id}`, data),

  
  delete: (id) => del(`/api/spaces/${id}`),
};


export const partnersApi = {
  list: (filters = {}) => get("/api/partners", filters),
  get: (id) => get(`/api/partners/${id}`),
};


export const metricsApi = {
  list: () => get("/api/metrics"),
  get: (key) => get(`/api/metrics/${key}`),
};


export const communitiesApi = {
  list: (filters = {}) => get("/api/communities", filters),
  get: (id) => get(`/api/communities/${id}`),
};


export const dashboardApi = {
  stats: () => get("/api/dashboard/stats"),
};


 * UTILITY FUNCTIONS
 * =============================================================================


export function isStatus(error, status) {
  return error instanceof ApiError && error.status === status;
}


export function isNetworkError(error) {
  return error instanceof ApiError && error.status === 0;
}


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