<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '@/services/ApiBase';
import { userStore } from '@/store/userStore';

interface Credential {
  dbType: string;
  host: string;
  port: number;
  user: string;
  password: string;
  db_name: string;
  schema_name: string;
}

interface User {
  _id: string;
  name: string;
  email: string;
  main_credentials: Credential;
  credentials: Credential[];
}

const user = ref<User | null>(null);
const isLoading = ref(true);
const errorMessage = ref('');
const successMessage = ref('');

const fetchUser = async () => {
  isLoading.value = true;
  try {
    const userId = userStore.user?._id;
    
    if (!userId) {
      const userData = userStore.user;
      
      if (!userData) {
        throw new Error('User is not logged in');
      }
      
      const actualUserId = userData.data?._id || userData._id || userData.id;
      
      if (!actualUserId) {
        throw new Error('User ID not found in user data');
      }
      
      const response = await api.get(`/auth/${actualUserId}`);
      if (response.data.status === 'success') {
        user.value = response.data.data;
      } else {
        throw new Error(response.data.message || 'Failed to fetch user data');
      }
    } else {
      const response = await api.get(`/auth/${userId}`);
      if (response.data.status === 'success') {
        user.value = response.data.data;
      } else {
        throw new Error(response.data.message || 'Failed to fetch user data');
      }
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'An unknown error occurred';
    console.error('Error fetching user:', error);
  } finally {
    isLoading.value = false;
  }
};

const setMainCredential = async (index: number) => {
  isLoading.value = true;
  try {
    const userData = userStore.user;
    const userId = userData?.data?._id || userData?._id || userData?.id;
    
    if (!userId) {
      throw new Error('User ID not found');
    }
    
    const response = await api.put(`/auth/${userId}/credentials/${index}/main`);
    if (response.data.status === 'success') {
      user.value = response.data.data;
      successMessage.value = 'Main database updated successfully';
      setTimeout(() => {
        successMessage.value = '';
      }, 3000);
    } else {
      throw new Error(response.data.message || 'Failed to update main credential');
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'An unknown error occurred';
    console.error('Error setting main credential:', error);
    setTimeout(() => {
      errorMessage.value = '';
    }, 3000);
  } finally {
    isLoading.value = false;
  }
};

const isMainCredential = (credential: Credential) => {
  if (!user.value?.main_credentials) return false;
  
  return (
    credential.dbType === user.value.main_credentials.dbType &&
    credential.host === user.value.main_credentials.host &&
    credential.port === user.value.main_credentials.port &&
    credential.db_name === user.value.main_credentials.db_name &&
    credential.user === user.value.main_credentials.user
  );
};

onMounted(() => {
  fetchUser();
});
</script>

<template>
  <div class="container mt-5 mb-5">
    <div class="card shadow-lg p-4">
      <h2 class="fw-bold fs-3 text-custom-purple brand-text text-center mb-4">Database Configuration</h2>
      
      <div v-if="isLoading" class="text-center">
        <div class="spinner-border text-custom-purple" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      
      <div v-else-if="errorMessage" class="alert alert-danger" role="alert">
        {{ errorMessage }}
      </div>
      
      <div v-else-if="successMessage" class="alert alert-success" role="alert">
        {{ successMessage }}
      </div>
      
      <div v-else-if="!user?.credentials?.length" class="alert alert-info" role="alert">
        No database credentials configured.
      </div>
      
      <div v-else>
        <p class="mb-4">Select the main database to use:</p>
        
        <div class="list-group">
          <div 
            v-for="(credential, index) in user.credentials" 
            :key="index" 
            class="list-group-item list-group-item-action"
            :class="{'active': isMainCredential(credential)}"
          >
            <div class="d-flex w-100 justify-content-between align-items-center">
              <div>
                <h5 class="mb-1">{{ credential.dbType }} - {{ credential.db_name }}</h5>
                <p class="mb-1">Host: {{ credential.host }}:{{ credential.port }}</p>
                <p class="mb-1">User: {{ credential.user }}</p>
                <p class="mb-1" v-if="credential.schema_name">Schema: {{ credential.schema_name }}</p>
              </div>
              <div>
                <button 
                  v-if="!isMainCredential(credential)"
                  @click="setMainCredential(index)" 
                  class="btn btn-primary custom-btn"
                >
                  Set as main
                </button>
                <span v-else class="badge bg-custom-purple">Main database</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
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

.text-custom-purple {
  color: #800080;
}

.bg-custom-purple {
  background-color: #800080;
}

.list-group-item.active {
  background-color: rgba(128, 0, 128, 0.1);
  border-color: #800080;
  color: #212529;
}

.badge {
  font-size: 0.85rem;
  padding: 0.5rem 0.75rem;
}
</style>