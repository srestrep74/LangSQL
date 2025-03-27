import type { DBCredentials } from "./DBCredentials";

export interface User {
    name: string;
    email: string;
  }
  
  export interface UserCreate extends User {
    password: string;
    main_credentials: DBCredentials;
    credentials: DBCredentials[];
    queries?: string[];
    alerts?: string[];
  }