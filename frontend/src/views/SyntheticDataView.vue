<script setup lang="ts">
import { ref } from 'vue';
import { onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import SyntheticDataService from '../services/SyntheticDataService';

const router = useRouter();

const databaseSchema = ref<string | null>(null);
const { t, locale } = useI18n();
const dataAmount = ref(40);
const errorMessage = ref('');
const toastMessage = ref('');
const toastType = ref<'info' | 'success' | 'danger'>('info');
const showToast = ref(false);

const validateInput = () => {
  if (dataAmount.value < 40 || dataAmount.value > 400) {
    errorMessage.value = t('message.syntheticData.errorMessage1');
    dataAmount.value = Math.max(40, Math.min(400, dataAmount.value));
  } else if (dataAmount.value % 40 !== 0) {
    errorMessage.value = t('message.syntheticData.errorMessage2');
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

  triggerToast(t('message.syntheticData.waitingMessage'), 'info');

  try {
    const response = await SyntheticDataService.postSyntheticData(dataAmount.value);

    if (response.status === "success") {
      triggerToast(t('message.syntheticData.successMessage'), 'success');
      setTimeout(() => {
        router.push('/');
      }, 2000);
    } else {
      throw new Error(response.message);
    }
  } catch (error) {
    triggerToast(t('message.syntheticData.errorMessage3'), 'danger');
  }
};

onMounted(async () => {
  try {
    const schema = await SyntheticDataService.getDatabaseSchema();
    databaseSchema.value = JSON.stringify(schema, null, 2);
  } catch (error) {
    triggerToast(t('message.syntheticData.errorMessage4'), 'danger');
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
      <h2 class="text-custom-purple">{{ t('message.syntheticData.title') }}</h2>
      <p>
        {{ t('message.syntheticData.description') }}
      </p>
    </div>

    <div class="schema-section">
      <h3 class="text-custom-purple">{{ t('message.syntheticData.databaseSchema') }}</h3>
      <div class="schema-display">
        <pre v-if="databaseSchema">{{ databaseSchema }}</pre>
        <p v-else class="text-muted">{{ t('message.syntheticData.loadingSchema') }}</p>
      </div>
    </div>

    <div class="input-section">
      <label for="data-amount" class="text-custom-purple">{{ t('message.syntheticData.numberOfRecords') }}</label>
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
      <button @click="generateData" class="btn btn-custom-purple">{{ t('message.syntheticData.generateData') }}</button>
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
