import axios, { AxiosError } from 'axios';
import { userStore } from '@/store/userStore';
import i18n from '@/i18n'; 

declare module 'axios' {
  interface AxiosInstance {
    isAxiosError(payload: any): payload is AxiosError;
  }
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.isAxiosError = (payload: any): payload is AxiosError => {
  return (payload as AxiosError).isAxiosError !== undefined;
};

api.interceptors.request.use(
  (config) => {
    const token = userStore.access_token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    config.headers['lang'] = i18n.global.locale.value;

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url.includes('/auth/refresh') &&
      !originalRequest.url.includes('/auth/login')
    ) {
      originalRequest._retry = true;

      try {
        const refreshed = await userStore.refreshToken();
        if (refreshed) {
          originalRequest.headers.Authorization = `Bearer ${userStore.access_token}`;
          originalRequest.headers['lang'] = i18n.global.locale.value; 
          return api(originalRequest);
        }
      } catch (refreshError) {
        console.error('Refresh token failed:', refreshError);
        userStore.logout();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export const isAxiosError = api.isAxiosError;

export default api;
