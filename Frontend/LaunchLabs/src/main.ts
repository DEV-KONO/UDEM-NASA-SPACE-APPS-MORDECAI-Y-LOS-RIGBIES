import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Bootstrap y Font Awesome se cargan desde CDN en index.html

import '@/grayscale.css'

const app = createApp(App)
app.use(router)
app.mount('#app')
