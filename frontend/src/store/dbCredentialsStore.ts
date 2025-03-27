import { reactive, watch } from 'vue';
import type { DBCredentials } from '@/interfaces/DBCredentials';

const state = reactive({
  credentials: JSON.parse(sessionStorage.getItem('dbCredentials') || 'null') as DBCredentials | null,
});

watch(
  () => state.credentials,
  (newValue) => {
    if (newValue) {
      sessionStorage.setItem('dbCredentials', JSON.stringify(newValue));
    } else {
      sessionStorage.removeItem('dbCredentials');
    }
  },
  { deep: true }
);

export const dbCredentialsStore = {
  get credentials(): DBCredentials | null {
    return state.credentials;
  },

  setCredentials(credentials: DBCredentials): void {
    state.credentials = credentials;
  },

  clear(): void {
    state.credentials = null;
  }
};