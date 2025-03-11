<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import AlertService from '../services/AlertService';

// Vue Router
const router = useRouter();

// Form fields
const notificationEmails = ref('');
const prompt = ref('');
const expirationDate = ref('');
const isLoading = ref(false);

const submitForm = async () => {
  isLoading.value = true;

  try {
    const formData = {
      notification_emails: notificationEmails.value.split(',').map(email => email.trim()),
      prompt: prompt.value,
      expiration_date: new Date(expirationDate.value).toISOString()
    };

    await AlertService.postCreateAlert(formData);
    isLoading.value = false;
    alert('Alert created successfully!');
    router.push('/');
  } catch (error) {
    isLoading.value = false;
    alert('Failed to create alert. Please try again.');
  }
};

onMounted(() => {
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipTriggerList.forEach(el => new window.bootstrap.Tooltip(el));
});
</script>

<template>
    <div class="container d-flex justify-content-center align-items-center vh-100">
      <div class="card shadow-lg p-4 col-md-6">
        <h2 class="fw-bold fs-3 text-custom-purple brand-text text-center mb-4">Create Alert</h2>
        
        <div v-if="isLoading" class="alert alert-info text-center fade show" role="alert">
          ⏳ Generating your alert... You will be notified when is ready.
        </div>
  
        <form @submit.prevent="submitForm">
          
          <div class="mb-3">
            <label class="form-label">
              Emails to Notify:*
              <span 
                  class="tooltip-icon" 
                  data-bs-toggle="tooltip" 
                  title="Enter multiple emails separated by commas">
                  ?
              </span>
            </label>
            <input v-model="notificationEmails" type="text" class="form-control">
          </div>
  
          <div class="mb-3">
            <label class="form-label">
              Condition:*
              <span 
                class="tooltip-icon" 
                data-bs-toggle="tooltip" 
                title="Specify the condition that triggers this alert">
                ?
              </span>
            </label>
            <textarea v-model="prompt" class="form-control" rows="3"></textarea>
          </div>
  
          <div class="mb-3">
            <label class="form-label">
              Expiration Date:*
              <span 
                class="tooltip-icon" 
                data-bs-toggle="tooltip" 
                title="Choose when this alert should expire">
                ?
              </span>
            </label>
            <input v-model="expirationDate" type="datetime-local" class="form-control">
          </div>
  
          <button type="submit" class="btn btn-primary btn-lg btn-block custom-btn">
            Submit
          </button>
          
        </form>
      </div>
    </div>
</template>  

<style scoped>
.form-control {
  border: 1px solid #ced4da;
}

.card {
  max-width: 500px;
  width: 100%;
  border-radius: 10px;
}

.custom-btn {
  background-color: #800080 !important;
  border-color: #800080 !important;
}

.custom-btn:hover {
  background-color: #6a006a !important;
  border-color: #6a006a !important;
}

textarea {
  resize: none;
}

.tooltip-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  font-size: 14px;
  font-weight: bold;
  color: white !important;
  background-color: #800080;
  border-radius: 50%;
  cursor: pointer;
  text-align: center;
  margin-left: 5px;
}

.alert {
  font-weight: bold;
  font-size: 16px;
}
</style>
