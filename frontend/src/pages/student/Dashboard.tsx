import { Button, Typography } from '@mui/material';
import { useAuth } from '../../hooks/useAuth';

const StudentDashboard = () => {
    const { logout } = useAuth();
    return (
        <div>
            <Typography variant="h4">Student Dashboard</Typography>
            <Typography>View results, attendance, etc.</Typography>
            <Button onClick={logout} variant="outlined">Logout</Button>
        </div>
    );
};

export default StudentDashboard;