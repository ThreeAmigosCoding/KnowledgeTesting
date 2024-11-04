import { Box, Typography, Card, CardContent } from "@mui/material";
import './tests.css';
import api from "../../config/axios-config.tsx";
import {useEffect, useState} from "react";
import {Question, Test} from "../../model/models.tsx";
import {useParams} from "react-router-dom";

export default function TestOverview() {

    const { id } = useParams<{ id: string; }>();
    const [questions, setQuestions] = useState<Question[]>([]);
    const [test, setTest] = useState<Test>();

    useEffect(() => {
        fetchTest().then(() => {})
        fetchQuestions().then(() => {})
    }, []);

    const fetchQuestions = async () => {
        try {
            const test_id = id?.valueOf()
            const response = await api.get<Question[]>(`test-questions`, {
                params: { test_id }
            });
            if (response.status === 200) {
                setQuestions(response.data);
            }
        }
        catch (error) {
            alert(error)
        }
    }

    const fetchTest = async () => {
        try {
            const test_id = id?.valueOf()
            const response = await api.get<Test>(`test`, {
                params: { test_id }
            });
            if (response.status === 200) {
                setTest(response.data);
            }
        }
        catch (error) {
            alert(error)
        }
    }

    return (
        <Box className='main-container'>
            <Box className='content'>
                <Typography variant='h1'>{test?.title}</Typography>
                <Box className="questions-container">
                    {questions.map((question) => (
                        <Card key={question.id} className="question-container">
                            <CardContent className="question-card-content">
                                <Typography variant="h2">{question.text}</Typography>
                                <Box className="answers-container">
                                    {question.answers.map((answer) => (
                                        <Typography
                                            sx = {{ color: answer.is_correct ? 'success.main' : '#1A1A1A' }}
                                            variant="h3">
                                            • {answer.text}
                                        </Typography>
                                    ))}
                                </Box>
                            </CardContent>
                        </Card>
                    ))}
                </Box>
            </Box>
        </Box>
    )
}