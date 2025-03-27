<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import UserService from '@/services/UserService';
import { dbCredentialsStore } from '@/store/dbCredentialsStore';
import type { UserCreate } from '@/interfaces/User';
import type { DBCredentials, DatabaseType } from '@/interfaces/DBCredentials';

const router = useRouter();
const currentStep = ref(1);

const initialCredentials: DBCredentials = {
  dbType: 'mysql',
  host: 'localhost',
  port: 3306,
  user: '',
  password: '',
  db_name: ''
};

const userData = ref<UserCreate>({
  name: '',
  email: '',
  password: '',
  main_credentials: { ...initialCredentials },
  credentials: [],
  queries: [],
  alerts: []
});

const loading = ref(false);
const errorMessage = ref('');

const dbTypes: DatabaseType[] = ['mysql', 'postgresql'];

const nextStep = () => {
  if (!userData.value.name || !userData.value.email || !userData.value.password) {
    errorMessage.value = 'Please fill all required fields';
    return;
  }
  currentStep.value = 2;
};

const prevStep = () => {
  currentStep.value = 1;
};

const register = async () => {
  try {
    loading.value = true;
    errorMessage.value = '';

    const mainCredentials = { ...userData.value.main_credentials };
    userData.value.credentials = [mainCredentials];
    
    const response = await UserService.register(userData.value);
    
    await router.push('/login');
  } catch (error: unknown) {
    errorMessage.value = error instanceof Error ? error.message : 'An error occurred';
    console.error('Registration error:', error);
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <main class="container-fluid d-flex justify-content-center align-items-center vh-100">
    <section class="config-panel p-5 rounded shadow-lg animate-fade-in">
      <h2 class="text-white text-center mb-4">User Registration</h2>
      
      <div v-if="errorMessage" class="alert alert-danger mb-4">
        {{ errorMessage }}
      </div>
      
      <form @submit.prevent="register" class="registration-form">
        <!-- Step 1: User Information -->
        <div v-if="currentStep === 1" class="step-content">
          <div class="mb-3">
            <label for="name" class="form-label text-white">Full Name</label>
            <input
              v-model="userData.name"
              type="text"
              class="form-control"
              id="name"
              placeholder="e.g., John Doe"
              required
            >
          </div>
          
          <div class="mb-3">
            <label for="email" class="form-label text-white">Email</label>
            <input
              v-model="userData.email"
              type="email"
              class="form-control"
              id="email"
              placeholder="e.g., user@example.com"
              required
            >
          </div>
          
          <div class="mb-3">
            <label for="password" class="form-label text-white">Password</label>
            <input
              v-model="userData.password"
              type="password"
              class="form-control"
              id="password"
              placeholder="Minimum 8 characters"
              required
              minlength="8"
            >
          </div>
          
          <div class="text-center mt-4">
            <button 
              type="button" 
              class="btn btn-lg btn-outline-light animate-pulse"
              @click="nextStep"
            >
              Next: Database Configuration
            </button>
          </div>
        </div>
        
        <!-- Step 2: Database Configuration -->
        <div v-if="currentStep === 2" class="step-content">
          <div class="mb-3">
            <label for="dbType" class="form-label text-white">Database Type</label>
            <select
              v-model="userData.main_credentials.dbType"
              class="form-select"
              id="dbType"
              required
            >
              <option 
                v-for="dbType in dbTypes" 
                :key="dbType" 
                :value="dbType"
              >
                {{ dbType.toUpperCase() }}
              </option>
            </select>
          </div>
          
          <div class="mb-3">
            <label for="host" class="form-label text-white">Host</label>
            <input
              v-model="userData.main_credentials.host"
              type="text"
              class="form-control"
              id="host"
              placeholder="e.g., localhost or 127.0.0.1"
              required
            >
          </div>
          
          <div class="mb-3">
            <label for="port" class="form-label text-white">Port</label>
            <input
              v-model.number="userData.main_credentials.port"
              type="number"
              class="form-control"
              id="port"
              placeholder="e.g., 3306 for MySQL"
              required
            >
          </div>
          
          <div class="mb-3">
            <label for="dbUser" class="form-label text-white">Database User</label>
            <input
              v-model="userData.main_credentials.user"
              type="text"
              class="form-control"
              id="dbUser"
              placeholder="Database user"
              required
            >
          </div>
          
          <div class="mb-3">
            <label for="dbPassword" class="form-label text-white">Database Password</label>
            <input
              v-model="userData.main_credentials.password"
              type="password"
              class="form-control"
              id="dbPassword"
              placeholder="Database password"
              required
            >
          </div>
          
          <div class="mb-3">
            <label for="dbName" class="form-label text-white">Database Name</label>
            <input
              v-model="userData.main_credentials.db_name"
              type="text"
              class="form-control"
              id="dbName"
              placeholder="Name of the database to connect"
              required
            >
          </div>
          
          <div class="d-flex justify-content-between mt-4">
            <button 
              type="button" 
              class="btn btn-outline-light"
              @click="prevStep"
            >
              Back
            </button>
            <button 
              type="submit" 
              class="btn btn-lg btn-outline-light animate-pulse"
              :disabled="loading"
            >
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              {{ loading ? 'Registering...' : 'Complete Registration' }}
            </button>
          </div>
        </div>
      </form>
    </section>
  </main>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');

body {
  font-family: 'Inter', sans-serif;
  background: linear-gradient(135deg, #a23dbf, #e289ff);
}

.config-panel {
  width: 50%;
  max-width: 600px;
  background: rgba(123, 7, 121, 0.9);
  border-radius: 12px;
  box-shadow: 0px 4px 15px rgba(123, 7, 121, 0.3);
}

h2 {
  font-weight: bold;
}

.form-control, .form-select {
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
  background-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.25);
}

.form-control::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.form-select option {
  background: white;
  color: #7b0779;
  font-weight: bold;
}

.btn-outline-light {
  border: 2px solid white;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-outline-light:hover {
  background-color: white;
  color: #7b0779;
}

.alert-danger {
  background-color: rgba(220, 53, 69, 0.8);
  border-color: rgba(220, 53, 69, 0.8);
  color: white;
}

.step-content {
  animation: fadeIn 0.5s ease-in-out;
}

/* Animations */
.animate-fade-in {
  animation: fadeIn 1s ease-in-out;
}

.animate-pulse {
  animation: pulse 1.5s infinite;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

@media (max-width: 768px) {
  .config-panel {
    width: 90%;
    padding: 2rem;
  }
}
</style>