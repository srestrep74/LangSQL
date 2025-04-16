import api, { isAxiosError } from '@/services/ApiBase';
import type { ApiErrorResponse } from '@/interfaces/ApiErrorResponse';
import { userStore } from '@/store/userStore';
import { dbCredentialsStore } from '@/store/dbCredentialsStore';

class AlertService {
  async getAlerts(): Promise<any> {
    try {
      const user = userStore.user;
      if (!user) {
        throw new Error('User is not logged in');
      }

      const dbCredentials = dbCredentialsStore.credentials;

      if (!dbCredentials) {
        throw new Error('No database credentials found');
      }
  
      const response = await api.get<any>('/alerts', {
        params: {
          user_id: String(user.id)
        }
      });
  
      if (response.data?.status !== 'success') {
        throw new Error(response.data?.message || 'Failed to fetch alerts');
      }      
  
      return response.data;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        const errorMessage = errorData?.message 
          || error.message 
          || 'Failed to fetch alerts';
        console.error('Alert Fetch Error:', {
          status: error.response?.status,
          message: errorMessage,
          data: error.response?.data
        });
        throw new Error(errorMessage);
      }
  
      console.error('Unknown error:', error);
      throw new Error('An unexpected error occurred while fetching alerts');
    }
  }

  async getAlert(alertId: string): Promise<any> {
    try {
      const user = userStore.user;
      if (!user) {
        throw new Error('User is not logged in');
      }
  
      const response = await api.get<any>(`/alerts/${alertId}`)
  
      if (response.data?.status !== 'success') {
        throw new Error(response.data?.message || 'Failed to fetch alert');
      }      
  
      return response.data;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        const errorMessage = errorData?.message 
          || error.message 
          || 'Failed to fetch alert';
        console.error('Alert Fetch Error:', {
          status: error.response?.status,
          message: errorMessage,
          data: error.response?.data
        });
        throw new Error(errorMessage);
      }
  
      console.error('Unknown error:', error);
      throw new Error('An unexpected error occurred while fetching alerts');
    }
  }

  async deleteAlert(alertId: string): Promise<any> {
    try {
      const user = userStore.user;
      if (!user) {
        throw new Error('User is not logged in');
      }
  
      const response = await api.delete<any>(`/alerts/${alertId}`, {
        params: {
          user_id: String(user.id)
        }
      });
  
      if (response.data?.status !== 'success') {
        throw new Error(response.data?.message || 'Failed to delete alert');
      }      
  
      return response.data;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        const errorMessage = errorData?.message 
          || error.message 
          || 'Failed to delete alert';
        console.error('Alert Deletion Error:', {
          status: error.response?.status,
          message: errorMessage,
          data: error.response?.data
        });
        throw new Error(errorMessage);
      }
  
      console.error('Unknown error:', error);
      throw new Error('An unexpected error occurred while deleting the alert');
    }
  }

  async editAlert(alertId: string, formData: any): Promise<any> {
    try {
      const user = userStore.user;
      if (!user) {
        throw new Error('User is not logged in');
      }
  
      const dbCredentials = dbCredentialsStore.credentials;
  
      if (!dbCredentials) {
        throw new Error('No database credentials found');
      }
      
      const emails = typeof formData.notification_emails === 'string'
      ? formData.notification_emails.split(',').map((e: string) => e.trim())
      : formData.notification_emails;
    
      const dataToSend = {
        notification_emails: emails,
        prompt: formData.prompt,
        expiration_date: formData.expiration_date
      };    

      console.log('Data to send:', dataToSend);
  
      const response = await api.patch<any>(`/alerts/${alertId}`, dataToSend);
  
      if (response.data?.status !== 'success') {
        throw new Error(response.data?.message || 'Alert update failed');
      }      
  
      return response.data;
    } catch (error: unknown) {
      if (isAxiosError(error)) {
        const errorData = error.response?.data as ApiErrorResponse;
        const errorMessage = errorData?.message 
          || error.message 
          || 'Failed to update alert';
        console.error('Alert Update Error:', {
          status: error.response?.status,
          message: errorMessage,
          data: error.response?.data
        });
        throw new Error(errorMessage);
      }
  
      console.error('Unknown error:', error);
      throw new Error('An unexpected error occurred while updating the alert');
    }
  }

  async postCreateAlert(formData: any): Promise<any> {
    try {
      const user = userStore.user;
  
      if (!user) {
        throw new Error('User is not logged in');
      }
  
      const dbCredentials = dbCredentialsStore.credentials;
  
      if (!dbCredentials) {
        throw new Error('No database credentials found');
      }
  
      const dataToSend = {
        connection: {
          db_type: dbCredentials.dbType,
          username: dbCredentials.user,
          password: dbCredentials.password,
          host: dbCredentials.host,
          port: dbCredentials.port,
          database_name: dbCredentials.db_name,
          schema_name: dbCredentials.schema_name ?? null,
        },
        alert_data: {
          notification_emails: formData.notification_emails,
          prompt: formData.prompt,
          expiration_date: formData.expiration_date,
          sent: false,
          creation_date: new Date().toISOString(),
          sql_query: null,
          user: String(user.id)
        }
      };
  
      const response = await api.post<any>('/alerts/create', dataToSend);
      
      if (response.data?.status !== 'success') {
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