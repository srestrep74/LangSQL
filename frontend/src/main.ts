import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import i18n from './i18n'
import router from './router'

const savedLang = localStorage.getItem('userLanguage')
if (savedLang) {
  i18n.global.locale.value = savedLang as 'en' | 'es'
}

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)

app.mount('#app')
