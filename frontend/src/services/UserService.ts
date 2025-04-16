import api, { isAxiosError } from '@/services/ApiBase';
import type { UserCreate } from '@/interfaces/User';
import type { AuthResponse } from '@/interfaces/Auth';
import type { ApiErrorResponse } from '@/interfaces/ApiErrorResponse';

class UserService {
  async register(userData: UserCreate): Promise<any> {
    try {
      const response = await api.post<any>('/auth/create', userData);
      
      if (response.data.status !== 'success') {
        throw new Error(response.data.message || 'Registration failed');
      }
      return response.data;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        throw new Error(errorData?.message || 'Error registering user');
      }
      throw new Error('Unknown error during registration');
    }
  }

  async login(credentials: { email: string; password: string }): Promise<AuthResponse> {
    try {
      const response = await api.post<AuthResponse>('/auth/login', credentials);
      
      if (response.data.status !== 'success') {
        throw new Error(response.data.message || 'Login failed');
      }
      
      return response.data;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        throw new Error(errorData?.message || 'Error logging in');
      }
      throw new Error('Unknown error while logging in');
    }
  }

  async refreshToken(refreshToken: string): Promise<AuthResponse> {
    try {
      const response = await api.post<AuthResponse>('/auth/refresh', {
        refresh_token: refreshToken
      });
      return response.data;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        throw new Error(errorData?.message || 'Error refreshing token');
      }
      throw new Error('Unknown error while refreshing token');
    }
  }
}

export default new UserService();