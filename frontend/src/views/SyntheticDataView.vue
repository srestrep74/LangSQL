<script setup lang="ts">
import { ref } from 'vue';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import SyntheticDataService from '../services/SyntheticDataService';

const router = useRouter();

const databaseSchema = ref<string | null>(null);
const dataAmount = ref(40);
const errorMessage = ref('');
const toastMessage = ref('');
const toastType = ref<'info' | 'success' | 'danger'>('info');
const showToast = ref(false);

const validateInput = () => {
  if (dataAmount.value < 40 || dataAmount.value > 400) {
    errorMessage.value = 'The value must be between 40 and 400.';
    dataAmount.value = Math.max(40, Math.min(400, dataAmount.value));
  } else if (dataAmount.value % 40 !== 0) {
    errorMessage.value = 'The value must be a multiple of 40.';
    dataAmount.value = Math.round(dataAmount.value / 40) * 40;
  } else {
    errorMessage.value = '';
  }
};

const triggerToast = (message: string, type: 'info' | 'success' | 'danger') => {
  toastMessage.value = message;
  toastType.value = type;
  showToast.value = true;

  setTimeout(() => {
    showToast.value = false;
  }, 4000);
};

const generateData = async () => {
  validateInput();
  if (errorMessage.value) return;

  triggerToast('⏳ Data is being generated. You will be notified shortly.', 'info');

  try {
    const response = await SyntheticDataService.postSyntheticData(dataAmount.value);

    if (response.status === "success") {
      triggerToast("✅ Data generation request successful! Redirecting...", 'success');
      setTimeout(() => {
        router.push('/');
      }, 2000);
    } else {
      throw new Error(response.message);
    }
  } catch (error) {
    console.error("Failed to generate data:", error);
    triggerToast("❌ An error occurred while generating data. Please try again.", 'danger');
  }
};

onMounted(async () => {
  try {
    const schema = await SyntheticDataService.getDatabaseSchema();
    databaseSchema.value = JSON.stringify(schema, null, 2);
  } catch (error) {
    triggerToast('❌ Failed to load database schema.', 'danger');
    console.error(error);
  }
});
</script>

<template>
  <div class="synthetic-data-view">
    <div v-if="showToast" :class="['toast-message', toastType]">
      <p>{{ toastMessage }}</p>
    </div>

    <div class="description">
      <h2 class="text-custom-purple">Synthetic Data Generation</h2>
      <p>
        This tool allows you to generate synthetic data based on your database schema.
        Enter the number of records you want to generate (in multiples of 40, up to 400) and click the button below.
      </p>
    </div>

    <div class="schema-section">
      <h3 class="text-custom-purple">Database Schema</h3>
      <div class="schema-display">
        <pre v-if="databaseSchema">{{ databaseSchema }}</pre>
        <p v-else class="text-muted">Loading Schema...</p>
      </div>
    </div>

    <div class="input-section">
      <label for="data-amount" class="text-custom-purple">Number of records to generate:</label>
      <input
        type="number"
        id="data-amount"
        v-model.number="dataAmount"
        min="40"
        max="400"
        step="40"
        class="form-control"
        @input="validateInput"
      />
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>

    <div class="button-section">
      <button @click="generateData" class="btn btn-custom-purple">Generate Data</button>
    </div>
  </div>
</template>

<style scoped>
.synthetic-data-view {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  position: relative;
}

.description {
  margin-bottom: 20px;
}

.schema-section {
  margin-bottom: 20px;
}

.schema-display {
  background-color: #f4f4f4;
  padding: 10px;
  border-radius: 5px;
  font-family: monospace;
}

.input-section {
  margin-bottom: 20px;
}

.input-section input {
  margin-top: 10px;
}

.error-message {
  color: red;
  font-size: 0.9em;
  margin-top: 5px;
}

.button-section {
  text-align: center;
}

.btn-custom-purple {
  background-color: #7b0779;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease-in-out;
}

.btn-custom-purple:hover {
  background-color: #5a0558;
}

.toast-message {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #7b0779;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  animation: fadeIn 0.5s ease-in-out;
}

.toast-message {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  border-radius: 5px;
  color: white;
  font-weight: 500;
  z-index: 1000;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  animation: fadeIn 0.4s ease-in-out;
}

.toast-message.info {
  background-color: #6c757d;
}

.toast-message.success {
  background-color: #198754;
}

.toast-message.danger {
  background-color: #dc3545;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}
</style>
