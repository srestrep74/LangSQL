import { createI18n } from 'vue-i18n'

// Type-define message resources
type MessageSchema = {
  message: {
    database: {
      credentialsMissing: string
    }
    query: {
      processing: string
      error: string
      results: string
    }
    ui: {
      placeholder: string
      send: string
    }
  }
}

// Load modularized translations
function loadLocaleMessages() {
  const locales = import.meta.glob('./locales/*.json', { eager: true })
  const messages: Record<string, any> = {}
  
  for (const path in locales) {
    const matched = path.match(/\/([a-z0-9]+)\.json$/i)
    if (matched && matched[1]) {
      const locale = matched[1]
      messages[locale] = (locales[path] as any).default || locales[path]
    }
  }
  
  return messages
}

const i18n = createI18n<[MessageSchema], 'en' | 'es'>({
  legacy: false,
  locale: 'en', // default language
  fallbackLocale: 'en',
  messages: loadLocaleMessages()
})

export default i18n