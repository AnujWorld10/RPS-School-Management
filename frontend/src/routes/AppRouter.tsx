import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from '../auth/Login';
import AdminDashboard from '../pages/admin/Dashboard';
import TeacherDashboard from '../pages/teacher/Dashboard';
import StudentDashboard from '../pages/student/Dashboard';

const AppRouter = () => (
    <Router>
        <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/teacher" element={<TeacherDashboard />} />
            <Route path="/student" element={<StudentDashboard />} />
        </Routes>
    </Router>
);

export default AppRouter;