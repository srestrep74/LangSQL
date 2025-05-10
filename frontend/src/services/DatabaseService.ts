import api, { isAxiosError } from '@/services/ApiBase';
import type { UserResponse } from '@/interfaces/User';
import type { DBCredentials } from '@/interfaces/DBCredentials';
import type { ApiErrorResponse } from '@/interfaces/ApiErrorResponse';

export interface DatabaseService {
  getUserData(userId: string): Promise<UserResponse>;
  setMainCredential(userId: string, credentialIndex: number): Promise<UserResponse>;
  addCredential(userId: string, credential: DBCredentials): Promise<UserResponse>;
  removeCredential(userId: string, credentialIndex: number): Promise<UserResponse>;
}

export function createUserService(): DatabaseService {
  return {
    async getUserData(userId: string): Promise<UserResponse> {
      try {
        const response = await api.get(`/auth/${userId}`);
        if (response.data.status === 'success') {
          return response.data.data;
        } else {
          throw new Error(response.data.message || 'Failed to fetch user data');
        }
      } catch (error) {
        if (isAxiosError(error)) {
          const errorData = error.response?.data as ApiErrorResponse;
          throw new Error(errorData?.message || 'Error fetching user data');
        }
        throw error instanceof Error ? error : new Error('Unknown error fetching user data');
      }
    },

    async setMainCredential(userId: string, credentialIndex: number): Promise<UserResponse> {
      try {
        const response = await api.put(`/auth/${userId}/credentials/${credentialIndex}/main`);
        if (response.data.status === 'success') {
          return response.data.data;
        } else {
          throw new Error(response.data.message || 'Failed to update main credential');
        }
      } catch (error) {
        if (isAxiosError(error)) {
          const errorData = error.response?.data as ApiErrorResponse;
          throw new Error(errorData?.message || 'Error updating main credential');
        }
        throw error instanceof Error ? error : new Error('Unknown error updating main credential');
      }
    },

    async addCredential(userId: string, credential: DBCredentials): Promise<UserResponse> {
      try {
        const response = await api.post(`/auth/${userId}/credentials`, credential);
        if (response.data.status === 'success') {
          return response.data.data;
        } else {
          throw new Error(response.data.message || 'Failed to add database credential');
        }
      } catch (error) {
        if (isAxiosError(error)) {
          const errorData = error.response?.data as ApiErrorResponse;
          throw new Error(errorData?.message || 'Error adding database credential');
        }
        throw error instanceof Error ? error : new Error('Unknown error adding database credential');
      }
    },

    async removeCredential(userId: string, credentialIndex: number): Promise<UserResponse> {
      try {
        const response = await api.delete(`/auth/${userId}/credentials/${credentialIndex}`);
        if (response.data.status === 'success') {
          return response.data.data;
        } else {
          throw new Error(response.data.message || 'Failed to remove database credential');
        }
      } catch (error) {
        if (isAxiosError(error)) {
          const errorData = error.response?.data as ApiErrorResponse;
          throw new Error(errorData?.message || 'Error removing database credential');
        }
        throw error instanceof Error ? error : new Error('Unknown error removing database credential');
      }
    }
  };
}
