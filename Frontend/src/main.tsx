import {createTheme, CssBaseline, ThemeProvider} from "@mui/material";
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import './index.css'
import TestsOverview from "./pages/tests/tests-overview.tsx";
import ReactDOM from 'react-dom/client'
import TestOverview from "./pages/tests/test-overview.tsx";
import GraphDrawing from "./pages/graphs/graph-drawing.tsx";
import Navbar from "./components/layout/navbar.tsx";
import TestCreate from "./pages/tests/test-create.tsx";
import {UserProvider} from "./context/user-context.tsx";
import GraphsComparison from "./pages/graphs/graphs-comparison.tsx";
import ResultsOverview from "./pages/results/results-overview.tsx";
import ResultOverview from "./pages/results/result-overview.tsx";


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
            fontSize: 'xx-large',
            fontWeight: 'normal',
            color: "#1A1A1A",
        },
        h2: {
            fontFamily: 'Poppins, sans-serif',
            fontSize: 'x-large',
            color: "#1A1A1A",
        },
        h3: {
            fontFamily: 'Poppins, sans-serif',
            fontSize: 'larger',
            color: "#1A1A1A",
        },
        h4: {
            fontFamily: 'Poppins, sans-serif',
            fontSize: 'large',
            color: "#1A1A1A",
        },
        h5: {
            fontFamily: 'Poppins, sans-serif',
            fontSize: 'medium',
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
                        color: '#1A1A1A',
                    },
                    '& .MuiInputLabel-root': {
                        color: '#1A1A1A',
                    },
                    '& .MuiFormHelperText-root': {
                        color: '#1A1A1A',
                    },
                },
            },
        },
    },
});

const router = createBrowserRouter([
    { path:"/", element: <Navbar/>,
        children: [
            { path:"/", element: <TestsOverview/> },
            { path:"/tests", element: <TestsOverview/> },
            { path:"/test/:id", element: <TestOverview/> },
            { path:"/graph-drawing", element: <GraphDrawing/>},
            { path:"/test-create", element: <TestCreate/>},
            { path:"/graphs-comparison/:id", element: <GraphsComparison/> },
            { path:"/results", element: <ResultsOverview/> },
            { path:"/result/:id", element: <ResultOverview/> },
        ]}

])

ReactDOM.createRoot(document.getElementById('root')!).render(
    <ThemeProvider theme={theme} >
        <UserProvider>
            <CssBaseline/>
            <RouterProvider router={router}/>
        </UserProvider>
    </ThemeProvider>
)