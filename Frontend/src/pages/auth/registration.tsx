import {Box, Typography} from "@mui/material";
import RegistrationForm from "../../components/auth/registration-form.tsx";
import './auth.css';

export default function Registration() {
    return (
        <Box className="registration-container">
            <Typography id="logo" variant="h1">Knowledge testing</Typography>
            <RegistrationForm/>
        </Box>
    )
}