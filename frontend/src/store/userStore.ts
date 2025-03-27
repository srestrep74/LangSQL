import { reactive, watch } from 'vue';
import type { User, UserResponse } from '@/interfaces/User';
import type { AuthResponse } from '@/interfaces/Auth';
import  UserService  from '@/services/UserService';
import { dbCredentialsStore } from './dbCredentialsStore';

const state = reactive({
  user: JSON.parse(sessionStorage.getItem('user') || 'null') as UserResponse | null,
  access_token: sessionStorage.getItem('access_token') || '',
  refresh_token: sessionStorage.getItem('refresh_token') || '',
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

  get access_token(): string {
    return state.access_token;
  },

  get refresh_token(): string {
    return state.refresh_token;
  },

  get isAuthenticated(): boolean {
    return !!state.access_token;
  },

  setUser(user: UserResponse): void {
    state.user = user;
  },

  setTokens(access_token: string, refresh_token: string): void {
    state.access_token = access_token;
    state.refresh_token = refresh_token;
  },

  setToken(access_token: string): void {
    state.access_token = access_token;
  },

  async refreshToken(): Promise<boolean> {
    try {
      const response = await UserService.refreshToken(state.refresh_token);
      if(response.data?.access_token) {
        this.setToken(response.data.access_token);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error refreshing token:', error);
      return false;
    }
  },

  handleAuthResponse(response: AuthResponse): void {

    if (response.data?.user) {
      this.setUser(response.data.user);

      if (response.data.user.main_credentials) {
        dbCredentialsStore.setCredentials(response.data.user.main_credentials);
      }
    }

    if (response.data?.access_token && response.data?.refresh_token) {
      this.setTokens(response.data.access_token, response.data.refresh_token);
    }
  },

  clear(): void {
    sessionStorage.clear();
  },

  logout(): void {
    dbCredentialsStore.clear();
    state.user = null;
    state.access_token = '';
    this.clear();
  },
};