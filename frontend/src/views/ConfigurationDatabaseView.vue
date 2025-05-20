<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { userStore } from '@/store/userStore';
import { dbCredentialsStore } from '@/store/dbCredentialsStore';
import type { UserResponse } from '@/interfaces/User';
import type { DBCredentials } from '@/interfaces/DBCredentials';
import { createUserService } from '@/services/DatabaseService';

const { t } = useI18n();
const userService = createUserService();
const user = ref<UserResponse | null>(null);
const isLoading = ref(true);
const errorMessage = ref('');
const successMessage = ref('');

const fetchUser = async () => {
  isLoading.value = true;
  try {
    const userId = userStore.user?.id;

    if (!userId) {
      throw new Error('User ID not found in user data');
    }

    const userData = await userService.getUserData(userId);
    user.value = userData;
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
    const userId = userStore.user?.id;

    if (!userId) {
      throw new Error('User ID not found');
    }

    const updatedUser = await userService.setMainCredential(userId, index);
    user.value = updatedUser;

    if (user.value?.main_credentials) {
      dbCredentialsStore.setCredentials(user.value.main_credentials);
    }

    successMessage.value = t('message.database.configuration.successMessage');
    setTimeout(() => {
      successMessage.value = '';
    }, 3000);
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

const isMainCredential = (credential: DBCredentials) => {
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
      <h2 class="fw-bold fs-3 text-custom-purple brand-text text-center mb-4">{{ t('message.database.configuration.title') }}</h2>

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
        {{ t('message.database.configuration.noCredentials') }}
      </div>

      <div v-else>
        <p class="mb-4">{{ t('message.database.configuration.selectMain') }}</p>

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
                <p class="mb-1">{{ t('message.database.configuration.host') }}: {{ credential.host }}:{{ credential.port }}</p>
                <p class="mb-1">{{ t('message.database.configuration.user') }}: {{ credential.user }}</p>
                <p class="mb-1" v-if="credential.schema_name">{{ t('message.database.configuration.schema') }}: {{ credential.schema_name }}</p>
              </div>
              <div>
                <button
                  v-if="!isMainCredential(credential)"
                  @click="setMainCredential(index)"
                  class="btn btn-primary custom-btn"
                >
                  {{ t('message.database.configuration.setAsMain') }}
                </button>
                <span v-else class="badge bg-custom-purple">{{ t('message.database.configuration.mainDatabase') }}</span>
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
