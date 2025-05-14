<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute, useRouter } from 'vue-router';
import AlertService from '../services/AlertService';

const route = useRoute();
const router = useRouter();

const { t, locale } = useI18n();
const alertId = route.params.id as string;
const alert = ref<any | null>(null);
const isLoading = ref(true);
const errorMessage = ref('');

const fetchAlert = async () => {
  isLoading.value = true;
  try {
    const response = await AlertService.getAlert(alertId);
    alert.value = response?.data;
  } catch (error: any) {
    errorMessage.value = error.message || t('message.alerts.errorMessage');
  } finally {
    isLoading.value = false;
  }
};

function formatDate(dateStr: string) {
  const isoStr = dateStr.endsWith('Z') ? dateStr : dateStr + 'Z';
  const date = new Date(isoStr);

  return new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/Bogota',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  }).format(date);
}

onMounted(() => {
  fetchAlert();
});
</script>

<template>
  <div class="container my-5">
    <button class="btn btn-secondary mb-3" @click="router.back()">{{ t('message.alerts.backButton') }}</button>

    <div v-if="isLoading" class="alert alert-info text-center" role="alert">
      {{ t('message.alerts.loadingMessage') }}
    </div>

    <div v-else-if="errorMessage" class="alert alert-danger text-center" role="alert">
      {{ errorMessage }}
    </div>

    <div v-else-if="alert" class="card shadow">
      <div class="card-body">
        <h2 class="card-title fw-bold text-custom-purple">{{ t('message.alerts.alertDetails') }}</h2>
        <hr />
        <dl class="row">
          <dt class="col-sm-4">{{ t('message.alerts.alertPrompt') }}</dt>
          <dd class="col-sm-8">{{ alert.prompt }}</dd>

          <dt class="col-sm-4">{{ t('message.alerts.alertStatus') }}</dt>
          <dd class="col-sm-8">
            <i
              v-if="alert.sent"
              class="bi bi-check-circle-fill text-success"
              title="Sent"
            ></i>
            <i
              v-else
              class="bi bi-x-circle-fill text-danger"
              title="Not Sent"
            ></i>
          </dd>

          <dt class="col-sm-4">{{ t('message.alerts.alertCreation') }}</dt>
          <dd class="col-sm-8">{{ formatDate(alert.creation_date) }}</dd>

          <dt class="col-sm-4">{{ t('message.alerts.alertExpiration') }}</dt>
          <dd class="col-sm-8">{{ formatDate(alert.expiration_date) }}</dd>

          <dt class="col-sm-4">{{ t('message.alerts.alertQuery') }}</dt>
          <dd class="col-sm-8">
            <pre class="bg-light p-2 rounded" v-if="alert.sql_query">{{ alert.sql_query }}</pre>
            <span v-else class="text-muted">{{ t('message.alerts.alertNoQuery') }}</span>
          </dd>

          <dt class="col-sm-4">{{ t('message.alerts.alertEmails') }}</dt>
          <dd class="col-sm-8">
            <ul class="mb-0">
              <li v-for="(email, idx) in alert.notification_emails" :key="idx">
                {{ email }}
              </li>
            </ul>
          </dd>
        </dl>
      </div>
    </div>
  </div>
</template>

<style scoped>
.text-custom-purple {
  color: #800080;
}
</style>
