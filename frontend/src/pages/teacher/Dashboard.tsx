import { Button, Typography } from '@mui/material';
import { useAuth } from '../../hooks/useAuth';

const TeacherDashboard = () => {
    const { logout } = useAuth();
    return (
        <div>
            <Typography variant="h4">Teacher Dashboard</Typography>
            <Typography>Manage attendance, results, etc.</Typography>
            <Button onClick={logout} variant="outlined">Logout</Button>
        </div>
    );
};

export default TeacherDashboard;