import axios from 'axios';
import type { UserCreate } from '@/interfaces/User';
import type { AuthResponse } from '@/interfaces/Auth';

const API_URL: string = import.meta.env.VITE_API_URL as string;

class UserService {
  async register(userData: UserCreate): Promise<any> {
    try {
      const response = await axios.post<any>(
        `${API_URL}/auth/create`, 
        userData,
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      
      if (response.data.status !== 'success') {
        throw new Error(response.data.message || 'Registration failed');
      }
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.message || 'Error registering user');
      }
      throw new Error('Unknown error');
    }
  }

  async login(credentials: { email: string; password: string }): Promise<AuthResponse> {
    try {
      const response = await axios.post<AuthResponse>(
        `${API_URL}/auth/login`,
        credentials,
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      
      if (response.data.status !== 'success') {
        throw new Error(response.data.message || 'Login failed');
      }
      
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.message || 'Error logging in');
      }
      throw new Error('Unknown error while logging in');
    }
  }
}

export default new UserService();