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

      if (response.data.status === 'error') {
        throw new Error(response.data.details?.error || response.data.message || 'Unknown API error');
      }

      if (!response.data?.data?.results) {
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
        const errorMessage = errorData?.message || error.message || 'Error processing query';
        throw new Error(errorMessage);
      }

      throw new Error('An unknown error occurred while processing your query');
    }
  }

  async deleteChat(chatId: string): Promise<boolean> {
    try {
      const credentials = dbCredentialsStore.credentials;
      if (!credentials) {
        throw new Error('No database credentials found');
      }

      const response = await api.delete<ApiResponse>('/text-to-sql/chat', {
        data: {
          chat_id: chatId,
          user_id: userStore.user?.id || '',
          connection: {
            db_type: credentials.dbType,
            username: credentials.user,
            password: credentials.password,
            host: credentials.host,
            port: credentials.port,
            database_name: credentials.db_name,
            schema_name: credentials.schema_name
          }
        }
      });

      if (response.data.status === 'error') {
        throw new Error(response.data.details?.error || response.data.message || 'Unknown API error');
      }

      return true;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        const errorMessage = errorData?.message || error.message || 'Error deleting chat';
        throw new Error(errorMessage);
      }

      throw new Error('An unknown error occurred while deleting the chat');
    }
  }

  async renameChat(chatId: string, newTitle: string): Promise<boolean> {
    try {
      const credentials = dbCredentialsStore.credentials;
      if (!credentials) {
        throw new Error('No database credentials found');
      }

      const response = await api.put<ApiResponse>('/text-to-sql/chat/rename', {
        chat_id: chatId,
        user_id: userStore.user?.id || '',
        new_title: newTitle,
        connection: {
          db_type: credentials.dbType,
          username: credentials.user,
          password: credentials.password,
          host: credentials.host,
          port: credentials.port,
          database_name: credentials.db_name,
          schema_name: credentials.schema_name
        }
      });

      if (response.data.status === 'error') {
        throw new Error(response.data.details?.error || response.data.message || 'Unknown API error');
      }

      if (response.data.status === 'error') {
        throw new Error(response.data.details?.error || response.data.message || 'Unknown API error');
      }

      return true;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        const errorMessage = errorData?.message || error.message || 'Error renaming chat';
        throw new Error(errorMessage);
      }

      throw new Error('An unknown error occurred while renaming the chat');
    }
  }

  async deleteChat(chatId: string): Promise<boolean> {
    try {
      const credentials = dbCredentialsStore.credentials;
      if (!credentials) {
        throw new Error('No database credentials found');
      }

      const response = await api.delete<ApiResponse>('/text-to-sql/chat', {
        data: {
          chat_id: chatId,
          user_id: userStore.user?.id || '',
          connection: {
            db_type: credentials.dbType,
            username: credentials.user,
            password: credentials.password,
            host: credentials.host,
            port: credentials.port,
            database_name: credentials.db_name,
            schema_name: credentials.schema_name
          }
        }
      });

      if (response.data.status === 'error') {
        throw new Error(response.data.details?.error || response.data.message || 'Unknown API error');
      }

      return true;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        const errorMessage = errorData?.message || error.message || 'Error deleting chat';
        throw new Error(errorMessage);
      }

      throw new Error('An unknown error occurred while deleting the chat');
    }
  }

  async renameChat(chatId: string, newTitle: string): Promise<boolean> {
    try {
      const credentials = dbCredentialsStore.credentials;
      if (!credentials) {
        throw new Error('No database credentials found');
      }

      const response = await api.put<ApiResponse>('/text-to-sql/chat/rename', {
        chat_id: chatId,
        user_id: userStore.user?.id || '',
        new_title: newTitle,
        connection: {
          db_type: credentials.dbType,
          username: credentials.user,
          password: credentials.password,
          host: credentials.host,
          port: credentials.port,
          database_name: credentials.db_name,
          schema_name: credentials.schema_name
        },
        chat_data: chatData
      });

      if (response.data.status === 'error') {
        throw new Error(response.data.details?.error || response.data.message || 'Unknown API error');
      }

      return true;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        const errorMessage = errorData?.message || error.message || 'Error renaming chat';
        throw new Error(errorMessage);
      }

      throw new Error('An unknown error occurred while renaming the chat');
    }
  }
}

export default new TextToSqlService();