import {useNavigate} from "react-router-dom";
import {useState} from "react";
import * as yup from 'yup'
import {useFormik} from "formik";
import api from "../../config/axios-config.tsx";
import {Box, Button, IconButton, InputAdornment, TextField, Typography} from "@mui/material";
import {Visibility, VisibilityOff} from "@mui/icons-material";

export default function RegistrationForm (){

    const navigate = useNavigate();

    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const handleClickShowPassword = () => setShowPassword(!showPassword);
    const handleClickShowConfirmPassword = () => setShowConfirmPassword(!showConfirmPassword);

    const handleLogin = () => {
        navigate('/login')
    }

    const validationSchema = yup.object({
        first_name: yup
            .string()
            .required('Name is required.'),
        last_name: yup
            .string()
            .required('Surname is required.'),
        email: yup
            .string()
            .email('Enter a valid email')
            .required('Email is required/'),
        password: yup
            .string()
            .min(8, 'Password should contain at least 8 characters.')
            .matches(
                /^(?=.*[A-Za-z])(?=.*\d)/,
                'Password must contain numbers and letters.'
            )
            .required('Password is required.'),
        confirmPassword: yup
            .string()
            .oneOf([yup.ref('password'), undefined], 'Passwords must match.')
            .required('Confirm Password is required.'),

    });

    const formik = useFormik({
        initialValues: {
            first_name: '',
            last_name: '',
            email: '',
            password: '',
            confirmPassword: '',
            role: 'student'
        },
        validationSchema: validationSchema,
        onSubmit: async (values) => {
            try {
                const response = await api.post('register', values);
                if (response.status === 201) {
                    alert("Registration successful");
                    navigate('/login')

                }
            } catch (error) {
                console.error('Registration failed:', error);
                alert('Error while registering');
            }
        },    });


    return (
        <div id={"form-container"} style={{width: "50%", padding: "0 10%"}}>
            <Typography variant="h1">Register</Typography>
            <form onSubmit={formik.handleSubmit}>
                <TextField
                    fullWidth
                    id="first_name"
                    name="first_name"
                    label="First Name"
                    value={formik.values.first_name}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    error={formik.touched.first_name && Boolean(formik.errors.first_name)}
                    helperText={formik.touched.first_name && formik.errors.first_name}
                />
                <TextField
                    fullWidth
                    id="last_name"
                    name="last_name"
                    label="Last Name"
                    value={formik.values.last_name}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    error={formik.touched.last_name && Boolean(formik.errors.last_name)}
                    helperText={formik.touched.last_name && formik.errors.last_name}
                />
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
                                    {showPassword ? <Visibility /> : <VisibilityOff />}
                                </IconButton>
                            </InputAdornment>
                        )
                    }}/>
                <TextField
                    fullWidth
                    id="confirmPassword"
                    name="confirmPassword"
                    label="Confirm password"
                    type={showConfirmPassword ? 'text' : 'password'}
                    value={formik.values.confirmPassword}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    error={formik.touched.confirmPassword && Boolean(formik.errors.confirmPassword)}
                    helperText={formik.touched.confirmPassword && formik.errors.confirmPassword}
                    InputProps={{
                        endAdornment: (
                            <InputAdornment position="end">
                                <IconButton
                                    aria-label="toggle confirm password visibility"
                                    onClick={handleClickShowConfirmPassword}
                                >
                                    {showConfirmPassword ? <Visibility /> : <VisibilityOff />}
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
                    Register
                </Button>

            </form>
            <Box sx={{display: "flex", flexDirection: "column", alignItems: "center", textAlign: "center"}}>
                <Typography variant="h4">Already have an account? <br/>
                    <span onClick={handleLogin}>Login</span>
                </Typography>
            </Box>
        </div>
    )
}