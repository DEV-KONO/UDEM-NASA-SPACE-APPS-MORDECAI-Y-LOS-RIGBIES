<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getProducts, createProduct, type Product } from '@/api/products'

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
    apiError.value = 'No se pudo cargar. Corre: npx json-server --watch db.json --port 3001'
  } finally {
    isLoadingProducts.value = false
  }
}

const addDemoProduct = async () => {
  isAddingProduct.value = true
  try {
    const demo: Omit<Product, 'id'> = { name: 'Módulo de acoplamiento', price: 89999, stock: 5 }
    await createProduct(demo)
    await loadProducts()
  } catch (e) {
    apiError.value = 'No se pudo crear. Corre la API primero.'
  } finally {
    isAddingProduct.value = false
  }
}

onMounted(loadProducts)
</script>

<template>
  <section class="products-section">
    <div class="container px-4 px-lg-5">
      <div class="row gx-4 gx-lg-5 justify-content-center text-center mb-4">
        <div class="col-lg-8">
          <h2 class="text-white mb-2">Productos</h2>
          <p class="text-white-50">Página dedicada (JSON Server)</p>
        </div>
      </div>

      <div class="row gx-4 gx-lg-5 justify-content-center">
        <div class="col-lg-10">
          <div class="products-card">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <span class="text-white-50">{{ isLoadingProducts ? 'Cargando...' : products.length + ' productos' }}</span>
              <button class="btn btn-sm btn-primary" :disabled="isAddingProduct" @click="addDemoProduct">
                <i class="fas fa-plus"></i> Agregar demo
              </button>
            </div>
            <div class="table-responsive">
              <table class="table table-dark table-striped table-hover align-middle mb-0">
                <thead>
                  <tr>
                    <th class="text-white-50">ID</th>
                    <th class="text-white-50">Nombre</th>
                    <th class="text-white-50">Precio</th>
                    <th class="text-white-50">Stock</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="apiError">
                    <td colspan="4" class="text-center text-danger">{{ apiError }}</td>
                  </tr>
                  <tr v-if="isLoadingProducts">
                    <td colspan="4" class="text-center text-white-50">Cargando...</td>
                  </tr>
                  <tr v-for="p in products" :key="p.id">
                    <td class="text-white-50">{{ p.id }}</td>
                    <td class="text-white">{{ p.name }}</td>
                    <td class="text-success fw-bold">${{ p.price.toLocaleString() }}</td>
                    <td class="text-info">{{ p.stock }}</td>
                  </tr>
                  <tr v-if="!isLoadingProducts && !apiError && products.length === 0">
                    <td colspan="4" class="text-center text-white-50">Sin productos. Agrega uno de demo.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.products-section {
  background: linear-gradient(135deg, #0f0f23, #1a1a2e 60%, #16213e);
  padding: 6rem 0;
}

.products-card {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}
</style>


