<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import UserService from '@/services/UserService';
import { userStore } from '@/store/userStore';

const { t, locale } = useI18n();
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

    userStore.handleAuthResponse(response);
    await router.push('/');
  } catch (error: unknown) {
    errorMessage.value = error instanceof Error ? error.message : t('message.login.error');
    console.error('Login error:', error);
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <main class="container-fluid">
    <section class="hero text-center text-white d-flex flex-column justify-content-center align-items-center py-5">
      <div class="login-container animate-fade-in my-5">
        <h1 class="display-4 fw-bold mb-4 text-white">{{ t('message.login.title') }}</h1>
        <p class="lead mb-5 animate-slide-up text-white">{{ t('message.login.subtitle') }}</p>

        <div class="login-card p-5 rounded my-4">
          <div v-if="errorMessage" class="alert alert-danger mb-4 animate-shake">
            {{ t('message.login.error') }}: {{ errorMessage }}
          </div>

          <form @submit.prevent="login" class="login-form">
            <div class="mb-4">
              <label for="loginEmail" class="form-label text-white d-block text-start mb-2">{{ t('message.login.email') }}</label>
              <input
                v-model="credentials.email"
                type="email"
                class="form-control-lg"
                id="loginEmail"
                placeholder="e.g., user@example.com"
                required
              >
            </div>

            <div class="mb-4">
              <label for="loginPassword" class="form-label text-white d-block text-start mb-2">{{ t('message.login.password') }}</label>
              <input
                v-model="credentials.password"
                type="password"
                class="form-control-lg"
                id="loginPassword"
                placeholder="••••••••"
                required
              >
            </div>

            <div class="text-center mt-5">
              <button 
                type="submit" 
                class="btn btn-lg hero-btn animate-pulse"
                :disabled="loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ loading ? t('message.login.loading') : t('message.login.button') }}
              </button>
            </div>

            <div class="text-center mt-4">
              <router-link to="/register" class="text-link">
                {{ t('message.login.registerPrompt') }}
              </router-link>
            </div>
          </form>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

body {
  font-family: 'Inter', sans-serif;
  color: #f5f5f5;
}

.hero {
  min-height: 100vh;
  background: linear-gradient(135deg, #a23dbf, #e289ff);
  padding: 4rem 2rem;
}

.login-container {
  width: 100%;
  max-width: 500px;
  margin: 2rem auto;
}

.login-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin: 2rem 0;
}

.form-control-lg {
  width: 100%;
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.15);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-control-lg:focus {
  background-color: rgba(255, 255, 255, 0.25);
  box-shadow: 0 0 0 0.25rem rgba(255, 255, 255, 0.15);
  outline: none;
}

.form-control-lg::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.hero-btn {
  background-color: #7b0779;
  color: white;
  font-weight: 600;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  box-shadow: 0px 4px 15px rgba(123, 7, 121, 0.3);
  width: 100%;
  max-width: 300px;
}

.hero-btn:hover {
  background-color: #6a0668;
  transform: translateY(-2px);
  box-shadow: 0px 6px 20px rgba(123, 7, 121, 0.4);
}

.hero-btn:disabled {
  background-color: #9d50bb;
  transform: none;
  box-shadow: none;
}

.alert-danger {
  background-color: rgba(220, 53, 69, 0.8);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 500;
}

.text-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s ease;
}

.text-link:hover {
  color: white;
  text-decoration: underline;
}

/* Animaciones */
.animate-fade-in {
  animation: fadeIn 1s ease-in-out;
}
.animate-slide-up {
  animation: slideUp 1s ease-in-out;
}
.animate-shake {
  animation: shake 0.5s ease-in-out;
}
.animate-pulse {
  animation: pulse 1.5s infinite;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-5px); }
  40%, 80% { transform: translateX(5px); }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.02); }
  100% { transform: scale(1); }
}

@media (max-width: 768px) {
  .hero {
    padding: 3rem 1.5rem;
  }

  .login-container {
    padding: 0 1.5rem;
  }

  .login-card {
    padding: 2rem 1.5rem;
    margin: 1.5rem 0;
  }

  h1 {
    font-size: 2.2rem;
  }

  .hero-btn {
    max-width: 100%;
  }
}
</style>