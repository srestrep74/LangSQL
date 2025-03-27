import type { UserResponse } from "./User";

export interface AuthUser {
    name: string;
    email: string;
  }
  
export interface AuthToken {
    access_token: string;
    token_type: string;
}

export interface AuthResponse {
    status: string;
    message: string;
    data: {
      access_token: string; 
      refresh_token: string;
      token_type: string;
      user: UserResponse;
    };
}