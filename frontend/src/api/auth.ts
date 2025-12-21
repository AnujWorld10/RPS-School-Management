import axios from 'axios';

interface LoginData {
    username: string;
    password: string;
    role: string;
}

export interface User {
    id: number;
    username: string;
    role: string;
    is_active: boolean;
}

const api = axios.create({
    baseURL: '', // IMPORTANT: empty because Vite proxy handles it
    headers: {
        'Content-Type': 'application/json',
    },
});

// LOGIN
export const loginUser = async (data: LoginData) => {
    const response = await api.post('/api/v1/auth/login', data);
    return response.data;
};

// REGISTER
export const registerUser = async (data: LoginData, token?: string) => {
    const response = await api.post(
        '/api/v1/auth/register',
        data,
        token
            ? { headers: { Authorization: `Bearer ${token}` } }
            : undefined
    );
    return response.data;
};
