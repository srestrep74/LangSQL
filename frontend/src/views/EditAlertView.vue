<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute, useRouter } from 'vue-router';
import AlertService from '../services/AlertService';

const router = useRouter();
const route = useRoute();
const { t, locale } = useI18n();
const alertId = route.params.id as string;

const formData = ref({
  prompt: '',
  notification_emails: [] as string[],
  expiration_date: '',
});

const isLoading = ref(true);
const isSubmitting = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const fetchAlert = async () => {
  try {
    const response = await AlertService.getAlert(alertId);
    const alert = response.data;

    formData.value.prompt = alert.prompt;
    formData.value.notification_emails = alert.notification_emails;
    formData.value.expiration_date = alert.expiration_date.slice(0, 16);
  } catch (error: any) {
    errorMessage.value = error.message || t('message.alerts.updateError');
  } finally {
    isLoading.value = false;
  }
};

const updateAlert = async () => {
  isSubmitting.value = true;
  successMessage.value = '';
  errorMessage.value = '';
  try {
    await AlertService.editAlert(alertId, formData.value);
    successMessage.value = t('message.alerts.updateSuccess');
  } catch (error: any) {
    errorMessage.value = error.message || t('message.alerts.updateError');
  } finally {
    isSubmitting.value = false;
  }
};

const goToAlerts = () => {
  router.push({ name: 'alerts' });
};

onMounted(() => {
  fetchAlert();
});
</script>

<template>
  <div class="container my-5">
    <button class="btn btn-secondary mb-3" @click="goToAlerts()">← {{ t('message.alerts.backButton') }}</button>

    <h2 class="fw-bold text-custom-purple mb-4">{{ t('message.alerts.editAlert') }}</h2>

    <div v-if="isLoading" class="alert alert-info text-center">{{ t('message.alerts.loadingAlert') }}</div>
    <div v-else>
      <form @submit.prevent="updateAlert" class="card p-4 shadow">
        <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
        <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

        <div class="mb-3">
          <label for="prompt" class="form-label">{{ t('message.alerts.alertPrompt') }}</label>
          <input
            v-model="formData.prompt"
            type="text"
            id="prompt"
            class="form-control"
            required
          />
        </div>

        <div class="mb-3">
          <label for="emails" class="form-label">{{ t('message.alerts.emailLabel') }}</label>
          <input
            v-model="formData.notification_emails"
            type="text"
            id="emails"
            class="form-control"
            @blur="formData.notification_emails = formData.notification_emails.join(',').split(',').map(e => e.trim())"
          />
        </div>

        <div class="mb-3">
          <label for="expiration" class="form-label">{{ t('message.alerts.alertExpiration') }}</label>
          <input
            v-model="formData.expiration_date"
            type="datetime-local"
            id="expiration"
            class="form-control"
            required
          />
        </div>

        <button class="btn btn-primary custom-btn" :disabled="isSubmitting">
          {{ isSubmitting ? t('message.alerts.updating') : t('message.alerts.updateAlertButton') }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.text-custom-purple {
  color: #800080;
}
.custom-btn {
  background-color: #800080 !important;
  border-color: #800080 !important;
}
.custom-btn:hover {
  background-color: #6a006a !important;
  border-color: #6a006a !important;
}
</style>
