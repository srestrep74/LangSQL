<script setup lang="ts">
import { ref, onMounted } from 'vue';
import AlertService from '../services/AlertService';
import { useRouter } from 'vue-router';

const router = useRouter();

const goToCreateAlert = () => {
  router.push({ name: 'create_alert' });
};

const alerts = ref<Array<any>>([]);
const isLoading = ref(true);
const errorMessage = ref('');

const fetchAlerts = async () => {
  isLoading.value = true;
  try {
    const data = await AlertService.getAlerts();
    alerts.value = data?.data || [];
    if (alerts.value.length === 0) {
      errorMessage.value = 'No alerts found.';
    } else {
      errorMessage.value = '';
    }
  } catch (error: any) {
    errorMessage.value = error.message || 'Failed to load alerts';
  } finally {
    isLoading.value = false;
  }
};

const deleteAlert = async (alertId: number) => {
  if (confirm('Are you sure you want to delete this alert?')) {
    try {
      await AlertService.deleteAlert(alertId.toString());
      alerts.value = alerts.value.filter((alert) => alert.id !== alertId);
      alert('Alert deleted successfully!');
    } catch (error: any) {
      alert(error.message || 'Failed to delete alert');
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
      <h2 class="fw-bold fs-3 text-custom-purple brand-text">Your Alerts</h2>
      <button @click="goToCreateAlert" class="btn btn-primary custom-btn">
          + Create Alert
      </button>
    </div>

    <div v-if="isLoading" class="alert alert-info text-center" role="alert">
      Loading alerts...
    </div>

    <div v-else-if="errorMessage" class="alert alert-danger text-center" role="alert">
      {{ errorMessage }}
    </div>

    <div v-else-if="alerts.length === 0" class="alert alert-warning text-center" role="alert">
      No alerts found.
    </div>

    <div v-else class="table-responsive">
      <table class="table table-hover table-bordered align-middle">
        <thead class="table-dark">
          <tr>
            <th scope="col">Condition</th>
            <th scope="col">Sent</th>
            <th scope="col">Created At</th>
            <th scope="col">Expires At</th>
            <th scope="col">Options</th>
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

<script lang="ts">
function formatDate(dateStr: string) {
  const date = new Date(dateStr);
  return date.toLocaleString();
}
</script>

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
