import api, { isAxiosError } from '@/services/ApiBase';
import type { ApiErrorResponse } from '@/interfaces/ApiErrorResponse';

class SyntheticDataService {
  async postSyntheticData(formData: any): Promise<any> {
    try {
      const response = await api.post('/text-to-sql/generate_synthetic_data', formData);
      
      if (!response.data) {
        throw new Error('Empty response from server');
      }
      
      return response.data;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        
        const errorMessage = errorData?.message 
          || error.message 
          || 'Failed to generate synthetic data';
        
        console.error('API Error:', {
          status: error.response?.status,
          message: errorMessage,
          data: error.response?.data
        });

        throw new Error(errorMessage);
      }

      console.error('Unknown error:', error);
      throw new Error('An unexpected error occurred while generating synthetic data');
    }
  }
}

export default new SyntheticDataService();