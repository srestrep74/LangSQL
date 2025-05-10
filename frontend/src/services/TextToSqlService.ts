import api, { isAxiosError } from '@/services/ApiBase';
import type { ApiResponse, QueryResults, ChatData } from '@/interfaces/ApiResponse';
import type { ApiErrorResponse } from '@/interfaces/ApiErrorResponse';
import { dbCredentialsStore } from '@/store/dbCredentialsStore';
import { userStore } from '@/store/userStore';


class TextToSqlService {
  async processQuery(query: string, chatData?: ChatData, chatId?: string | null): Promise<QueryResults> {
    try {
      const credentials = dbCredentialsStore.credentials;
      if (!credentials) {
        throw new Error('No database credentials found');
      }

      // Use provided chatData or create a default one
      const finalChatData = chatData || {
        user_id: userStore.user?.id || '',
        messages: []
      };

      const response = await api.post<ApiResponse>('/text-to-sql/chat', {
        user_input: query,
        connection: {
          db_type: credentials.dbType,
          username: credentials.user,
          password: credentials.password,
          host: credentials.host,
          port: credentials.port,
          database_name: credentials.db_name,
          schema_name: credentials.schema_name
        },
        chat_data: finalChatData,
        chat_id: chatId || null
      });

      // Add more detailed logging to debug the response
      console.log('API Response:', response.data);

      // Check for error response
      if (response.data.status === 'error') {
        console.error('API returned error:', response.data);
        throw new Error(response.data.details?.error || response.data.message || 'Unknown API error');
      }

      if (!response.data?.data?.results) {
        console.error('Invalid response structure:', response.data);

        // Create a fallback response for empty queries (when just loading chat history)
        if (!query && chatId) {
          return {
            chat_id: chatId,
            header: '',
            sql_query: '',
            sql_results: '[]',
            chats: [],
            messages: []
          };
        }

        throw new Error('Invalid response structure from API');
      }

      // Ensure the results object has all required fields
      const results = response.data.data.results;
      return {
        chat_id: results.chat_id || chatId || '',
        header: results.header || '',
        sql_query: results.sql_query || '',
        sql_results: typeof results.sql_results === 'string' ?
          results.sql_results :
          (Array.isArray(results.sql_results) ? JSON.stringify(results.sql_results) : '[]'),
        chats: results.chats || [],
        messages: results.messages || []
      };
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        console.error('Axios Error full response:', error.response);

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
