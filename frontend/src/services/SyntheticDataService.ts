import api, { isAxiosError } from '@/services/ApiBase';
import type { ApiErrorResponse } from '@/interfaces/ApiErrorResponse';
import { dbCredentialsStore } from '@/store/dbCredentialsStore';

class SyntheticDataService {
  async getDatabaseSchema(): Promise<any> {
    try {
      const credentials = dbCredentialsStore.credentials;
      if (!credentials) {
        throw new Error('No database credentials found');
      }

      const response = await api.post('/queries/db_structure/', {
        db_type: credentials.dbType,
        username: credentials.user,
        password: credentials.password,
        host: credentials.host,
        port: credentials.port,
        database_name: credentials.db_name,
        schema_name: credentials.schema_name
      });

      if (!response.data) {
        throw new Error('Empty response from server');
      }

      return response.data.data.db_structure;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;

        const errorMessage = errorData?.message
          || error.message
          || 'Failed to load database schema';

        console.error('API Error:', {
          status: error.response?.status,
          message: errorMessage,
          data: error.response?.data
        });

        throw new Error(errorMessage);
      }

      console.error('Unknown error:', error);
      throw new Error('An unexpected error occurred while loading database schema');
    }
  }

  async postSyntheticData(iterations: number): Promise<any> {
    try {

      const credentials = dbCredentialsStore.credentials;
      if (!credentials) {
        throw new Error('No database credentials found');
      }

      const response = await api.post('/text-to-sql/generate_synthetic_data', {
        iterations: iterations,
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
