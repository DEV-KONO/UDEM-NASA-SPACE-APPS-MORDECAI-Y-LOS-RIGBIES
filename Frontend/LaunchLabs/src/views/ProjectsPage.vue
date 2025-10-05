<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

type ProjectRow = {
  id: number
  title: string
  description: string
  program: string
  taxonomy: string
  lastUpdated: string
  url: string
  apiUrl: string
}

const projects = ref<ProjectRow[]>([])
const isLoadingProjects = ref(false)
const projectsError = ref<string | null>(null)

// Controles de búsqueda/filtros
const searchTerm = ref('')
const selectedProgram = ref('')
const selectedTaxonomy = ref('')

// Listados únicos para selects
const programs = computed(() => {
  const set = new Set(projects.value.map(p => p.program).filter(Boolean))
  return Array.from(set).sort()
})

const taxonomies = computed(() => {
  const set = new Set(projects.value.map(p => p.taxonomy).filter(Boolean))
  return Array.from(set).sort()
})

// Filtro principal
const filteredProjects = computed(() => {
  const term = searchTerm.value.trim().toLowerCase()
  return projects.value.filter(p => {
    const matchText = term
      ? (p.title?.toLowerCase().includes(term) || p.description?.toLowerCase().includes(term))
      : true
    const matchProgram = selectedProgram.value ? p.program === selectedProgram.value : true
    const matchTax = selectedTaxonomy.value ? p.taxonomy === selectedTaxonomy.value : true
    return matchText && matchProgram && matchTax
  })
})

// KPIs estilo consultora
const totalProjects = computed(() => projects.value.length)
const distinctPrograms = computed(() => new Set(projects.value.map(p => p.program)).size)
const distinctTaxonomies = computed(() => new Set(projects.value.map(p => p.taxonomy)).size)
const recentlyUpdated = computed(() => {
  // Cuenta proyectos con lastUpdated en los últimos 90 días si es fecha válida
  const now = Date.now()
  const days90 = 90 * 24 * 60 * 60 * 1000
  return projects.value.filter(p => {
    const t = Date.parse(p.lastUpdated)
    return !Number.isNaN(t) && (now - t) <= days90
  }).length
})

// "IA" local: análisis heurístico de factibilidad
type RankedProject = { project: ProjectRow; score: number; reasons: string[] }
const analysisLoading = ref(false)
const analysisResults = ref<RankedProject[] | null>(null)
const topAnalysis = computed<RankedProject | null>(() => {
  const list = analysisResults.value ?? []
  return list.length > 0 ? list[0]! : null
})
const topFive = computed<RankedProject[]>(() => {
  return (analysisResults.value ?? []).slice(0, 5)
})

const analyzeProjects = async () => {
  if (!projects.value.length) return
  analysisLoading.value = true
  try {
    // Heurística: recencia (40%), completitud de campos (30%), claridad (20%), accesibilidad (10%)
    const now = Date.now()
    const days180 = 180 * 24 * 60 * 60 * 1000
    const ranked: RankedProject[] = projects.value.map(p => {
      const reasons: string[] = []
      let score = 0

      // Recencia
      const t = Date.parse(p.lastUpdated)
      if (!Number.isNaN(t)) {
        const age = now - t
        const recency = Math.max(0, 1 - age / days180) // 1 si < hoy, 0 si > 180d
        score += recency * 40
        if (recency > 0.66) reasons.push('Actualizado recientemente')
        else if (recency > 0.33) reasons.push('Actualización intermedia')
        else reasons.push('Desactualizado')
      } else {
        reasons.push('Sin fecha de actualización')
      }

      // Completitud
      const fields = [p.title, p.description, p.program, p.taxonomy, p.url].filter(v => !!v)
      const completeness = fields.length / 5
      score += completeness * 30
      reasons.push(completeness > 0.8 ? 'Datos completos' : completeness > 0.5 ? 'Datos parciales' : 'Datos incompletos')

      // Claridad (longitud moderada de descripción)
      const descLen = (p.description || '').length
      const clarity = descLen === 0 ? 0 : descLen < 120 ? 1 : descLen < 360 ? 0.8 : 0.5
      score += clarity * 20
      if (clarity >= 0.9) reasons.push('Descripción concisa')
      else if (clarity >= 0.7) reasons.push('Descripción clara')
      else reasons.push('Descripción extensa o ausente')

      // Accesibilidad (tiene URL)
      const access = p.url ? 1 : 0
      score += access * 10
      if (access) reasons.push('Con enlace de referencia')
      else reasons.push('Sin enlace')

      return { project: p, score: Math.round(score), reasons }
    })

    ranked.sort((a, b) => b.score - a.score)
    analysisResults.value = ranked
  } finally {
    analysisLoading.value = false
  }
}

const loadCsvProjects = async () => {
  isLoadingProjects.value = true
  try {
    projectsError.value = null
    const res = await fetch('http://localhost:3001/projects')
    if (!res.ok) throw new Error('Error al cargar proyectos')
    projects.value = await res.json()
  } catch (e) {
    projectsError.value = 'No se pudo cargar proyectos. Corre: npm run import-csv y luego npm run api'
  } finally {
    isLoadingProjects.value = false
  }
}

onMounted(loadCsvProjects)
</script>

<template>
  <section class="projects-page">
    <div class="container px-4 px-lg-5">
      <!-- Header -->
      <div class="row gx-4 gx-lg-5 justify-content-center text-center mb-4">
        <div class="col-lg-9">
          <h2 class="text-white mb-2">Portafolio de Proyectos</h2>
          <p class="text-white-50">Datos convertidos desde Excel a JSON (json-server)</p>
        </div>
      </div>

      <!-- KPIs -->
      <div class="row gx-4 gx-lg-5 mb-4 kpi-row">
        <div class="col-sm-6 col-lg-3 mb-3">
          <div class="kpi-card">
            <div class="kpi-label">Proyectos</div>
            <div class="kpi-value">{{ totalProjects }}</div>
          </div>
        </div>
        <div class="col-sm-6 col-lg-3 mb-3">
          <div class="kpi-card">
            <div class="kpi-label">Programas</div>
            <div class="kpi-value">{{ distinctPrograms }}</div>
          </div>
        </div>
        <div class="col-sm-6 col-lg-3 mb-3">
          <div class="kpi-card">
            <div class="kpi-label">Taxonomías</div>
            <div class="kpi-value">{{ distinctTaxonomies }}</div>
          </div>
        </div>
        <div class="col-sm-6 col-lg-3 mb-3">
          <div class="kpi-card">
            <div class="kpi-label">Actualizados (90d)</div>
            <div class="kpi-value">{{ recentlyUpdated }}</div>
          </div>
        </div>
        <div class="col-12 col-lg-3 mb-3">
          <div class="kpi-card d-grid">
            <button class="btn btn-primary btn-sm" :disabled="analysisLoading || !projects.length" @click="analyzeProjects">
              <i class="fas fa-magic"></i>
              {{ analysisLoading ? 'Analizando…' : 'Analizar con IA' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Filtros -->
      <div class="row gx-3 gy-2 align-items-end filter-row mb-4">
        <div class="col-12 col-md-6 col-lg-5">
          <label class="form-label text-white-50">Buscar</label>
          <input v-model="searchTerm" type="text" class="form-control form-control-sm" placeholder="Título o descripción" />
        </div>
        <div class="col-6 col-md-3 col-lg-3">
          <label class="form-label text-white-50">Programa</label>
          <select v-model="selectedProgram" class="form-select form-select-sm">
            <option value="">Todos</option>
            <option v-for="pr in programs" :key="pr" :value="pr">{{ pr }}</option>
          </select>
        </div>
        <div class="col-6 col-md-3 col-lg-3">
          <label class="form-label text-white-50">Taxonomía</label>
          <select v-model="selectedTaxonomy" class="form-select form-select-sm">
            <option value="">Todas</option>
            <option v-for="tx in taxonomies" :key="tx" :value="tx">{{ tx }}</option>
          </select>
        </div>
        <div class="col-12 col-lg-1 d-grid">
          <button class="btn btn-outline-light btn-sm" @click="() => { searchTerm = ''; selectedProgram = ''; selectedTaxonomy = '' }">Limpiar</button>
        </div>
      </div>

      <!-- Panel de resultados IA -->
      <div v-if="topAnalysis" class="ai-panel mb-4">
        <div class="row gx-4 gx-lg-5 align-items-stretch">
          <div class="col-lg-6 mb-3">
            <div class="ai-card best">
              <div class="ai-title">Proyecto más factible</div>
              <div class="ai-top">
                <div class="ai-score">{{ topAnalysis.score }}</div>
                <div>
                  <div class="ai-project">{{ topAnalysis.project.title }}</div>
                  <div class="ai-tags">
                    <span class="badge program">{{ topAnalysis.project.program || '—' }}</span>
                    <span class="badge taxonomy">{{ topAnalysis.project.taxonomy || '—' }}</span>
                  </div>
                </div>
              </div>
              <ul class="ai-reasons">
                <li v-for="(r, i) in topAnalysis.reasons" :key="i">{{ r }}</li>
              </ul>
              <div class="mt-2">
                <a v-if="topAnalysis.project.url" :href="topAnalysis.project.url" target="_blank" rel="noopener" class="btn btn-sm btn-outline-primary">Ver enlace</a>
              </div>
            </div>
          </div>
          <div class="col-lg-6 mb-3">
            <div class="ai-card">
              <div class="ai-title">Ranking</div>
              <div v-for="(r, idx) in topFive" :key="r.project.id" class="rank-row">
                <div class="rank-head">
                  <span class="rank-index">#{{ idx + 1 }}</span>
                  <span class="rank-name">{{ r.project.title }}</span>
                  <span class="rank-score">{{ r.score }}</span>
                </div>
                <div class="rank-bar">
                  <div class="rank-fill" :style="{ width: (r.score) + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Estado de carga/error -->
            <div v-if="projectsError" class="alert alert-danger mb-3">{{ projectsError }}</div>
      <div v-if="isLoadingProjects" class="loading text-white-50 text-center mb-4">Cargando proyectos...</div>

      <!-- Grid de tarjetas -->
      <div v-if="!isLoadingProjects && filteredProjects.length" class="row gx-4 gx-lg-5">
        <div v-for="p in filteredProjects" :key="p.id" class="col-md-6 col-lg-4 mb-4">
          <div class="project-card">
            <div class="project-header">
              <div class="badge program">{{ p.program || '—' }}</div>
              <div class="badge taxonomy">{{ p.taxonomy || '—' }}</div>
            </div>
            <h5 class="project-title">{{ p.title }}</h5>
            <p class="project-desc">{{ p.description || 'Sin descripción' }}</p>
            <div class="project-meta">
              <span class="meta-item">
                <i class="far fa-clock"></i>
                {{ p.lastUpdated || '—' }}
              </span>
                      <a v-if="p.url" :href="p.url" target="_blank" rel="noopener" class="btn btn-sm btn-outline-primary">Ver</a>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!isLoadingProjects && !filteredProjects.length" class="text-center text-white-50">
        No se encontraron resultados con los filtros aplicados.
      </div>
    </div>
  </section>
</template>

<style scoped>
.projects-page {
  background: linear-gradient(135deg, #0f0f23, #1a1a2e 60%, #16213e);
  padding: 6rem 0;
}

/* KPIs */
.kpi-row {
  --kpi-bg: rgba(255, 255, 255, 0.06);
}

.kpi-card {
  background: var(--kpi-bg);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.kpi-label {
  color: rgba(255,255,255,0.7);
  font-size: 0.8rem;
}

.kpi-value {
  color: #fff;
  font-weight: 800;
  font-size: 1.6rem;
}

/* Filtros */
.filter-row .form-control,
.filter-row .form-select {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #fff;
}

.filter-row .form-control::placeholder { color: rgba(255,255,255,0.5); }

/* Tarjetas */
.project-card {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  padding: 1rem 1.25rem;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 40px rgba(0,0,0,0.35);
}

.project-header {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.project-header .badge {
  display: inline-block;
  padding: 0.35rem 0.5rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.badge.program {
  background: linear-gradient(135deg, #0b3d91, #1e5cb8);
  color: #fff;
  border: none;
}

.badge.taxonomy {
  background: linear-gradient(135deg, #8a2be2, #6a0dad);
  color: #fff;
  border: none;
}

.project-title {
  color: #fff;
  margin: 0.25rem 0 0.25rem;
  font-size: 1rem;
}

.project-desc {
  color: rgba(255,255,255,0.75);
  font-size: 0.85rem;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-meta {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: rgba(255,255,255,0.6);
}

.project-meta .btn { border-radius: 10px; }

.loading { opacity: 0.85; }

/* IA Panel */
.ai-panel .ai-card {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  height: 100%;
}

.ai-title {
  color: rgba(255,255,255,0.75);
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.ai-top { display: flex; gap: 0.75rem; align-items: center; }
.ai-score { 
  background: linear-gradient(135deg, #0b3d91, #1e5cb8);
  color: #fff; font-weight: 800; font-size: 1.4rem; 
  border-radius: 10px; padding: 0.35rem 0.6rem; min-width: 54px; text-align: center;
}
.ai-project { color: #fff; font-weight: 600; }
.ai-tags { margin-top: 0.25rem; display: flex; gap: 0.5rem; flex-wrap: wrap; }
.ai-reasons { margin: 0.5rem 0 0; padding-left: 1rem; color: rgba(255,255,255,0.8); }
.ai-reasons li { margin-bottom: 0.25rem; }

.rank-row { margin-bottom: 0.6rem; }
.rank-head { display: flex; align-items: center; gap: 0.5rem; color: #fff; }
.rank-index { color: #1e5cb8; font-weight: 800; }
.rank-name { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.rank-score { color: rgba(255,255,255,0.8); font-weight: 700; }
.rank-bar { height: 6px; background: rgba(255,255,255,0.1); border-radius: 6px; overflow: hidden; }
.rank-fill { height: 100%; background: linear-gradient(90deg, #0b3d91, #2c7be5); }
</style>




