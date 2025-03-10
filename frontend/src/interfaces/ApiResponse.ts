export interface SqlResultItem {
    name: string;
}

export interface QueryResults {
    header: string;
    sql_results: string;
}

export interface ApiResponse {
    status: string;
    message: string;
    data: {
        results: QueryResults;
    };
    status_code: number;
}