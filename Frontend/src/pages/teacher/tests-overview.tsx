import {Box, Typography, Card, CardContent, Button} from "@mui/material";
import './tests.css';
import api from "../../config/axios-config.tsx";
import {useEffect, useState} from "react";
import {Test} from "../../model/models.tsx";
import {useNavigate} from "react-router-dom";

export default function TestsOverview() {

    const navigate = useNavigate();
    const [tests, setTests] = useState<Test[]>([]);

    useEffect(() => {
        fetchTests().then(() => {})
    }, []);

    const fetchTests = async () => {
        try {
            const author_id = 1;
            const response = await api.get<Test[]>(`tests`, {
                params: { author_id }
            });
            if (response.status === 200) {
                setTests(response.data);
            }
        }
        catch (error) {
            alert(error)
        }
    }

    const openTest = (testId: number) => {
        navigate(`/test/${testId}`);
    };

    const openTestCreate = () => {
        navigate(`/test-create`);
    };

    return (
        <Box className='main-container'>
            <Box className='content'>
                <Typography variant='h1'>Tests</Typography>
                <Button
                    sx={{
                        fontSize: "x-large",
                        textTransform: "capitalize",
                        maxWidth: "300px"
                    }}
                    id="open-test-create"
                    variant="contained" color="primary"
                    onClick={openTestCreate}>
                    Create Test
                </Button>
                <Box className="tests-container">
                    {tests.map((test) => (
                        <Card
                            key={test.id}
                            className="test-card"
                            onClick={() => openTest(test.id)}>
                            <CardContent className="test-card-content">
                                <Typography variant="h2">{test.title}</Typography>
                                <Typography variant="h3">
                                    Author: {test.author.first_name} {test.author.last_name}
                                </Typography>
                                <Typography variant="h4">
                                    Questions: {test.questions.length}
                                </Typography>
                            </CardContent>
                        </Card>
                    ))}
                </Box>
            </Box>
        </Box>
    )
}