import type { DBCredentials } from './DBCredentials';

export interface GraphRequest {
  table: string;
  columns: string[];
}

export interface ChartData {
  chart_type?: string;
  type?: string;
  data: any;
  additional_info: any;
}

export interface ReportResponse {
  [key: string]: ChartData[] | string;
}

export interface ReportRequestPayload {
  graph_requests: GraphRequest[];
  connection: {
    db_type: string;
    username: string;
    password: string;
    host: string;
    port: number;
    database_name: string;
    schema_name?: string;
  };
}

export interface DBColumn {
  name: string;
  type: string;
  nullable: boolean;
  primary_key: boolean;
}

export interface ForeignKey {
  column: string;
  references: string;
  referenced_column: string;
}

export interface TableStructure {
  columns: DBColumn[];
  foreign_keys: ForeignKey[];
}

export interface DBStructure {
  [tableName: string]: TableStructure;
}
