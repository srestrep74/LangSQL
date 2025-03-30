export type DatabaseType = 'mysql' | 'postgresql';

export interface DBCredentials {
  dbType: DatabaseType;
  host: string;
  port: number;
  user: string;
  password: string;
  db_name: string;
}