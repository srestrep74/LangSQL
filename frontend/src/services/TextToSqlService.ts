import type { ApiResponse, QueryResults } from '@/interfaces/ApiResponse';
import axios from 'axios';

const API_URL: string = import.meta.env.VITE_API_URL as string;

class TextToSqlService {
    async proccessQuery(query: string): Promise<QueryResults> {
        try {
            const response = await axios.post<ApiResponse>(`${API_URL}/text-to-sql/process_query`, { 
                user_input: query,
                schema_name: 'inventory'
            });
            return response.data.data.results;
        } catch (error) {
            console.error(error);
            throw new Error('Error processing query');
        }
    }
}

export default new TextToSqlService();