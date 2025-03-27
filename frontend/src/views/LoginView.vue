<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import UserService from '@/services/UserService';
import { userStore } from '@/store/userStore';

const router = useRouter();

const credentials = ref({
  email: '',
  password: ''
});

const loading = ref(false);
const errorMessage = ref('');

const login = async () => {
  try {
    loading.value = true;
    errorMessage.value = '';

    const response = await UserService.login(credentials.value);

    userStore.setToken(response.data.access_token);
    
    await router.push('/');
  } catch (error: unknown) {
    errorMessage.value = error instanceof Error ? error.message : 'An error occurred';
    console.error('Login error:', error);
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <main class="container-fluid d-flex justify-content-center align-items-center vh-100">
    <section class="config-panel p-5 rounded shadow-lg animate-fade-in">
      <h2 class="text-white text-center mb-4">Login</h2>
      
      <div v-if="errorMessage" class="alert alert-danger mb-4">
        {{ errorMessage }}
      </div>
      
      <form @submit.prevent="login" class="login-form">
        <div class="mb-3">
          <label for="loginEmail" class="form-label text-white">Email</label>
          <input
            v-model="credentials.email"
            type="email"
            class="form-control"
            id="loginEmail"
            placeholder="e.g., user@example.com"
            required
          >
        </div>
        
        <div class="mb-3">
          <label for="loginPassword" class="form-label text-white">Password</label>
          <input
            v-model="credentials.password"
            type="password"
            class="form-control"
            id="loginPassword"
            placeholder="Enter your password"
            required
          >
        </div>
        
        <div class="text-center mt-4">
          <button 
            type="submit" 
            class="btn btn-lg btn-outline-light animate-pulse"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
        </div>
        
        <div class="text-center mt-3">
          <router-link to="/register" class="text-white-50">Don't have an account? Register</router-link>
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
  max-width: 500px;
  background: rgba(123, 7, 121, 0.9);
  border-radius: 12px;
  box-shadow: 0px 4px 15px rgba(123, 7, 121, 0.3);
}

h2 {
  font-weight: bold;
}

.form-control {
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  transition: all 0.3s ease;
}

.form-control:focus {
  background-color: rgba(255, 255, 255, 0.3);
  box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.25);
}

.form-control::placeholder {
  color: rgba(255, 255, 255, 0.7);
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

.text-white-50 {
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
  transition: color 0.3s ease;
}

.text-white-50:hover {
  color: white;
}
</style>