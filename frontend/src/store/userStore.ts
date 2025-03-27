import { reactive, watch } from 'vue';
import type { User } from '@/interfaces/User';
import type { AuthResponse } from '@/interfaces/Auth';

const state = reactive({
  user: JSON.parse(sessionStorage.getItem('user') || 'null') as User | null,
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

  setUser(user: User): void {
    state.user = user;
  },

  setToken(token: string): void {
    state.access_token = token;
  },

  handleAuthResponse(response: AuthResponse): void {
    if (response.data?.access_token) {
      this.setToken(response.data.access_token);
    }
  },

  clear(): void {
    state.user = null;
    state.access_token = '';
  },

  logout(): void {
    this.clear();
  },
};