<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { createUserService } from '@/services/DatabaseService';
import type { DBCredentials } from '@/interfaces/DBCredentials';
import { userStore } from '@/store/userStore';
import { dbCredentialsStore } from '@/store/dbCredentialsStore';

const databaseService = createUserService();

const credentials = ref<DBCredentials>({
  dbType: 'mysql',
  host: '',
  port: 3306,
  user: '',
  password: '',
  db_name: '',
  schema_name: ''
});

const loading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

const showSchemaField = ref(false);
const onDbTypeChange = () => {
  showSchemaField.value = credentials.value.dbType === 'postgresql';
};

const saveConfiguration = async () => {
  loading.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    const userId = userStore.user?.id;

    if (!userId) {
      throw new Error('User ID not found. Please log in again.');
    }

    const newCredential: DBCredentials = {
      ...credentials.value
    };

    const updatedUser = await databaseService.addCredential(userId, newCredential);

    if (updatedUser.credentials.length === 1) {
      await databaseService.setMainCredential(userId, 0);
      dbCredentialsStore.setCredentials(updatedUser.credentials[0]);
    }

    successMessage.value = 'Database configuration saved successfully!';

    credentials.value = {
      dbType: 'mysql',
      host: '',
      port: 3306,
      user: '',
      password: '',
      db_name: '',
      schema_name: ''
    };

    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'An error occurred while saving configuration';
    console.error('Error saving configuration:', error);

    setTimeout(() => {
      errorMessage.value = '';
    }, 5000);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  onDbTypeChange();
});
</script>

<template>
  <main class="container-fluid">
    <section class="config-section p-5">
      <div class="config-container">
        <div class="config-header text-center mb-5">
          <h1 class="display-5 fw-bold animate-slide-up">Database Configuration</h1>
          <p class="lead animate-fade-in">Connect to your databases and start querying with natural language</p>
        </div>

        <div class="row">
          <div class="col-lg-8 offset-lg-2">
            <div class="config-card p-4 rounded-lg shadow-lg animate-fade-in">
              <div class="card-header d-flex align-items-center mb-4">
                <i class="bi bi-database-fill me-3 header-icon"></i>
                <h2 class="m-0">Add New Database Connection</h2>
              </div>

              <div v-if="errorMessage" class="alert alert-danger animate-shake mb-4">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                {{ errorMessage }}
              </div>

              <div v-if="successMessage" class="alert alert-success animate-pulse mb-4">
                <i class="bi bi-check-circle-fill me-2"></i>
                {{ successMessage }}
              </div>

              <form @submit.prevent="saveConfiguration">
                <div class="row g-4">
                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="dbType" class="form-label">Database Type</label>
                      <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-hdd-network-fill"></i></span>
                        <select
                          v-model="credentials.dbType"
                          class="form-select"
                          id="dbType"
                          @change="onDbTypeChange"
                          required
                        >
                          <option value="mysql">MySQL</option>
                          <option value="postgresql">PostgreSQL</option>
                        </select>
                      </div>
                      <small class="form-text text-muted">
                        Default ports: MySQL (3306), PostgreSQL (5432)
                      </small>
                    </div>
                  </div>

                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="host" class="form-label">Host</label>
                      <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-globe"></i></span>
                        <input
                          v-model="credentials.host"
                          type="text"
                          class="form-control"
                          id="host"
                          placeholder="e.g., localhost or 127.0.0.1"
                          required
                        >
                      </div>
                    </div>
                  </div>

                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="port" class="form-label">Port</label>
                      <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-ethernet"></i></span>
                        <input
                          v-model="credentials.port"
                          type="number"
                          class="form-control"
                          id="port"
                          placeholder="Port number"
                          required
                        >
                      </div>
                    </div>
                  </div>

                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="username" class="form-label">Username</label>
                      <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-person-fill"></i></span>
                        <input
                          v-model="credentials.user"
                          type="text"
                          class="form-control"
                          id="username"
                          placeholder="Database username"
                          required
                        >
                      </div>
                    </div>
                  </div>

                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="password" class="form-label">Password</label>
                      <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-key-fill"></i></span>
                        <input
                          v-model="credentials.password"
                          type="password"
                          class="form-control"
                          id="password"
                          placeholder="Database password"
                          required
                        >
                      </div>
                    </div>
                  </div>

                  <div class="col-md-6">
                    <div class="form-group">
                      <label for="database" class="form-label">Database Name</label>
                      <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-folder-fill"></i></span>
                        <input
                          v-model="credentials.db_name"
                          type="text"
                          class="form-control"
                          id="database"
                          placeholder="Name of the database"
                          required
                        >
                      </div>
                    </div>
                  </div>

                  <div v-if="showSchemaField" class="col-md-6">
                    <div class="form-group">
                      <label for="schema" class="form-label">Schema Name</label>
                      <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-diagram-3-fill"></i></span>
                        <input
                          v-model="credentials.schema_name"
                          type="text"
                          class="form-control"
                          id="schema"
                          placeholder="Schema name (e.g., public)"
                        >
                      </div>
                    </div>
                  </div>

                  <div class="col-md-12">
                    <div class="form-group mt-4">
                      <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                        <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                        <i v-else class="bi bi-save-fill me-2"></i>
                        {{ loading ? 'Saving...' : 'Save Configuration' }}
                      </button>
                    </div>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.config-section {
  min-height: 100vh;
  background: linear-gradient(135deg, #a23dbf, #e289ff);
  color: #f5f5f5;
  font-family: 'Inter', sans-serif;
}

.config-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 0;
}

.config-header {
  margin-bottom: 2rem;
}

.config-card {
  background: rgba(255, 255, 255, 0.95);
  color: #333;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.card-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  padding-bottom: 1rem;
}

.header-icon {
  font-size: 1.8rem;
  color: #7b0779;
}

.form-label {
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #555;
}

.form-control, .form-select {
  border: 1px solid rgba(0, 0, 0, 0.1);
  padding: 0.6rem 0.75rem;
}

.form-control:focus, .form-select:focus {
  border-color: #a23dbf;
  box-shadow: 0 0 0 0.25rem rgba(162, 61, 191, 0.25);
}

.input-group-text {
  background-color: #f8f9fa;
  border: 1px solid rgba(0, 0, 0, 0.1);
  color: #7b0779;
}

.btn-primary {
  background-color: #a23dbf !important;
  border-color: #a23dbf !important;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary:hover, .btn-primary:focus {
  background-color: #7b0779 !important;
  border-color: #7b0779 !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(123, 7, 121, 0.3);
}

.btn-outline-secondary {
  color: #555;
  border-color: #ced4da;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-outline-secondary:hover {
  background-color: #f8f9fa;
  color: #333;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.existing-connections {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

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
  animation: pulse 1.5s;
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
  .config-section {
    padding: 2rem 1rem;
  }

  .config-card {
    padding: 1.5rem;
  }

  .existing-connections {
    padding: 1.5rem;
  }
}
</style>