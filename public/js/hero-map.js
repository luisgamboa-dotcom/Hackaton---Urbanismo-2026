// =============================================================================
// HERO MAP - Leaflet + OpenStreetMap
// =============================================================================

(function() {
  'use strict';

  // Configuración
  const CONFIG = {
    // Centro inicial: Santiago
    center: [-33.4372, -70.6506],
    zoom: 12,
    minZoom: 10,
    maxZoom: 18,
    
    // Tile layer OSM
    tileUrl: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    tileAttribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    
    // API endpoint
    apiUrl: '/api/map/spaces',
    
    // Colores por estado (CSS custom properties)
    statusColors: {
      completed: 'var(--color-primary)',      // Verde
      in_progress: 'var(--color-tertiary)',   // Terracota
      identified: 'var(--color-on-surface-variant)' // Gris
    },
    
    // Iconos por categoría
    categoryIcons: {
      pocket_park: '🌳',
      green_corridor: '🌿',
      community_garden: '🥕',
      resting_area: '🪑',
      urban_forest: '🌲',
      playground: '🛝',
      abandoned_land: '⚠️',
      dumping_ground: '🗑️'
    },

    // Colores específicos para terrenos abandonados/vertederos (rojo/naranja)
    problemCategoryColors: {
      abandoned_land: '#ef4444',    // Rojo
      dumping_ground: '#f97316'     // Naranja
    }
  };

  let map = null;
  let markersLayer = null; // MarkerClusterGroup
  let allMarkers = [];     // Referencia a todos los marcadores para filtrado
  let currentFilter = '';

  // ---------------------------------------------------------------------------
  // Inicialización
  // ---------------------------------------------------------------------------
  function initHeroMap() {
    const container = document.getElementById('hero-map');
    const filterSelect = document.getElementById('hero-map-filter');

    if (!container) return;

    // Ensure container has dimensions before initializing Leaflet
    if (container.offsetWidth === 0 || container.offsetHeight === 0) {
      // Container not visible yet, retry after a short delay
      console.warn('Hero map: container has no dimensions, retrying...');
      setTimeout(initHeroMap, 100);
      return;
    }

    // Force container to have explicit dimensions as fallback
    if (!container.style.height) {
      container.style.height = '380px';
    }
    if (!container.style.width) {
      container.style.width = '100%';
    }

    // Crear mapa
    map = L.map('hero-map', {
      center: CONFIG.center,
      zoom: CONFIG.zoom,
      minZoom: CONFIG.minZoom,
      maxZoom: CONFIG.maxZoom,
      zoomControl: true,
      scrollWheelZoom: false, // Evita scroll accidental en página
      tap: true,              // Touch friendly
      attributionControl: true
    });
    
    // Tile layer OSM
    L.tileLayer(CONFIG.tileUrl, {
      attribution: CONFIG.tileAttribution,
      maxZoom: 19
    }).addTo(map);
    
    // Marker Cluster Group
    markersLayer = L.markerClusterGroup({
      spiderfyOnMaxZoom: true,
      showCoverageOnHover: false,
      zoomToBoundsOnClick: true,
      maxClusterRadius: 50,
      iconCreateFunction: createClusterIcon
    });
    map.addLayer(markersLayer);
    
    // Cargar datos
    loadSpacesData();
    
    // Evento filtro
    if (filterSelect) {
      filterSelect.addEventListener('change', (e) => {
        currentFilter = e.target.value;
        filterMarkers(currentFilter);
      });
    }

    // Botón pantalla completa - apunta al contenedor .hero-after-map (data-hero-map)
    const fullscreenBtn = document.getElementById('hero-map-fullscreen');
    const mapWrapper = document.querySelector('[data-hero-map]');
    if (fullscreenBtn && mapWrapper) {
      fullscreenBtn.addEventListener('click', () => {
        toggleFullscreen(mapWrapper, fullscreenBtn);
      });
    }

    // Lazy-load: activar scroll wheel zoom solo al hacer hover
    container.addEventListener('mouseenter', () => {
      map.scrollWheelZoom.enable();
    });
    container.addEventListener('mouseleave', () => {
      map.scrollWheelZoom.disable();
    });
    
    // Exponer para debug
    window.heroMap = { map, markersLayer, filterMarkers };
  }

  // ---------------------------------------------------------------------------
  // Cargar datos desde API
  // ---------------------------------------------------------------------------
  async function loadSpacesData() {
    try {
      const response = await fetch(CONFIG.apiUrl);
      if (!response.ok) throw new Error('Error cargando espacios');
      
      const data = await response.json();
      renderMarkers(data.spaces || data);
    } catch (error) {
      console.warn('Hero map: usando datos de fallback', error);
      // Fallback: datos embebidos en template
      renderMarkers(window.HERO_MAP_SPACES || []);
    }
  }

  // ---------------------------------------------------------------------------
  // Renderizar marcadores
  // ---------------------------------------------------------------------------
  function renderMarkers(spaces) {
    if (!markersLayer || !map) return;
    
    markersLayer.clearLayers();
    allMarkers = [];
    
    spaces.forEach(space => {
      if (!space.latitude || !space.longitude) return;
      
      const marker = createMarker(space);
      markersLayer.addLayer(marker);
      allMarkers.push({ marker, space, category: space.category, status: space.status });
    });
    
    // Ajustar vista a marcadores si hay datos
    if (allMarkers.length > 0) {
      const group = new L.featureGroup(allMarkers.map(m => m.marker));
      map.fitBounds(group.getBounds().pad(0.1));
    }
  }

  // ---------------------------------------------------------------------------
  // Crear marcador individual
  // ---------------------------------------------------------------------------
  function createMarker(space) {
    // Usar colores especiales para terrenos problemáticos
    let color = CONFIG.statusColors[space.status] || CONFIG.statusColors.identified;
    if (CONFIG.problemCategoryColors[space.category]) {
      color = CONFIG.problemCategoryColors[space.category];
    }

    const iconHtml = CONFIG.categoryIcons[space.category] || '📍';

    // Custom div icon con tus colores
    const icon = L.divIcon({
      className: 'hero-map-marker',
      html: `
        <div class="marker-inner" style="--marker-color: ${color};">
          <span class="marker-icon">${iconHtml}</span>
          <span class="marker-pulse"></span>
        </div>
      `,
      iconSize: [36, 36],
      iconAnchor: [18, 36],
      popupAnchor: [0, -36]
    });

    const marker = L.marker([space.latitude, space.longitude], { icon });

    // Popup personalizado - más compacto
    const popupContent = createPopupContent(space);
    marker.bindPopup(popupContent, {
      className: 'hero-map-popup',
      maxWidth: 240,
      minWidth: 200
    });

    return marker;
  }

  // ---------------------------------------------------------------------------
  // Crear icono de cluster personalizado
  // ---------------------------------------------------------------------------
  function createClusterIcon(cluster) {
    const count = cluster.getChildCount();
    const color = count > 10 ? 'var(--color-primary)' : 'var(--color-tertiary)';
    
    return L.divIcon({
      className: 'hero-map-cluster',
      html: `<div class="cluster-inner" style="--cluster-color: ${color};">${count}</div>`,
      iconSize: count > 10 ? [48, 48] : [40, 40],
      iconAnchor: [24, 24]
    });
  }

  // ---------------------------------------------------------------------------
  // Contenido del popup
  // ---------------------------------------------------------------------------
  function createPopupContent(space) {
    const statusLabel = {
      completed: 'Completado',
      in_progress: 'En Progreso',
      identified: 'Identificado'
    }[space.status] || space.status;
    
    const categoryLabel = {
      pocket_park: 'Plaza de Bolsillo',
      green_corridor: 'Corredor Verde',
      community_garden: 'Huerto Comunitario',
      resting_area: 'Zona de Descanso',
      urban_forest: 'Mini Bosque Urbano',
      playground: 'Área de Juegos',
      abandoned_land: 'Terreno Abandonado',
      dumping_ground: 'Vertedero Ilegal'
    }[space.category] || space.category;
    
    const area = space.area_m2 ? `${space.area_m2.toLocaleString('es-CL')} m²` : '—';
    
    return `
      <div class="popup-content">
        <h4 class="popup-title">${escapeHtml(space.name)}</h4>
        <div class="popup-meta">
          <span class="popup-badge status-${space.status}">${statusLabel}</span>
          <span class="popup-badge category-${space.category}">${categoryLabel}</span>
        </div>
        <p class="popup-commune">
          <svg class="icon icon-xs" aria-hidden="true"><use href="#icon-map-pin"></use></svg>
          ${escapeHtml(space.commune || 'Sin comuna')}
        </p>
        <p class="popup-area">
          <svg class="icon icon-xs" aria-hidden="true"><use href="#icon-square"></use></svg>
          ${area}
        </p>
        ${space.description ? `<p class="popup-desc">${escapeHtml(space.description.substring(0, 120))}…</p>` : ''}
        <a href="/espacios/${space.id}" class="btn btn-primary btn-sm btn-block popup-link">
          Ver detalles
          <svg class="icon icon-sm" aria-hidden="true"><use href="#icon-arrow-right"></use></svg>
        </a>
      </div>
    `;
  }

  // ---------------------------------------------------------------------------
  // Filtrado por categoría
  // ---------------------------------------------------------------------------
  function filterMarkers(category) {
    allMarkers.forEach(({ marker, space }) => {
      const matches = !category || space.category === category;
      if (matches) {
        markersLayer.addLayer(marker);
      } else {
        markersLayer.removeLayer(marker);
      }
    });
  }

  // ---------------------------------------------------------------------------
  // Pantalla completa
  // ---------------------------------------------------------------------------
  function toggleFullscreen(element, button) {
    if (!document.fullscreenElement) {
      // Entrar en pantalla completa
      element.requestFullscreen().catch(err => {
        console.warn('Error al entrar en pantalla completa:', err);
      });
      button.innerHTML = '<svg class="icon icon-sm" aria-hidden="true"><use href="#icon-minimize"></use></svg>';
      button.setAttribute('aria-label', 'Salir de pantalla completa');
      button.title = 'Salir de pantalla completa';
    } else {
      // Salir de pantalla completa
      document.exitFullscreen().catch(err => {
        console.warn('Error al salir de pantalla completa:', err);
      });
      button.innerHTML = '<svg class="icon icon-sm" aria-hidden="true"><use href="#icon-maximize"></use></svg>';
      button.setAttribute('aria-label', 'Pantalla completa');
      button.title = 'Pantalla completa';
    }
  }

  // Escuchar cambios de pantalla completa (por si el usuario usa ESC o F11)
  document.addEventListener('fullscreenchange', () => {
    const button = document.getElementById('hero-map-fullscreen');
    if (button) {
      if (document.fullscreenElement) {
        button.innerHTML = '<svg class="icon icon-sm" aria-hidden="true"><use href="#icon-minimize"></use></svg>';
        button.setAttribute('aria-label', 'Salir de pantalla completa');
        button.title = 'Salir de pantalla completa';
      } else {
        button.innerHTML = '<svg class="icon icon-sm" aria-hidden="true"><use href="#icon-maximize"></use></svg>';
        button.setAttribute('aria-label', 'Pantalla completa');
        button.title = 'Pantalla completa';
      }
    }
  });

  // ---------------------------------------------------------------------------
  // Utilidades
  // ---------------------------------------------------------------------------
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // ---------------------------------------------------------------------------
  // Auto-inicializar cuando el DOM esté listo
  // ---------------------------------------------------------------------------
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHeroMap);
  } else {
    initHeroMap();
  }

})();