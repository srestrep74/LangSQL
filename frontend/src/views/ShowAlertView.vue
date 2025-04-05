<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import AlertService from '../services/AlertService';

const route = useRoute();
const router = useRouter();

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
    errorMessage.value = error.message || 'Failed to load alert';
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchAlert();
});
</script>

<template>
  <div class="container my-5">
    <button class="btn btn-secondary mb-3" @click="router.back()">← Back</button>

    <div v-if="isLoading" class="alert alert-info text-center" role="alert">
      Loading alert details...
    </div>

    <div v-else-if="errorMessage" class="alert alert-danger text-center" role="alert">
      {{ errorMessage }}
    </div>

    <div v-else-if="alert" class="card shadow">
      <div class="card-body">
        <h2 class="card-title fw-bold text-custom-purple">Alert Details</h2>
        <hr />
        <dl class="row">
          <dt class="col-sm-4">Prompt</dt>
          <dd class="col-sm-8">{{ alert.prompt }}</dd>

          <dt class="col-sm-4">Sent</dt>
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

          <dt class="col-sm-4">Created At</dt>
          <dd class="col-sm-8">{{ formatDate(alert.creation_date) }}</dd>

          <dt class="col-sm-4">Expires At</dt>
          <dd class="col-sm-8">{{ formatDate(alert.expiration_date) }}</dd>

          <dt class="col-sm-4">SQL Query</dt>
          <dd class="col-sm-8">
            <pre class="bg-light p-2 rounded" v-if="alert.sql_query">{{ alert.sql_query }}</pre>
            <span v-else class="text-muted">No query provided.</span>
          </dd>

          <dt class="col-sm-4">User</dt>
          <dd class="col-sm-8">{{ alert.user }}</dd>

          <dt class="col-sm-4">Notification Emails</dt>
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

<script lang="ts">
function formatDate(dateStr: string) {
  const date = new Date(dateStr);
  return date.toLocaleString();
}
</script>

<style scoped>
.text-custom-purple {
  color: #800080;
}
</style>
