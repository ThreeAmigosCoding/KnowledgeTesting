import {Box, Button} from "@mui/material";
import {Outlet, useNavigate} from "react-router-dom";
import './navbar.css';
import {useUser} from "../../context/user-context.tsx";


export default function Navbar() {
    const navigate = useNavigate();
    const { setUser } = useUser();
    const handleTests = () => { navigate("/tests"); }
    const handleGraph = () => { navigate("/graph-drawing"); }
    const handleLogOut = () => {
        setUser(null);
        navigate("/login");
    }

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

                <Button
                    className='nav-bar-button'
                    sx={{
                        color: "primary.contrastText",
                        fontSize: "medium",
                        marginLeft: "auto"
                    }}
                    onClick={() => handleLogOut()}>
                    Log Out
                </Button>
            </Box>
            <Outlet/>
        </Box>
    )
}