import { useState } from 'react';
import { TextField, Button, Select, MenuItem, FormControl, InputLabel, Typography, Alert } from '@mui/material';
import { useAuth } from '../../hooks/useAuth';
import { registerUser } from '../../api/auth';

const AdminDashboard = () => {
    const { logout, token } = useAuth();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('STUDENT');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    const handleRegister = async () => {
        if (!token) return;
        try {
            await registerUser({ username, password, role }, token);
            setMessage('User registered successfully!');
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Registration failed');
        }
    };

    return (
        <div style={{ padding: 20 }}>
            <Typography variant="h4">Admin Dashboard - RPS School</Typography>
            <Button onClick={logout} variant="outlined">Logout</Button>
            <Typography variant="h6" style={{ marginTop: 20 }}>Register New User</Typography>
            {error && <Alert severity="error">{error}</Alert>}
            {message && <Alert severity="success">{message}</Alert>}
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
            <Button onClick={handleRegister} variant="contained" fullWidth>Register User</Button>
        </div>
    );
};

export default AdminDashboard;