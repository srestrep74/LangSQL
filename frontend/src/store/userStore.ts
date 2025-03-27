import { reactive, watch } from 'vue';
import type { User, UserResponse } from '@/interfaces/User';
import type { AuthResponse } from '@/interfaces/Auth';
import { dbCredentialsStore } from './dbCredentialsStore';

const state = reactive({
  user: JSON.parse(sessionStorage.getItem('user') || 'null') as UserResponse | null,
  access_token: sessionStorage.getItem('access_token') || '',
});

watch(
  () => state.user,
  (newValue) => {
    if (newValue) {
      sessionStorage.setItem('user', JSON.stringify(newValue));
    } else {
      sessionStorage.removeItem('user');
    }
  },
  { deep: true }
);

watch(
  () => state.access_token,
  (newValue) => {
    if (newValue) {
      sessionStorage.setItem('access_token', newValue);
    } else {
      sessionStorage.removeItem('access_token');
    }
  }
);

export const userStore = {
  get user(): User | null {
    return state.user;
  },

  get isAuthenticated(): boolean {
    return !!state.access_token;
  },

  setUser(user: UserResponse): void {
    state.user = user;
  },

  setToken(token: string): void {
    state.access_token = token;
  },

  handleAuthResponse(response: AuthResponse): void {

    if (response.data?.user) {
      this.setUser(response.data.user);

      if (response.data.user.main_credentials) {
        dbCredentialsStore.setCredentials(response.data.user.main_credentials);
      }
    }

    if (response.data?.access_token) {
      this.setToken(response.data.access_token);
    }
  },

  clear(): void {
    sessionStorage.clear();
  },

  logout(): void {
    this.clear();
  },
};