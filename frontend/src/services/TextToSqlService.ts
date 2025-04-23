import api, { isAxiosError } from '@/services/ApiBase';
import type { ApiResponse, QueryResults } from '@/interfaces/ApiResponse';
import type { ApiErrorResponse } from '@/interfaces/ApiErrorResponse';
import { dbCredentialsStore } from '@/store/dbCredentialsStore';
import { userStore } from '@/store/userStore';


class TextToSqlService {
  async processQuery(query: string, currentChatId?: string | null): Promise<QueryResults> {
    try {

      const credentials = dbCredentialsStore.credentials;
      const userId = userStore.user?.id;
      if (!credentials) {
        throw new Error('No database credentials found');
      }

      const response = await api.post<ApiResponse>('/text-to-sql/chat', {
        user_input: query,
        connection : {
          db_type: credentials.dbType,
          username: credentials.user,
          password: credentials.password,
          host: credentials.host,
          port: credentials.port,
          database_name: credentials.db_name,
          schema_name: credentials.schema_name
        },
        chat_data: {
          user_id: userId,
        },
        chat_id: currentChatId || null
      });

      if (!response.data?.data?.results) {
        throw new Error('Invalid response structure from API');
      }
      console.log(response.data.data.results);
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
