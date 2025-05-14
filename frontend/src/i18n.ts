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
      yourChats: string
      newChat: string
      noChats: string
      loadingHistory: string
      startConversation: string
      confirmDelete: string
      deleteConfirmation: string
      deleteWarning: string
      cancel: string
      delete: string
      errorLoadingChat: string
      unknownError: string
      errorLoadingHistory: string
      errorDeletingChat: string
      errorRenamingChat: string
      queryResults: string
      dataFrom: string
      selectedFields: string
      noResultsFound: string
      errorDisplayingResults: string
      null: string
      true: string
      false: string
      rowReturned: {
        one: string
        other: string
      }
      enterTitle: string
      chatPrefix: string
      noMessages: string
    }
    alerts: {
      errorMessage: string
      loadingMessage: string
      backButton: string
      alertDetails: string
      alertPrompt: string
      alertStatus: string
      alertCreation: string
      alertExpiration: string
      alertQuery: string
      alertEmails: string
      alertNoQuery: string
      noAlertsFound: string
      loadingAlerts: string
      deleteConfirmation: string
      deleteSuccess: string
      deleteError: string
      deletePrompt: string
      alertSent: string
      alertNotSent: string
      condition: string
      options: string
      showAlert: string
      createAlert: string
      title: string
      createTitle: string
      generating: string
      createSuccess: string
      createError: string
      notificationEmails: string
      notificationEmailsTooltip: string
      conditionTooltip: string
      expirationDate: string
      expirationDateTooltip: string
      submit: string
      editAlert: string
      loadingAlert: string
      updateSuccess: string
      updateError: string
      emailLabel: string
      updating: string
      updateAlertButton: string
    }
    syntheticData: {
      errorMessage1: string
      errorMessage2: string
      waitingMessage: string
      successMessage: string
      errorMessage3: string
      errorMessage4: string
      title: string
      description: string
      databaseSchema: string
      loadingSchema: string
      numberOfRecords: string
      generateData: string
    }
  }
}

// Load modularized translations
function loadLocaleMessages() {
  const locales = import.meta.glob('./locales/*.json', { eager: true })
  const messages: { [key: string]: any } = {}

  for (const path in locales) {
    const matched = path.match(/\/([a-z0-9]+)\.json$/i)
    if (matched && matched[1]) {
      const locale = matched[1]
      messages[locale] = (locales[path] as any).default || locales[path]
    }
  }

  return messages
}

const i18n = createI18n({
  legacy: false,
  locale: 'en', // default language
  fallbackLocale: 'en',
  messages: loadLocaleMessages()
})

export default i18n
