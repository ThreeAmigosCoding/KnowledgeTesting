import {createTheme, CssBaseline, ThemeProvider} from "@mui/material";
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import './index.css'
import TestsOverview from "./pages/teacher/tests-overview.tsx";
import ReactDOM from 'react-dom/client'
import TestOverview from "./pages/teacher/test-overview.tsx";

const theme = createTheme({
    palette: {
        primary: {
            main: "#3C493F",
            light: "#7E8D85",
            contrastText: "#F5F5F5"
        },
        secondary: {
            main: "#7E8D85",
            contrastText: '#1A1A1A'
        },
        error: {
            main: "#DD3636"
        },
        success: {
            main: "#3FCB4D"
        },
        background: {
            default: "#F0F7F4",
        }
    },
    typography: {
        h1: {
            fontFamily: 'Poppins, sans-serif',
            fontSize: '52px',
            fontWeight: 'normal',
            color: "#1A1A1A",
            textAlign: 'center'
        },
        h2: {
            fontFamily: 'Poppins, sans-serif',
            fontSize: 'xxx-large',
            color: "#1A1A1A",
        },
        h3: {
            fontFamily: 'Poppins, sans-serif',
            fontSize: 'xx-large',
            color: "#1A1A1A",
        },
        h4: {
            fontFamily: 'Poppins, sans-serif',
            fontSize: 'x-large',
            color: "#1A1A1A",
        },
        h5: {
            fontFamily: 'Poppins, sans-serif',
            fontSize: 'larger',
            color: "#1A1A1A",
        },
        allVariants: {
            fontFamily: 'Poppins, sans-serif',
            color: "#1A1A1A",
        },
    },
    components: {
        MuiTextField: {
            styleOverrides: {
                root: {
                    '& .MuiInputBase-input': {
                        color: '#F5F5F5',
                    },
                    '& .MuiInputLabel-root': {
                        color: '#F5F5F5',
                    },
                    '& .MuiFormHelperText-root': {
                        color: '#F5F5F5',
                    },
                },
            },
        },
    },
});

const router = createBrowserRouter([
    { path:"/tests", element: <TestsOverview/> },
    { path:"/test/:id", element: <TestOverview/> },
])

ReactDOM.createRoot(document.getElementById('root')!).render(
    <ThemeProvider theme={theme} >
        <CssBaseline/>
        <RouterProvider router={router}/>
    </ThemeProvider>
)