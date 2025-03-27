import api, { isAxiosError } from '@/services/ApiBase';
import type { ApiResponse, QueryResults } from '@/interfaces/ApiResponse';
import type { ApiErrorResponse } from '@/interfaces/ApiErrorResponse';


class TextToSqlService {
  async processQuery(query: string): Promise<QueryResults> {
    try {
      const response = await api.post<ApiResponse>('/text-to-sql/process_query', { 
        user_input: query,
        schema_name: 'inventory'
      });

      if (!response.data?.data?.results) {
        throw new Error('Invalid response structure from API');
      }

      return response.data.data.results;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        
        const errorMessage = errorData?.message 
          || error.message 
          || 'Error processing query';
        
        console.error('API Error:', {
          status: error.response?.status,
          message: errorMessage,
          data: error.response?.data
        });

        throw new Error(errorMessage);
      }

      console.error('Unknown error:', error);
      throw new Error('An unknown error occurred while processing your query');
    }
  }
}

export default new TextToSqlService();