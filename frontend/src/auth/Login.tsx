import { useState } from 'react';
import { TextField, Button, Select, MenuItem, FormControl, InputLabel, Alert } from '@mui/material';
import { useAuth } from '../hooks/useAuth';
import { loginUser } from '../api/auth';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('STUDENT');
    const [error, setError] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            const data = await loginUser({ username, password, role });
            login({ id: 1, username, role, is_active: true }, data.access_token);
            navigate(`/${role.toLowerCase()}`);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Login failed');
        }
    };

    return (
        <div style={{ padding: 20 }}>
            <h2>Login to RPS School System</h2>
            {error && <Alert severity="error">{error}</Alert>}
            <TextField label="Username" onChange={(e) => setUsername(e.target.value)} fullWidth />
            <TextField label="Password" type="password" onChange={(e) => setPassword(e.target.value)} fullWidth />
            <FormControl fullWidth>
                <InputLabel>Role</InputLabel>
                <Select value={role} onChange={(e) => setRole(e.target.value)}>
                    <MenuItem value="ADMIN">Admin</MenuItem>
                    <MenuItem value="TEACHER">Teacher</MenuItem>
                    <MenuItem value="STUDENT">Student</MenuItem>
                </Select>
            </FormControl>
            <Button onClick={handleLogin} variant="contained" fullWidth>Login</Button>
        </div>
    );
};

export default Login;