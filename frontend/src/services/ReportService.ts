import api, { isAxiosError } from '@/services/ApiBase';
import type { GraphRequest, ReportResponse, DBStructure } from '@/interfaces/ReportInterfaces';
import type { ApiErrorResponse } from '@/interfaces/ApiErrorResponse';
import { dbCredentialsStore } from '@/store/dbCredentialsStore';

class ReportService {
  async generateCharts(graphRequests: GraphRequest[]): Promise<ReportResponse> {
    try {
      const credentials = dbCredentialsStore.credentials;
      if (!credentials) {
        throw new Error('No database credentials found');
      }

      const response = await api.post<ReportResponse>('/reports/generate-charts', {
        graph_requests: graphRequests,
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

      return response.data;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;

        const errorMessage = errorData?.message
          || error.message
          || 'Error generating charts';

        console.error('API Error:', {
          status: error.response?.status,
          message: errorMessage,
          data: error.response?.data
        });

        throw new Error(errorMessage);
      }

      console.error('Unknown error:', error);
      throw new Error('An unknown error occurred while generating charts');
    }
  }

  async getDatabaseStructure(): Promise<DBStructure> {
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

      return response.data.data.db_structure as DBStructure;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        const errorMessage = errorData?.message || error.message || 'Error fetching database structure';
        console.error('API Error:', {
          status: error.response?.status,
          message: errorMessage,
          data: error.response?.data
        });

        throw new Error(errorMessage);
      }

      console.error('Unknown error:', error);
      throw new Error('An unknown error occurred while fetching database structure');
    }
  }
}

export default new ReportService();
