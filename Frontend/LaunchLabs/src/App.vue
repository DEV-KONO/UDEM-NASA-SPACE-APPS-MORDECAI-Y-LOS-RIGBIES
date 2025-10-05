<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { getProducts, createProduct, type Product } from '@/api/products'
import { useRoute } from 'vue-router'

// Tipos para proyectos importados desde CSV -> json-server
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

// Variables reactivas para el simulador
const isRunning = ref(false)
const currentSpeed = ref(1)
const currentScenario = ref('Lanzamiento básico')
const launchCount = ref(0)
const totalSavings = ref(2300000)
const fuelSaved = ref(89)

// Variables adicionales para simulación avanzada
const altitude = ref(0)
const velocity = ref(0)
const payload = ref(0)
const missionTime = ref(0)
const energyEfficiency = ref(0)
const cableTension = ref(0)
const isLaunching = ref(false)
const missionPhase = ref('En Espera')

// Intervalos para animaciones
let statsInterval: number | null = null
let animationInterval: number | null = null
let missionInterval: number | null = null

// Función para iniciar/pausar simulación
const toggleSimulation = () => {
  isRunning.value = !isRunning.value
  
  if (isRunning.value) {
    startSimulation()
  } else {
    stopSimulation()
  }
}

// Función para cambiar velocidad
const changeSpeed = (speed: number) => {
  currentSpeed.value = speed
  updateAnimations()
}

// Función para cambiar escenario
const changeScenario = (scenario: string) => {
  currentScenario.value = scenario
  // Aquí podrías cambiar los parámetros de la animación según el escenario
}

// Función para iniciar la simulación
const startSimulation = () => {
  // Iniciar estadísticas en tiempo real
  statsInterval = setInterval(() => {
    if (isRunning.value) {
      updateMissionData()
    }
  }, 1000)
  
  // Iniciar simulación de misión
  missionInterval = setInterval(() => {
    if (isRunning.value && isLaunching.value) {
      simulateLaunch()
    }
  }, 100)
  
  // Iniciar animaciones
  updateAnimations()
}

// Función para actualizar datos de misión
const updateMissionData = () => {
  // Incrementar contador de lanzamientos
  launchCount.value += Math.floor(Math.random() * 2) + 1
  
  // Calcular ahorro basado en lanzamientos
  const savingsPerLaunch = currentScenario.value === 'Misión a Marte' ? 50000 : 
                          currentScenario.value === 'Carga pesada' ? 25000 : 15000
  totalSavings.value += savingsPerLaunch * (Math.floor(Math.random() * 2) + 1)
  
  // Actualizar porcentaje de combustible ahorrado
  fuelSaved.value = Math.min(95, fuelSaved.value + Math.random() * 0.1)
  
  // Actualizar eficiencia energética
  energyEfficiency.value = Math.min(98, energyEfficiency.value + Math.random() * 0.2)
}

// Función para simular lanzamiento
const simulateLaunch = () => {
  missionTime.value += 0.1
  
  // Simular ascenso
  if (missionPhase.value === 'Ascenso') {
    altitude.value += velocity.value * 0.1
    velocity.value += 0.5 // Aceleración
    cableTension.value = altitude.value * 0.1
    
    if (altitude.value >= 200) {
      missionPhase.value = 'Órbita'
      velocity.value = 7.8 // Velocidad orbital
    }
  }
  
  // Simular órbita
  if (missionPhase.value === 'Órbita') {
    altitude.value = 200 + Math.sin(missionTime.value * 0.1) * 10
    cableTension.value = 20 + Math.cos(missionTime.value * 0.1) * 5
  }
  
  // Simular descenso
  if (missionPhase.value === 'Descenso') {
    altitude.value -= velocity.value * 0.1
    velocity.value -= 0.3 // Desaceleración
    
    if (altitude.value <= 0) {
      missionPhase.value = 'Completado'
      isLaunching.value = false
      missionTime.value = 0
    }
  }
}

// Función para detener la simulación
const stopSimulation = () => {
  if (statsInterval) {
    clearInterval(statsInterval)
    statsInterval = null
  }
  
  if (animationInterval) {
    clearInterval(animationInterval)
    animationInterval = null
  }
  
  if (missionInterval) {
    clearInterval(missionInterval)
    missionInterval = null
  }
}

// Función para iniciar un lanzamiento
const startLaunch = () => {
  if (!isRunning.value) return
  
  isLaunching.value = true
  missionPhase.value = 'Ascenso'
  altitude.value = 0
  velocity.value = 0
  missionTime.value = 0
  payload.value = currentScenario.value === 'Misión a Marte' ? 1000 : 
                 currentScenario.value === 'Carga pesada' ? 5000 : 2000
}

// Función para cambiar a fase de descenso
const startDescent = () => {
  if (missionPhase.value === 'Órbita') {
    missionPhase.value = 'Descenso'
  }
}

// Función para resetear misión
const resetMission = () => {
  isLaunching.value = false
  missionPhase.value = 'En Espera'
  altitude.value = 0
  velocity.value = 0
  missionTime.value = 0
  payload.value = 0
  cableTension.value = 0
}

// Función para actualizar animaciones según velocidad
const updateAnimations = () => {
  if (animationInterval) {
    clearInterval(animationInterval)
  }
  
  // Siempre establecer la variable CSS, no solo cuando está corriendo
  const root = document.documentElement
  root.style.setProperty('--animation-speed', currentSpeed.value.toString())
}

// Función para formatear números
const formatNumber = (num: number) => {
  if (num >= 1000000000) {
    return (num / 1000000000).toFixed(1) + 'B'
  } else if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

// Función para obtener clase CSS de fase de misión
const getPhaseClass = (phase: string) => {
  switch (phase) {
    case 'En Espera':
      return 'bg-secondary'
    case 'Ascenso':
      return 'bg-danger'
    case 'Órbita':
      return 'bg-primary'
    case 'Descenso':
      return 'bg-warning'
    case 'Completado':
      return 'bg-success'
    default:
      return 'bg-secondary'
  }
}

// Inicializar animaciones al montar el componente
onMounted(() => {
  updateAnimations()
  // Cargar productos al iniciar
  loadProducts()
  // Cargar proyectos CSV a la tabla
  loadCsvProjects()
})

// Limpiar intervalos al desmontar el componente
onUnmounted(() => {
  stopSimulation()
})

// =====================
// Productos (API demo)
// =====================
const products = ref<Product[]>([])
const isLoadingProducts = ref(false)
const isAddingProduct = ref(false)
const apiError = ref<string | null>(null)

const loadProducts = async () => {
  isLoadingProducts.value = true
  try {
    apiError.value = null
    products.value = await getProducts()
  } catch (e) {
    apiError.value = 'No se pudo cargar. Asegúrate de correr: npx json-server --watch db.json --port 3001'
  } finally {
    isLoadingProducts.value = false
  }
}

const addDemoProduct = async () => {
  isAddingProduct.value = true
  try {
    const demo: Omit<Product, 'id'> = {
      name: 'Módulo de acoplamiento',
      price: 89999,
      stock: 5
    }
    apiError.value = null
    await createProduct(demo)
    await loadProducts()
  } catch (e) {
    apiError.value = 'No se pudo crear. Corre la API local primero.'
  } finally {
    isAddingProduct.value = false
  }
}

// Router
const route = useRoute()

// =====================
// Proyectos (CSV -> json-server)
// =====================
const projects = ref<ProjectRow[]>([])
const isLoadingProjects = ref(false)
const projectsError = ref<string | null>(null)

const loadCsvProjects = async () => {
  isLoadingProjects.value = true
  try {
    projectsError.value = null
    const res = await fetch('http://localhost:3002/projects')
    if (!res.ok) throw new Error('Error al cargar proyectos')
    projects.value = await res.json()
  } catch (e) {
    projectsError.value = 'No se pudo cargar proyectos. Corre: npm run import-csv y luego npm run api'
  } finally {
    isLoadingProjects.value = false
  }
}
</script>

<template>
  <div id="page-top">
    <!-- Navbar ARRIBA -->
    <nav class="navbar navbar-expand-lg navbar-light fixed-top" id="mainNav">
      <div class="container px-4 px-lg-5">
        <a class="navbar-brand" href="#page-top">LaunchLabs</a>
        <button
          class="navbar-toggler navbar-toggler-right"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarResponsive"
          aria-controls="navbarResponsive"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          Menu <i class="fas fa-bars"></i>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><a class="nav-link" href="/">Acerca</a></li>
            <li class="nav-item"><a class="nav-link" href="/projects">Proyectos</a></li>
            <!-- Productos removido -->
            <li class="nav-item"><a class="nav-link" href="#signup">Video</a></li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Vista de rutas (actualmente vacío) -->
    <RouterView />

    <!-- Contenido principal (solo cuando no estamos en /projects) -->
    <div v-if="route.name !== 'projects'">
    <header class="masthead d-flex align-items-center justify-content-center">
  <div class="text-center">
    <h1 class="text-uppercase">Explora el Universo</h1>
    <h2 class="text-white mx-auto mt-2 mb-5">
      Descubre cómo LaunchLabs podría revolucionar el acceso al espacio.
    </h2>
    <a class="btn btn-primary" href="#about">Comenzar</a>
  </div>
</header>

    <!-- Acerca del pryecto en curso -->
    <section class="about-section text-center" id="about">
      <div class="container px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
          <div class="col-lg-8">
            <h2 class="text-white mb-4">¿Qué es el Skyhook?</h2>
            <p class="text-white-50 mb-5">
              El Skyhook es un sistema de transporte espacial revolucionario que podría cambiar para siempre cómo accedemos al espacio. 
              En lugar de usar cohetes tradicionales, utiliza un cable de alta resistencia que se extiende desde la Tierra hasta el espacio.
            </p>
          </div>
        </div>
        
        <!-- Tarjetas -->
        <div class="row gx-4 gx-lg-5 mb-5">
          <div class="col-lg-3 col-md-6 mb-4">
            <div class="stat-card">
              <i class="fas fa-rocket fa-3x text-primary mb-3"></i>
              <h3 class="stat-number">90%</h3>
              <p class="stat-text">Menos combustible requerido</p>
            </div>
          </div>
          <div class="col-lg-3 col-md-6 mb-4">
            <div class="stat-card">
              <i class="fas fa-dollar-sign fa-3x text-success mb-3"></i>
              <h3 class="stat-number">$100B</h3>
              <p class="stat-text">Ahorro estimado anual</p>
            </div>
          </div>
          <div class="col-lg-3 col-md-6 mb-4">
            <div class="stat-card">
              <i class="fas fa-calendar fa-3x text-warning mb-3"></i>
              <h3 class="stat-number">2035</h3>
              <p class="stat-text">Fecha estimada de implementación</p>
            </div>
          </div>
          <div class="col-lg-3 col-md-6 mb-4">
            <div class="stat-card">
              <i class="fas fa-globe fa-3x text-info mb-3"></i>
              <h3 class="stat-number">1000+</h3>
              <p class="stat-text">Lanzamientos diarios posibles</p>
            </div>
          </div>
        </div>

        <!-- Informacion del detalle -->
        <div class="row gx-4 gx-lg-5">
          <div class="col-lg-6 mb-4">
            <div class="feature-card">
              <i class="fas fa-cogs fa-2x text-primary mb-3"></i>
              <h4>¿Cómo funciona?</h4>
              <p class="text-white-50">
                El sistema utiliza un cable de materiales ultra-ligeros y resistentes que se extiende desde una estación espacial 
                hasta la atmósfera terrestre. Las naves se conectan al cable y son aceleradas usando la rotación de la Tierra.
              </p>
            </div>
          </div>
          <div class="col-lg-6 mb-4">
            <div class="feature-card">
              <i class="fas fa-leaf fa-2x text-success mb-3"></i>
              <h4>Beneficios Ambientales</h4>
              <p class="text-white-50">
                Reduce drásticamente las emisiones de carbono al eliminar la necesidad de combustibles químicos tradicionales. 
                Cada lanzamiento con Skyhook equivale a miles de vuelos comerciales en términos de eficiencia energética.
              </p>
            </div>
          </div>
        </div>

        <!-- Hablando de SkyHook -->
        <div class="row gx-4 gx-lg-5 mt-5">
          <div class="col-lg-12">
            <div class="nasa-info-card">
              <div class="row align-items-center">
                <div class="col-md-4">
                  <div class="nasa-logo-container">
                    <i class="fas fa-rocket fa-5x text-primary"></i>
                    <h3 class="text-white mt-3">NASA</h3>
                    <p class="text-white-50">Space Apps Challenge 2025</p>
                  </div>
                </div>
                <div class="col-md-8">
                  <h4 class="text-white">Proyecto NASA Space Apps Challenge 2025</h4>
                  <p class="text-white-50">
                    Este proyecto fue desarrollado para el NASA Space Apps Challenge, demostrando cómo la tecnología 
                    del Skyhook podría revolucionar el acceso al espacio y hacer posible la exploración espacial sostenible.
                  </p>
                  <div class="tags">
                    <span class="tag">Tecnología del espacio</span>
                    <span class="tag">Sostenibilidad</span>
                    <span class="tag">Innovación</span>
                    <span class="tag">Futuro</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Projects -->
    <section class="projects-section bg-light" id="projects">
      <div class="container px-4 px-lg-5">
        <!-- Section Header -->
        <div class="row gx-4 gx-lg-5 justify-content-center text-center mb-5">
          <div class="col-lg-8">
            <h2 class="text-black mb-4">Proyectos Innovadores del Espacio</h2>
            <p class="text-black-50 mb-5">
              Descubre las tecnologías más revolucionarias que están transformando el futuro de la exploración espacial.
            </p>
          </div>
        </div>

        <!-- Skyhook Project -->
        <div class="row gx-4 gx-lg-5 mb-5 align-items-center">
          <div class="col-xl-6 col-lg-7">
            <img class="img-fluid mb-3 mb-lg-0 rounded" src="https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=800&h=600&fit=crop" alt="Skyhook Concept" />
          </div>
          <div class="col-xl-6 col-lg-5">
            <div class="project-card">
              <div class="project-icon">
                <i class="fas fa-anchor fa-2x text-primary"></i>
              </div>
              <h4 class="project-title">Skyhook</h4>
              <p class="project-description">
                Sistema de transporte espacial que utiliza cables de alta resistencia para lanzar naves sin combustibles tradicionales. 
                Reduce costos en 90% y permite lanzamientos diarios masivos.
              </p>
              <div class="project-stats">
                <span class="stat">90% menos combustible</span>
                <span class="stat">$100B ahorro anual</span>
                <span class="stat">2035 implementación</span>
              </div>
              <div class="project-links">
                <a href="#" class="btn btn-outline-primary btn-sm">Ver Detalles</a>
                <a href="#" class="btn btn-outline-secondary btn-sm">Documentación</a>
              </div>
            </div>
          </div>
        </div>

        <!-- Space Elevator Project -->
        <div class="row gx-4 gx-lg-5 mb-5 align-items-center">
          <div class="col-xl-6 col-lg-5 order-lg-2">
            <img class="img-fluid mb-3 mb-lg-0 rounded" src="https://images.unsplash.com/photo-1502134249126-9f3755a50d78?w=800&h=600&fit=crop" alt="Space Elevator" />
          </div>
          <div class="col-xl-6 col-lg-7 order-lg-1">
            <div class="project-card">
              <div class="project-icon">
                <i class="fas fa-elevator fa-2x text-success"></i>
              </div>
              <h4 class="project-title">Space Elevator</h4>
              <p class="project-description">
                Ascensor espacial que conecta la Tierra con una estación orbital usando nanotubos de carbono. 
                Permite transporte de carga y personas a bajo costo y alta frecuencia.
              </p>
              <div class="project-stats">
                <span class="stat">$100/kg vs $10,000/kg</span>
                <span class="stat">24/7 operación</span>
                <span class="stat">2040-2050</span>
              </div>
              <div class="project-links">
                <a href="#" class="btn btn-outline-primary btn-sm">Ver Detalles</a>
                <a href="#" class="btn btn-outline-secondary btn-sm">Investigación</a>
              </div>
            </div>
          </div>
        </div>

        <!-- Mars Colony Project -->
        <div class="row gx-4 gx-lg-5 mb-5 align-items-center">
          <div class="col-xl-6 col-lg-7">
            <img class="img-fluid mb-3 mb-lg-0 rounded" src="https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=800&h=600&fit=crop" alt="Mars Colony" />
          </div>
          <div class="col-xl-6 col-lg-5">
            <div class="project-card">
              <div class="project-icon">
                <i class="fas fa-globe fa-3x text-info mb-3"></i>
              </div>
              <h4 class="project-title">Mars Colony Initiative</h4>
              <p class="project-description">
                Establecimiento de la primera colonia humana permanente en Marte. Incluye hábitats inflables, 
                sistemas de soporte vital y agricultura marciana.
              </p>
              <div class="project-stats">
                <span class="stat">1,000 colonos iniciales</span>
                <span class="stat">2030-2040</span>
                <span class="stat">$500B inversión</span>
              </div>
              <div class="project-links">
                <a href="#" class="btn btn-outline-primary btn-sm">Ver Detalles</a>
                <a href="#" class="btn btn-outline-secondary btn-sm">Aplicar</a>
              </div>
            </div>
          </div>
        </div>

        <!-- Asteroid Mining Project -->
        <div class="row gx-4 gx-lg-5 mb-5 align-items-center">
          <div class="col-xl-6 col-lg-5 order-lg-2">
            <img class="img-fluid mb-3 mb-lg-0 rounded" src="https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=800&h=600&fit=crop" alt="Asteroid Mining" />
          </div>
          <div class="col-xl-6 col-lg-7 order-lg-1">
            <div class="project-card">
              <div class="project-icon">
                <i class="fas fa-gem fa-2x text-warning"></i>
              </div>
              <h4 class="project-title">Asteroid Mining</h4>
              <p class="project-description">
                Extracción de metales preciosos y agua de asteroides cercanos a la Tierra. 
                Proporciona recursos para misiones espaciales y reduce la dependencia terrestre.
              </p>
              <div class="project-stats">
                <span class="stat">$100T en recursos</span>
                <span class="stat">2025-2030</span>
                <span class="stat">Robots autónomos</span>
              </div>
              <div class="project-links">
                <a href="#" class="btn btn-outline-primary btn-sm">Ver Detalles</a>
                <a href="#" class="btn btn-outline-secondary btn-sm">Inversión</a>
              </div>
            </div>
          </div>
        </div>

        <!-- Fusion Drive Project -->
        <div class="row gx-4 gx-lg-5 mb-5 align-items-center">
          <div class="col-xl-6 col-lg-7">
            <img class="img-fluid mb-3 mb-lg-0 rounded" src="https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=800&h=600&fit=crop" alt="Fusion Drive" />
          </div>
          <div class="col-xl-6 col-lg-5">
            <div class="project-card">
              <div class="project-icon">
                <i class="fas fa-bolt fa-2x text-info"></i>
              </div>
              <h4 class="project-title">Fusion Drive</h4>
              <p class="project-description">
                Sistema de propulsión basado en fusión nuclear para viajes interplanetarios rápidos. 
                Reduce el tiempo de viaje a Marte de 6 meses a solo 30 días.
              </p>
              <div class="project-stats">
                <span class="stat">30 días a Marte</span>
                <span class="stat">Energía ilimitada</span>
                <span class="stat">2045-2050</span>
              </div>
              <div class="project-links">
                <a href="#" class="btn btn-outline-primary btn-sm">Ver Detalles</a>
                <a href="#" class="btn btn-outline-secondary btn-sm">Tecnología</a>
              </div>
            </div>
          </div>
        </div>

        <!-- Project Grid -->
        <div class="row gx-4 gx-lg-5 mt-5">
          <div class="col-lg-12 text-center">
            <h3 class="text-black mb-4">Más Proyectos en Desarrollo</h3>
            <div class="row gx-4 gx-lg-5">
              <div class="col-lg-4 col-md-6 mb-4">
                <div class="mini-project-card">
                  <i class="fas fa-satellite fa-2x text-primary mb-3"></i>
                  <h5>Internet Satelital Global</h5>
                  <p>Constelación de satélites para internet de alta velocidad en todo el mundo.</p>
                </div>
              </div>
              <div class="col-lg-4 col-md-6 mb-4">
                <div class="mini-project-card">
                  <i class="fas fa-leaf fa-2x text-success mb-3"></i>
                  <h5>Invernaderos Espaciales</h5>
                  <p>Cultivos en órbita para alimentar misiones espaciales de larga duración.</p>
                </div>
              </div>
              <div class="col-lg-4 col-md-6 mb-4">
                <div class="mini-project-card">
                  <i class="fas fa-shield-alt fa-2x text-warning mb-3"></i>
                  <h5>Defensa Planetaria</h5>
                  <p>Sistemas para detectar y desviar asteroides que amenacen la Tierra.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Skyhook Simulator -->
    <section class="video-section" id="signup">
      <div class="container px-4 px-lg-5">
        
        <!-- Header -->
        <div class="row gx-4 gx-lg-5 justify-content-center text-center mb-5">
          <div class="col-lg-8">
            <i class="fas fa-cogs fa-4x text-primary mb-4"></i>
            <h2 class="text-white mb-4">Simulador Skyhook</h2>
            <p class="text-white-50 mb-5">
              Experimenta cómo funciona el sistema Skyhook en tiempo real
            </p>
          </div>
        </div>

        <!-- Interactive Simulation -->
        <div class="row gx-4 gx-lg-5 mb-5">
          <div class="col-lg-12">
            <div class="simulation-card">
              <div class="simulation-status" :class="isRunning ? 'running' : 'paused'">
                <i :class="isRunning ? 'fas fa-play' : 'fas fa-pause'"></i>
                {{ isRunning ? 'En Ejecución' : 'Pausado' }}
              </div>
              <h3 class="text-white mb-4 text-center">
                <i class="fas fa-rocket me-2"></i>Simulación en Tiempo Real
              </h3>
              <div class="row align-items-center">
                <div class="col-lg-8">
                  <div class="simulation-area">
                    <div class="skyhook-animation" :class="isRunning ? 'running' : 'paused'">
                      <div class="earth"></div>
                      <div class="cable"></div>
                      <div class="spacecraft" :class="missionPhase.toLowerCase().replace(/\s+/g, '')"></div>
                      <div class="orbit"></div>
                      <div class="particle particle-1"></div>
                      <div class="particle particle-2"></div>
                      <div class="particle particle-3"></div>
                      <div class="particle particle-4"></div>
                      <div class="particle particle-5"></div>
                    </div>
                  </div>
                </div>
                <div class="col-lg-4">
                  <div class="simulation-controls">
                    <h5 class="text-white mb-3">Controles de Misión</h5>
                    
                    <!-- Estado de la Misión -->
                    <div class="mission-status mb-3">
                      <div class="status-item">
                        <span class="text-white-50">Fase:</span>
                        <span class="badge" :class="getPhaseClass(missionPhase)">
                          {{ missionPhase }}
                        </span>
                      </div>
                      <div class="status-item">
                        <span class="text-white-50">Tiempo:</span>
                        <span class="text-primary fw-bold">{{ missionTime.toFixed(1) }}s</span>
                      </div>
                    </div>

                    <!-- Controles de Velocidad -->
                    <div class="control-group mb-3">
                      <label class="text-white-50">Velocidad de Simulación:</label>
                      <div class="btn-group w-100" role="group">
                        <button 
                          class="btn btn-sm" 
                          :class="currentSpeed === 0.5 ? 'btn-primary' : 'btn-outline-light'"
                          @click="changeSpeed(0.5)"
                        >
                          0.5x
                        </button>
                        <button 
                          class="btn btn-sm" 
                          :class="currentSpeed === 1 ? 'btn-primary' : 'btn-outline-light'"
                          @click="changeSpeed(1)"
                        >
                          1x
                        </button>
                        <button 
                          class="btn btn-sm" 
                          :class="currentSpeed === 2 ? 'btn-primary' : 'btn-outline-light'"
                          @click="changeSpeed(2)"
                        >
                          2x
                        </button>
                      </div>
                    </div>

                    <!-- Selector de Escenario -->
                    <div class="control-group mb-3">
                      <label class="text-white-50">Tipo de Misión:</label>
                      <select 
                        class="form-select form-select-sm"
                        v-model="currentScenario"
                        @change="changeScenario(currentScenario)"
                        :disabled="isLaunching"
                      >
                        <option value="Lanzamiento básico">Lanzamiento básico (2,000 kg)</option>
                        <option value="Carga pesada">Carga pesada (5,000 kg)</option>
                        <option value="Misión a Marte">Misión a Marte (1,000 kg)</option>
                      </select>
                    </div>

                    <!-- Controles de Misión -->
                    <div class="mission-controls mb-3">
                      <button 
                        class="btn btn-success btn-sm me-2"
                        @click="startLaunch"
                        :disabled="!isRunning || isLaunching"
                      >
                        <i class="fas fa-rocket"></i> Lanzar
                      </button>
                      <button 
                        class="btn btn-warning btn-sm me-2"
                        @click="startDescent"
                        :disabled="missionPhase !== 'Órbita'"
                      >
                        <i class="fas fa-arrow-down"></i> Descender
                      </button>
                      <button 
                        class="btn btn-secondary btn-sm"
                        @click="resetMission"
                      >
                        <i class="fas fa-redo"></i> Reset
                      </button>
                    </div>

                    <!-- Control Principal -->
                    <button 
                      class="btn w-100 mb-3"
                      :class="isRunning ? 'btn-danger' : 'btn-primary'"
                      @click="toggleSimulation"
                    >
                      <i :class="isRunning ? 'fas fa-pause' : 'fas fa-play'"></i> 
                      {{ isRunning ? 'Pausar' : 'Iniciar' }} Simulador
                    </button>
                  </div>
                  <div class="live-stats">
                    <h6 class="text-white mb-2">Telemetría en Vivo</h6>
                    
                    <!-- Datos de Misión -->
                    <div class="stats-section mb-3">
                      <h6 class="text-primary mb-2">Datos de Misión</h6>
                      <div class="stat-item">
                        <span class="text-white-50">Altitud:</span>
                        <span class="text-info fw-bold">{{ altitude.toFixed(1) }} km</span>
                      </div>
                      <div class="stat-item">
                        <span class="text-white-50">Velocidad:</span>
                        <span class="text-warning fw-bold">{{ velocity.toFixed(1) }} km/s</span>
                      </div>
                      <div class="stat-item">
                        <span class="text-white-50">Carga útil:</span>
                        <span class="text-success fw-bold">{{ payload }} kg</span>
                      </div>
                      <div class="stat-item">
                        <span class="text-white-50">Tensión del cable:</span>
                        <span class="text-danger fw-bold">{{ cableTension.toFixed(1) }} kN</span>
                      </div>
                    </div>

                    <!-- Estadísticas Generales -->
                    <div class="stats-section">
                      <h6 class="text-success mb-2">Rendimiento</h6>
                      <div class="stat-item">
                        <span class="text-white-50">Ahorro total:</span>
                        <span class="text-success fw-bold">${{ formatNumber(totalSavings) }}</span>
                      </div>
                      <div class="stat-item">
                        <span class="text-white-50">Lanzamientos:</span>
                        <span class="text-primary fw-bold">{{ launchCount }}</span>
                      </div>
                      <div class="stat-item">
                        <span class="text-white-50">Eficiencia energética:</span>
                        <span class="text-warning fw-bold">{{ energyEfficiency.toFixed(1) }}%</span>
                      </div>
                      <div class="stat-item">
                        <span class="text-white-50">Combustible ahorrado:</span>
                        <span class="text-info fw-bold">{{ fuelSaved.toFixed(1) }}%</span>
                      </div>
                    </div>
                  </div>
                </div>
            </div>
            </div>
          </div>
        </div>

      </div>
    </section>

    

    <!-- Footer Épico -->
    <footer class="epic-footer">
      <!-- Fondo espacial animado -->
      <div class="space-background">
        <div class="star-field">
          <div class="star" v-for="n in 50" :key="n" :style="{ 
            left: Math.random() * 100 + '%', 
            top: Math.random() * 100 + '%',
            animationDelay: Math.random() * 3 + 's',
            animationDuration: (Math.random() * 3 + 2) + 's'
          }"></div>
        </div>
        <div class="nebula"></div>
      </div>
      
      <!-- Contenido del footer -->
      <div class="footer-content">
        <div class="container">
          <div class="row align-items-center">
            <!-- Logo y título -->
            <div class="col-lg-4 text-center mb-4 mb-lg-0">
              <div class="footer-logo">
                <div class="logo-icon">
                  <i class="fas fa-rocket"></i>
                  <div class="logo-glow"></div>
                </div>
                <h4 class="logo-text">LaunchLabs</h4>
                <p class="logo-subtitle">El futuro del espacio</p>
              </div>
            </div>
            
            <!-- Enlaces rápidos -->
            <div class="col-lg-4 text-center mb-4 mb-lg-0">
              <div class="quick-links">
                <h6 class="links-title">Explorar</h6>
                <div class="links-grid">
                  <a href="#about" class="footer-link">
                    <i class="fas fa-info-circle"></i>
                    <span>Acerca</span>
                  </a>
                  <a href="#projects" class="footer-link">
                    <i class="fas fa-project-diagram"></i>
                    <span>Proyectos</span>
                  </a>
                  <a href="#signup" class="footer-link">
                    <i class="fas fa-play"></i>
                    <span>Simulador</span>
                  </a>
                </div>
              </div>
            </div>
            
            <!-- Información del proyecto -->
            <div class="col-lg-4 text-center">
              <div class="project-info">
                <div class="nasa-badge">
                  <i class="fas fa-globe-americas"></i>
                  <span>NASA Space Apps 2025</span>
                </div>
                <div class="team-info">
                  <p class="team-text">Desarrollado por</p>
                  <h5 class="team-name">Mordecai y los Rigbies</h5>
                  
                </div>
              </div>
            </div>
          </div>
          
          <!-- Línea divisoria animada -->
          <div class="footer-divider">
            <div class="divider-line"></div>
            <div class="divider-glow"></div>
          </div>
          
          <!-- Copyright y stats -->
          <div class="row align-items-center">
            <div class="col-md-6 text-center text-md-start">
              <div class="copyright">
                <p>&copy; 2025 LaunchLabs.</p>
              </div>
            </div>
            
          </div>
        </div>
      </div>
      
      <!-- Efectos de partículas flotantes -->
      <div class="floating-particles">
        <div class="particle" v-for="n in 20" :key="'footer-' + n" :style="{
          left: Math.random() * 100 + '%',
          top: Math.random() * 100 + '%',
          animationDelay: Math.random() * 5 + 's',
          animationDuration: (Math.random() * 4 + 6) + 's'
        }"></div>
      </div>
    </footer>
    </div>
  </div>
</template>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Nunito:200,300,400,600,700,800,900");

body, html {
  scroll-behavior: smooth;
  background-color: #000;
}

/* Hero Section - estilos movidos a grayscale.css */

/* About Section */
.about-section {
  background-color: #111;
  padding: 6rem 0;
}

/* Statistics Cards */
.stat-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 2rem 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.stat-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.3);
}

.stat-number {
  font-size: 3rem;
  font-weight: 700;
  color: #fff;
  margin: 0.5rem 0;
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
}

.stat-text {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  margin: 0;
}

/* Feature Cards */
.feature-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 2rem;
  height: 100%;
  transition: all 0.3s ease;
}

.feature-card:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-5px);
}

.feature-card h4 {
  color: #fff;
  margin-bottom: 1rem;
  font-weight: 600;
}

/* NASA Info Card */
.nasa-info-card {
  background: linear-gradient(135deg, rgba(11, 61, 145, 0.3), rgba(0, 0, 0, 0.7));
  border: 2px solid rgba(11, 61, 145, 0.5);
  border-radius: 20px;
  padding: 2rem;
  margin-top: 2rem;
}

.nasa-logo-container {
  text-align: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.nasa-info-card h4 {
  color: #fff;
  margin-bottom: 1rem;
}

/* Tags */
.tags {
  margin-top: 1rem;
}

.tag {
  display: inline-block;
  background: rgba(11, 61, 145, 0.7);
  color: #fff;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.8rem;
  margin: 0.25rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Projects Section */
.projects-section {
  padding: 6rem 0;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

/* Project Cards */
.project-card {
  background: #fff;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  height: 100%;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.project-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
}

.project-icon {
  margin-bottom: 1.5rem;
}

.project-title {
  color: #333;
  font-weight: 700;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.project-description {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.project-stats {
  margin-bottom: 2rem;
}

.project-stats .stat {
  display: inline-block;
  background: linear-gradient(135deg, #0b3d91, #1e5cb8);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.8rem;
  font-weight: 600;
  margin: 0.25rem;
  box-shadow: 0 4px 15px rgba(11, 61, 145, 0.3);
}

.project-links {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.project-links .btn {
  border-radius: 25px;
  padding: 0.5rem 1.5rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.project-links .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* Mini Project Cards */
.mini-project-card {
  background: #fff;
  border-radius: 15px;
  padding: 2rem 1.5rem;
  text-align: center;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
  height: 100%;
}

.mini-project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
}

.mini-project-card h5 {
  color: #333;
  font-weight: 600;
  margin-bottom: 1rem;
}

.mini-project-card p {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0;
}

/* Project Images */
.project-card img {
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.project-card:hover img {
  transform: scale(1.02);
}

/* Skyhook Simulator Section */
.video-section {
  background: linear-gradient(135deg, #0b3d91 0%, #1e5cb8 50%, #2c7be5 100%);
  padding: 6rem 0;
  position: relative;
  overflow: hidden;
}

.video-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="40" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="40" cy="80" r="1" fill="rgba(255,255,255,0.1)"/></svg>');
  animation: float 20s infinite linear;
}

@keyframes float {
  0% { transform: translateY(0px); }
  100% { transform: translateY(-100px); }
}

/* Simulation Card */
.simulation-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.simulation-area {
  background: linear-gradient(135deg, #0f0f23, #1a1a2e, #16213e);
  border-radius: 15px;
  padding: 2rem;
  height: 400px;
  position: relative;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.simulation-area::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
    radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.05) 1px, transparent 1px),
    radial-gradient(circle at 40% 60%, rgba(255, 255, 255, 0.08) 1px, transparent 1px);
  background-size: 50px 50px, 80px 80px, 60px 60px;
  animation: stars-twinkle 10s ease-in-out infinite;
}

@keyframes stars-twinkle {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

.skyhook-animation {
  position: relative;
  width: 100%;
  height: 100%;
}

.earth {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 80px;
  background: linear-gradient(45deg, #4a90e2, #357abd, #2c5aa0);
  border-radius: 50%;
  box-shadow: 
    0 0 20px rgba(74, 144, 226, 0.5),
    inset -10px -10px 20px rgba(0, 0, 0, 0.3),
    inset 10px 10px 20px rgba(255, 255, 255, 0.1);
  animation: earth-rotate 8s linear infinite;
}

.earth::before {
  content: '';
  position: absolute;
  top: 20%;
  left: 30%;
  width: 15px;
  height: 8px;
  background: linear-gradient(45deg, #2d5a2d, #4a7c4a);
  border-radius: 50% 30% 50% 30%;
  opacity: 0.8;
  animation: earth-rotate 8s linear infinite reverse;
}

.earth::after {
  content: '';
  position: absolute;
  top: 60%;
  right: 25%;
  width: 12px;
  height: 6px;
  background: linear-gradient(45deg, #2d5a2d, #4a7c4a);
  border-radius: 40% 60% 40% 60%;
  opacity: 0.7;
  animation: earth-rotate 8s linear infinite reverse;
}

@keyframes earth-rotate {
  0% { transform: translateX(-50%) rotate(0deg); }
  100% { transform: translateX(-50%) rotate(360deg); }
}

.cable {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translateX(-50%);
  width: 4px;
  height: 250px;
  background: linear-gradient(to top, #fff, #ccc, transparent);
  border-radius: 2px;
  animation: cable-sway 3s ease-in-out infinite;
}

@keyframes cable-sway {
  0% { 
    transform: translateX(-50%) rotate(2deg) scaleY(1); 
    opacity: 0.8;
  }
  25% { 
    transform: translateX(-50%) rotate(-1deg) scaleY(1.05); 
    opacity: 1;
  }
  50% { 
    transform: translateX(-50%) rotate(-3deg) scaleY(1.1); 
    opacity: 0.9;
  }
  75% { 
    transform: translateX(-50%) rotate(-1deg) scaleY(1.05); 
    opacity: 1;
  }
  100% { 
    transform: translateX(-50%) rotate(2deg) scaleY(1); 
    opacity: 0.8;
  }
}

.spacecraft {
  position: absolute;
  top: 25%;
  left: 50%;
  transform: translateX(-50%);
  width: 25px;
  height: 18px;
  background: linear-gradient(45deg, #fff, #f0f0f0);
  border-radius: 4px;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
  transition: top 2s ease-in-out;
}

.spacecraft::before {
  content: '';
  position: absolute;
  top: 50%;
  left: -15px;
  transform: translateY(-50%);
  width: 20px;
  height: 3px;
  background: linear-gradient(90deg, transparent, #ff6b6b, #ffa500);
  border-radius: 2px;
  opacity: 0.8;
  animation: engine-flame 0.5s ease-in-out infinite alternate;
}

.spacecraft::after {
  content: '';
  position: absolute;
  top: 50%;
  left: -25px;
  transform: translateY(-50%);
  width: 15px;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(255, 107, 107, 0.6));
  border-radius: 1px;
  opacity: 0.6;
  animation: engine-flame 0.3s ease-in-out infinite alternate;
}

@keyframes engine-flame {
  0% { 
    opacity: 0.6; 
    transform: translateY(-50%) scaleX(1);
  }
  100% { 
    opacity: 1; 
    transform: translateY(-50%) scaleX(1.2);
  }
}


/* Estados de animación */
.skyhook-animation.running .earth,
.skyhook-animation.running .cable,
.skyhook-animation.running .particle {
  animation-play-state: running;
}

.skyhook-animation.paused .earth,
.skyhook-animation.paused .cable,
.skyhook-animation.paused .particle {
  animation-play-state: paused;
}

/* Posiciones del spacecraft según la fase */
.spacecraft.enespera {
  top: 25% !important;
}

.spacecraft.ascenso {
  top: 15% !important;
}

.spacecraft.órbita {
  top: 10% !important;
}

.spacecraft.descenso {
  top: 20% !important;
}

.spacecraft.completado {
  top: 25% !important;
}

.orbit {
  position: absolute;
  top: 15%;
  left: 50%;
  transform: translateX(-50%);
  width: 180px;
  height: 180px;
  border: 2px dashed rgba(255, 255, 255, 0.4);
  border-radius: 50%;
  animation: orbit-pulse 4s ease-in-out infinite;
}

@keyframes orbit-pulse {
  0%, 100% { 
    border-color: rgba(255, 255, 255, 0.4);
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
  }
  50% { 
    border-color: rgba(74, 144, 226, 0.6);
    box-shadow: 0 0 20px rgba(74, 144, 226, 0.4);
  }
}

/* Partículas flotantes */
.particle {
  position: absolute;
  width: 2px;
  height: 2px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  animation: particle-float 8s ease-in-out infinite;
}

.particle-1 {
  top: 20%;
  left: 20%;
  animation-delay: 0s;
  animation-duration: 6s;
}

.particle-2 {
  top: 30%;
  right: 15%;
  animation-delay: 1s;
  animation-duration: 7s;
}

.particle-3 {
  top: 60%;
  left: 10%;
  animation-delay: 2s;
  animation-duration: 5s;
}

.particle-4 {
  top: 40%;
  right: 25%;
  animation-delay: 3s;
  animation-duration: 8s;
}

.particle-5 {
  top: 70%;
  right: 30%;
  animation-delay: 4s;
  animation-duration: 6s;
}

@keyframes particle-float {
  0%, 100% { 
    transform: translateY(0px) translateX(0px);
    opacity: 0.3;
  }
  25% { 
    transform: translateY(-10px) translateX(5px);
    opacity: 1;
  }
  50% { 
    transform: translateY(-5px) translateX(-5px);
    opacity: 0.7;
  }
  75% { 
    transform: translateY(-15px) translateX(3px);
    opacity: 0.9;
  }
}

.simulation-controls {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 1rem;
}

.control-group {
  margin-bottom: 1rem;
}

.live-stats {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.stat-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(5px);
}

.stats-section {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.mission-status {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 1rem;
}

.mission-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.mission-controls .btn {
  flex: 1;
  min-width: 80px;
}

/* Indicador de estado de simulación */
.simulation-status {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.simulation-status.running {
  background: rgba(40, 167, 69, 0.2);
  color: #28a745;
  border: 1px solid rgba(40, 167, 69, 0.3);
}

.simulation-status.paused {
  background: rgba(220, 53, 69, 0.2);
  color: #dc3545;
  border: 1px solid rgba(220, 53, 69, 0.3);
}

/* Products section */
.products-section {
  background: linear-gradient(135deg, #0f0f23, #1a1a2e 60%, #16213e);
  padding: 4rem 0 6rem;
}

.products-card {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

/* Animación de pulso para estadísticas */
.stat-item span:last-child {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}


/* Navbar */
.navbar {
  transition: background-color 0.3s;
}

.navbar.scrolled {
  background-color: rgba(0, 0, 0, 0.85);
}

/* ===== FOOTER ÉPICO ===== */
.epic-footer {
  position: relative;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  min-height: 400px;
  overflow: hidden;
  border-top: 2px solid rgba(11, 61, 145, 0.3);
}

/* Fondo espacial */
.space-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.star-field {
  position: absolute;
  width: 100%;
  height: 100%;
}

.star {
  position: absolute;
  width: 2px;
  height: 2px;
  background: #fff;
  border-radius: 50%;
  animation: star-twinkle infinite ease-in-out;
}

@keyframes star-twinkle {
  0%, 100% { 
    opacity: 0.3; 
    transform: scale(1);
  }
  50% { 
    opacity: 1; 
    transform: scale(1.5);
  }
}

.nebula {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(ellipse at 20% 30%, rgba(11, 61, 145, 0.3) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 70%, rgba(44, 123, 229, 0.2) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%, rgba(30, 92, 184, 0.1) 0%, transparent 70%);
  animation: nebula-drift 20s ease-in-out infinite;
}

@keyframes nebula-drift {
  0%, 100% { transform: translateX(0px) translateY(0px); }
  33% { transform: translateX(10px) translateY(-5px); }
  66% { transform: translateX(-5px) translateY(10px); }
}

/* Contenido del footer */
.footer-content {
  position: relative;
  z-index: 2;
  padding: 4rem 0 2rem;
}

/* Logo del footer */
.footer-logo {
  text-align: center;
}

.logo-icon {
  position: relative;
  display: inline-block;
  margin-bottom: 1rem;
}

.logo-icon i {
  font-size: 3rem;
  color: #0b3d91;
  animation: logo-pulse 3s ease-in-out infinite;
}

.logo-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  background: radial-gradient(circle, rgba(11, 61, 145, 0.3) 0%, transparent 70%);
  border-radius: 50%;
  animation: logo-glow-pulse 3s ease-in-out infinite;
}

@keyframes logo-pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

@keyframes logo-glow-pulse {
  0%, 100% { 
    opacity: 0.5; 
    transform: translate(-50%, -50%) scale(1);
  }
  50% { 
    opacity: 1; 
    transform: translate(-50%, -50%) scale(1.2);
  }
}

.logo-text {
  color: #fff;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 20px rgba(11, 61, 145, 0.5);
}

.logo-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin: 0;
}

/* Enlaces rápidos */
.quick-links {
  text-align: center;
}

.links-title {
  color: #fff;
  font-weight: 600;
  margin-bottom: 1.5rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.links-grid {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.footer-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease;
  padding: 1rem;
  border-radius: 10px;
  position: relative;
  overflow: hidden;
}

.footer-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(11, 61, 145, 0.3), transparent);
  transition: left 0.5s ease;
}

.footer-link:hover::before {
  left: 100%;
}

.footer-link:hover {
  color: #0b3d91;
  transform: translateY(-5px);
  background: rgba(11, 61, 145, 0.1);
}

.footer-link i {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.footer-link span {
  font-size: 0.8rem;
  font-weight: 500;
}

/* Información del proyecto */
.project-info {
  text-align: center;
}

.nasa-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, rgba(11, 61, 145, 0.3), rgba(44, 123, 229, 0.2));
  border: 1px solid rgba(11, 61, 145, 0.5);
  border-radius: 25px;
  padding: 0.5rem 1rem;
  margin-bottom: 1.5rem;
  color: #fff;
  font-weight: 600;
  animation: badge-glow 4s ease-in-out infinite;
}

@keyframes badge-glow {
  0%, 100% { 
    box-shadow: 0 0 10px rgba(11, 61, 145, 0.3);
  }
  50% { 
    box-shadow: 0 0 20px rgba(11, 61, 145, 0.6);
  }
}

.team-info {
  color: rgba(255, 255, 255, 0.8);
}

.team-text {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  color: rgba(255, 255, 255, 0.6);
}

.team-name {
  color: #fff;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 15px rgba(11, 61, 145, 0.5);
}

/* Línea divisoria */
.footer-divider {
  position: relative;
  margin: 3rem 0 2rem;
  height: 2px;
}

.divider-line {
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(11, 61, 145, 0.5), transparent);
}

.divider-glow {
  position: absolute;
  top: -1px;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, transparent, rgba(11, 61, 145, 0.3), transparent);
  animation: divider-scan 3s ease-in-out infinite;
}

@keyframes divider-scan {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

/* Copyright y estadísticas */
.copyright {
  color: rgba(255, 255, 255, 0.7);
}

.copyright p {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.mission-text {
  font-style: italic;
  color: rgba(11, 61, 145, 0.8);
}

.footer-stats {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  border: 1px solid rgba(11, 61, 145, 0.2);
  transition: all 0.3s ease;
  min-width: 80px;
}

.stat-item:hover {
  background: rgba(11, 61, 145, 0.1);
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(11, 61, 145, 0.3);
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #0b3d91;
  text-shadow: 0 0 10px rgba(11, 61, 145, 0.5);
}

.stat-label {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Partículas flotantes */
.floating-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
  pointer-events: none;
}

.floating-particles .particle {
  position: absolute;
  width: 1px;
  height: 1px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  animation: particle-drift infinite linear;
}

@keyframes particle-drift {
  0% { 
    transform: translateY(100vh) translateX(0px);
    opacity: 0;
  }
  10% { 
    opacity: 1;
  }
  90% { 
    opacity: 1;
  }
  100% { 
    transform: translateY(-100px) translateX(50px);
    opacity: 0;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .footer-content {
    padding: 2rem 0 1rem;
  }
  
  .links-grid {
    gap: 1rem;
  }
  
  .footer-stats {
    gap: 1rem;
  }
  
  .stat-item {
    min-width: 60px;
    padding: 0.5rem;
  }
  
  .stat-number {
    font-size: 1.2rem;
  }
}
</style>
