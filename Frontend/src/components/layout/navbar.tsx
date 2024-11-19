import {Box, Button} from "@mui/material";
import {Outlet, useNavigate} from "react-router-dom";
import './navbar.css';


export default function Navbar() {
    const navigate = useNavigate();
    const handleTests = () => { navigate("/tests"); }
    const handleGraph = () => { navigate("/graph-drawing"); }

    return (
        <Box>
            <Box className='nav-bar'>
                <Button
                    className='nav-bar-button'
                    sx={{
                        color: "primary.contrastText",
                        fontSize: 'medium'
                    }}
                    onClick={() => handleTests()}>
                    Tests
                </Button>
                <Button
                    className='nav-bar-button'
                    sx={{
                        color: "primary.contrastText",
                        fontSize: "medium"
                    }}
                    onClick={() => handleGraph()}>
                    Graph
                </Button>
            </Box>
            <Outlet/>
        </Box>
    )
}