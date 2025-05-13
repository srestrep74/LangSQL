export interface SqlResultItem {
    name: string;
    [key: string]: any;
}

export interface ChatData {
    user_id: string;
    messages?: ChatMessage[];
}

export interface ChatInfo {
    chat_id: string;
    title: string;
}

export interface ChatMessage {
    role: number;
    message: string;
    timestamp: string;
}

export interface QueryResults {
    header: string;
    sql_results: string;
    chat_id: string;
    sql_query: string;
    chats: ChatInfo[];
    messages: ChatMessage[];
}

export interface ChatData {
    user_id: string;
    messages: Message[];
}

export interface Message {
    role: number;
    message: string;
    timestamp: string;
}

export interface ApiResponse {
    status: string;
    message: string;
    data?: {
        results: QueryResults;
    };
    details?: {
        error: string;
        [key: string]: any;
    };
    status_code: number;
}
