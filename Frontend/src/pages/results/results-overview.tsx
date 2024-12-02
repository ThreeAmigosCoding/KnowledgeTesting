import {Box, Card, CardContent, Typography} from "@mui/material";
import './results.css'
import {useEffect, useState} from "react";
import {Result} from "../../model/models.tsx";
import api from "../../config/axios-config.tsx";
import {formatTimestamp} from "../../utils/converter.tsx";
import {useNavigate} from "react-router-dom";


export default function ResultsOverview() {

    const navigate = useNavigate();
    const [results, setResults] = useState<Result[]>([]);

    useEffect(() => {
        fetchResults().then(() => {})
    }, []);

    const fetchResults = async () => {
        try {
            const studentId = 2;
            const response = await api.get<Result[]>(`get-results`, {
                params: { studentId: studentId }
            });
            if (response.status === 200) {
                setResults(response.data);
            }
        }
        catch (error) {
            alert(error)
        }
    }

    const openResult = (resultId: number) => {
        navigate(`/result/${resultId}`);
    };

    return (
        <Box className='main-container'>
            <Box className='content'>
                <Typography variant='h1' sx={{textAlign: 'center'}}>Results</Typography>
                <Box className="results-container">
                    {results.map((result) => (
                        <Card
                            key={result.id}
                            className="result-card"
                            onClick={() => openResult(result.id as number)}>
                            <CardContent className="result-card-content">
                                <Typography variant="h2">{result.test.title}</Typography>
                                <Typography variant="h3">
                                    Author: {result.test?.author?.first_name} {result.test?.author?.last_name}
                                </Typography>
                                <Typography variant="h4">
                                    Questions: {result.test.questions.length}
                                </Typography>
                                <Typography variant="h5">
                                    {formatTimestamp(result.timestamp)}
                                </Typography>
                            </CardContent>
                        </Card>
                    ))}
                </Box>
            </Box>
        </Box>
    )
}