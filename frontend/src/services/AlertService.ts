import api, { isAxiosError } from '@/services/ApiBase';
import type { ApiErrorResponse } from '@/interfaces/ApiErrorResponse';

class AlertService {
  async postCreateAlert(formData: any): Promise<any> {
    try {
      const response = await api.post<any>('/alerts/create', formData);
      
      if (!response.data?.success) {
        throw new Error(response.data?.message || 'Alert creation failed');
      }
      
      return response.data;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        
        const errorMessage = errorData?.message 
          || error.message 
          || 'Failed to create alert';
        
        console.error('Alert Creation Error:', {
          status: error.response?.status,
          message: errorMessage,
          data: error.response?.data
        });

        throw new Error(errorMessage);
      }

      console.error('Unknown error:', error);
      throw new Error('An unexpected error occurred while creating the alert');
    }
  }
}

export default new AlertService();