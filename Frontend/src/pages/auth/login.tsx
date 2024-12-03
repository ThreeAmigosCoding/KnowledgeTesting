import {Box, Typography} from "@mui/material";
import LoginForm from "../../components/auth/login-form.tsx";
import './auth.css';

export function Login() {
    return (
        <Box className="login-container">
            <Typography id="logo" variant="h1">Knowledge Testing</Typography>
            <LoginForm/>
        </Box>
    )
}