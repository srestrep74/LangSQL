<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import UserService from '@/services/UserService';
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
  <main class="container-fluid">
    <section class="hero text-center text-white d-flex flex-column justify-content-center align-items-center py-5">
      <div class="login-container animate-fade-in my-5">
        <h1 class="display-4 fw-bold mb-4 text-white">Create Your LangSQL Account</h1>
        <p class="lead mb-5 animate-slide-up text-white">Start querying your database with natural language</p>
        
        <div class="login-card p-5 rounded my-4">
          <div v-if="errorMessage" class="alert alert-danger mb-4 animate-shake">
            {{ errorMessage }}
          </div>
          
          <form @submit.prevent="register" class="login-form">
            <!-- Step 1: User Information -->
            <div v-if="currentStep === 1" class="step-content">
              <div class="row g-4">
                <div class="col-12">
                  <label for="name" class="form-label text-white d-block text-start mb-2">Full Name</label>
                  <input
                    v-model="userData.name"
                    type="text"
                    class="form-control-lg"
                    id="name"
                    placeholder="e.g., John Doe"
                    required
                  >
                </div>
                
                <div class="col-md-6">
                  <label for="email" class="form-label text-white d-block text-start mb-2">Email</label>
                  <input
                    v-model="userData.email"
                    type="email"
                    class="form-control-lg"
                    id="email"
                    placeholder="e.g., user@example.com"
                    required
                  >
                </div>
                
                <div class="col-md-6">
                  <label for="password" class="form-label text-white d-block text-start mb-2">Password</label>
                  <input
                    v-model="userData.password"
                    type="password"
                    class="form-control-lg"
                    id="password"
                    placeholder="Minimum 8 characters"
                    required
                    minlength="8"
                  >
                </div>
              </div>
              
              <div class="text-center mt-5">
                <button 
                  type="button" 
                  class="btn btn-lg hero-btn animate-pulse"
                  @click="nextStep"
                >
                  Next
                </button>
              </div>
              
              <div class="text-center mt-4">
                <router-link to="/login" class="text-link">Already have an account? <span class="fw-bold">Login here</span></router-link>
              </div>
            </div>
            
            <!-- Step 2: Database Configuration -->
            <div v-if="currentStep === 2" class="step-content">
              <div class="row g-4">
                <div class="col-md-6">
                  <label for="dbType" class="form-label text-white d-block text-start mb-2">Database Type</label>
                  <select
                    v-model="userData.main_credentials.dbType"
                    class="form-control-lg"
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
                
                <div class="col-md-6">
                  <label for="host" class="form-label text-white d-block text-start mb-2">Host</label>
                  <input
                    v-model="userData.main_credentials.host"
                    type="text"
                    class="form-control-lg"
                    id="host"
                    placeholder="e.g., localhost or 127.0.0.1"
                    required
                  >
                </div>
                
                <div class="col-md-3">
                  <label for="port" class="form-label text-white d-block text-start mb-2">Port</label>
                  <input
                    v-model.number="userData.main_credentials.port"
                    type="number"
                    class="form-control-lg"
                    id="port"
                    placeholder="e.g., 3306 for MySQL"
                    required
                  >
                </div>
                
                <div class="col-md-4">
                  <label for="dbUser" class="form-label text-white d-block text-start mb-2">DB User</label>
                  <input
                    v-model="userData.main_credentials.user"
                    type="text"
                    class="form-control-lg"
                    id="dbUser"
                    placeholder="Database user"
                    required
                  >
                </div>
                
                <div class="col-md-5">
                  <label for="dbPassword" class="form-label text-white d-block text-start mb-2">DB Password</label>
                  <input
                    v-model="userData.main_credentials.password"
                    type="password"
                    class="form-control-lg"
                    id="dbPassword"
                    placeholder="Database password"
                    required
                  >
                </div>
                
                <div class="col-12">
                  <label for="dbName" class="form-label text-white d-block text-start mb-2">Database Name</label>
                  <input
                    v-model="userData.main_credentials.db_name"
                    type="text"
                    class="form-control-lg"
                    id="dbName"
                    placeholder="Name of the database to connect"
                    required
                  >
                </div>
              </div>
              
              <div class="d-flex justify-content-between mt-5">
                <button 
                  type="button" 
                  class="btn btn-outline-light"
                  @click="prevStep"
                >
                  Back
                </button>
                <button 
                  type="submit" 
                  class="btn btn-lg hero-btn animate-pulse"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ loading ? 'Registering...' : 'Complete Registration' }}
                </button>
              </div>
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
  max-width: 600px;
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

select.form-control-lg {
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath fill='white' d='M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 16px 12px;
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

.btn-outline-light {
  border: 2px solid white;
  color: white;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-outline-light:hover {
  background-color: white;
  color: #7b0779;
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

.step-content {
  animation: fadeIn 0.3s ease-in-out;
}

/* Animations */
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
  
  .row.g-4 > [class^="col-"] {
    width: 100%;
    max-width: 100%;
  }
}
</style>