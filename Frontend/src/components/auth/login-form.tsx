import {useState} from "react";
import {useNavigate} from "react-router-dom";
import * as yup from 'yup'
import {useFormik} from "formik";
import api from "../../config/axios-config.tsx";
import {useUser} from "../../context/user-context.tsx";
import {userFromToken} from "../../services/auth-service.ts";
import {Box, Button, IconButton, InputAdornment, TextField, Typography} from "@mui/material";
import {Visibility, VisibilityOff} from "@mui/icons-material";
import "./login-registration-form.css";

export default function LoginForm (){

    const navigate = useNavigate()
    const [showPassword, setShowPassword] = useState(false);

    const {setUser} = useUser();


    const handleClickShowPassword = () => setShowPassword(!showPassword);

    const handleRegister = () => {
        navigate('/registration')
    }

    const validationSchema = yup.object({
        email: yup
            .string()
            .test('is-email', 'Enter a valid email', (value) => {
                if (value === 'admin') {
                    return true;
                }

                try {
                    yup.string().email().validateSync(value, { abortEarly: true });
                    return true;
                } catch {
                    return false;
                }
            })
            .required('Email is required.'),
        password: yup
            .string()
            .min(8, 'Password should contain at least 8 characters.')
            .required('Password is required.'),
    });

    const formik = useFormik({
        initialValues: {
            email: '',
            password: '',
        },
        validationSchema: validationSchema,
        onSubmit: async (values) => {
            try {
                const response = await api.post('login', values);
                if (response.status === 200) {
                    const { token } = response.data;
                    localStorage.setItem('token', token);
                    setUser(userFromToken(token));
                    navigate('/tests');
                }
            } catch (error) {
                console.error('Login failed:', error);
                alert("Login failed");
            }
        },
    });

    return (
        <div id={"form-container"} style={{width: "50%", padding: "0 10%"}}>
            <Typography variant="h1">Login</Typography>
            <form onSubmit={formik.handleSubmit}>
                <TextField
                    fullWidth
                    id="email"
                    name="email"
                    label="Email"
                    value={formik.values.email}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    error={formik.touched.email && Boolean(formik.errors.email)}
                    helperText={formik.touched.email && formik.errors.email}
                />
                <TextField
                    fullWidth
                    id="password"
                    name="password"
                    label="Password"
                    type={showPassword ? 'text' : 'password'}
                    value={formik.values.password}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    error={formik.touched.password && Boolean(formik.errors.password)}
                    helperText={formik.touched.password && formik.errors.password}
                    InputProps={{
                        endAdornment: (
                            <InputAdornment position="end">
                                <IconButton
                                    aria-label="toggle password visibility"
                                    onClick={handleClickShowPassword}
                                >
                                    {showPassword ? <Visibility/> : <VisibilityOff/>}
                                </IconButton>
                            </InputAdornment>
                        )
                    }}
                />
                <Button
                    sx={{
                        fontSize: "20px",
                        textTransform: "capitalize"
                    }}
                    variant="contained" color="primary" fullWidth type="submit">
                    Login
                </Button>
            </form>
            <Box sx={{display: "flex", flexDirection: "column", alignItems: "center", textAlign: "center"}}>
                <Typography variant="h4">Don't have an account? <br/>
                    <span onClick={handleRegister}>Get started</span>
                </Typography>
            </Box>
        </div>
    )
}