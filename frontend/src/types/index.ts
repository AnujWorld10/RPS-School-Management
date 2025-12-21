export interface User {
    id: number;
    username: string;
    role: string;
    is_active: boolean;
}

export interface LoginData {
    username: string;
    password: string;
    role: string;
}