<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import AlertService from '../services/AlertService';
import { useRouter } from 'vue-router';

const router = useRouter();

const goToCreateAlert = () => {
  router.push({ name: 'create_alert' });
};

const alerts = ref<Array<any>>([]);
const { t, locale } = useI18n();
const isLoading = ref(true);
const errorMessage = ref('');

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

const fetchAlerts = async () => {
  isLoading.value = true;
  try {
    const data = await AlertService.getAlerts();
    alerts.value = data?.data || [];
    if (alerts.value.length === 0) {
      errorMessage.value = t('message.alerts.noAlertsFound');
    } else {
      errorMessage.value = '';
    }
  } catch (error: any) {
    errorMessage.value = error.message || t('message.alerts.noAlertsLoaded');
  } finally {
    isLoading.value = false;
  }
};

const deleteAlert = async (alertId: number) => {
  if (confirm(t('message.alerts.deleteConfirmation'))) {
    try {
      await AlertService.deleteAlert(alertId.toString());
      alerts.value = alerts.value.filter((alert) => alert.id !== alertId);
      alert(t('message.alerts.deleteSuccess'));
    } catch (error: any) {
      alert(error.message || t('message.alerts.deleteError'));
    }
  }
};

const getAlert = (alertId: number) => {
  router.push({ name: 'alert_details', params: { id: alertId } });
};

const updateAlert = (alertId: number) => {
  router.push({ name: 'alert_edit', params: { id: alertId } });
};

onMounted(() => {
  fetchAlerts();
});
</script>

<template>
  <div class="container my-5">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="fw-bold fs-3 text-custom-purple brand-text">{{ t('message.alerts.title') }}</h2>
      <button @click="goToCreateAlert" class="btn btn-primary custom-btn">
          + {{ t('message.alerts.createAlert') }}
      </button>
    </div>

    <div v-if="isLoading" class="alert alert-info text-center" role="alert">
      {{ t('message.alerts.loadingAlerts') }}
    </div>

    <div v-else-if="errorMessage" class="alert alert-danger text-center" role="alert">
      {{ errorMessage }}
    </div>

    <div v-else-if="alerts.length === 0" class="alert alert-warning text-center" role="alert">
      {{ t('message.alerts.noAlertsFound') }}
    </div>

    <div v-else class="table-responsive">
      <table class="table table-hover table-bordered align-middle">
        <thead class="table-dark">
          <tr>
            <th scope="col">{{ t('message.alerts.condition') }}</th>
            <th scope="col">{{ t('message.alerts.alertStatus') }}</th>
            <th scope="col">{{ t('message.alerts.alertCreation') }}</th>
            <th scope="col">{{ t('message.alerts.alertExpiration') }}</th>
            <th scope="col">{{ t('message.alerts.options') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="alert in alerts" :key="alert.id">
            <td>{{ alert.prompt }}</td>
            <td class="text-center">
              <i v-if="alert.sent" class="bi bi-check-circle-fill text-success" title="Sent"></i>
              <i v-else class="bi bi-x-circle-fill text-danger" title="Not Sent"></i>
            </td>
            <td>{{ formatDate(alert.creation_date) }}</td>
            <td>{{ formatDate(alert.expiration_date) }}</td>
            <td>
              <button class="btn btn-outline-danger me-2" @click="deleteAlert(alert.id)" title="Delete Alert">
                  <i class="bi bi-trash"></i>
              </button>
              <button class="btn btn-outline-primary me-2" @click="updateAlert(alert.id)" title="Edit Alert">
                  <i class="bi bi-pencil"></i>
              </button>
              <button class="btn btn-outline-secondary me-2" @click="getAlert(alert.id)" title="Show Alert">
                  <i class="bi bi-eye"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.table {
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  vertical-align: middle !important;
}

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
