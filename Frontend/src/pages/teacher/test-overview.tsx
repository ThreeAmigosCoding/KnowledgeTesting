import {Box, Typography, Card, CardContent, FormControlLabel, Checkbox, Radio, Button, RadioGroup} from "@mui/material";
import './tests.css';
import api from "../../config/axios-config.tsx";
import {useEffect, useState} from "react";
import {Question, Test} from "../../model/models.tsx";
import {useParams} from "react-router-dom";
import {useUser} from "../../context/user-context.tsx";

export default function TestOverview() {

    const { id } = useParams<{ id: string; }>();
    const [questions, setQuestions] = useState<Question[]>([]);
    const [test, setTest] = useState<Test>();

    const [answers, setAnswers] = useState<Record<number, string[]>>({});


    const {user, setUser} = useUser();

    useEffect(() => {
        fetchTest().then(() => {});
        fetchQuestions().then(() => {});
        setUser({
            email: "pera@mail.com",
            first_name: "Pera",
            id: 0,
            last_name: "Peric",
            password: "petar123",
            role: "student"
        });
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

    const handleAnswerChange = (questionId: number | undefined, answerText: string, isChecked: boolean) => {
        if (questionId) {
            setAnswers((prev) => {
                const updated = { ...prev };
                if (!updated[questionId]) {
                    updated[questionId] = [];
                }

                if (isChecked) {
                    updated[questionId].push(answerText);
                } else {
                    updated[questionId] = updated[questionId].filter((a) => a !== answerText);
                }
                return updated;
            });
        }

    };

    const handleSingleAnswerChange = (questionId: number | undefined, answerText: string) => {
        if (questionId) {
            setAnswers((prev) => ({
                ...prev,
                [questionId]: [answerText],
            }));
        }
    };

    const handleSubmit = () => {
        console.log("Submitted answers:", answers);
        alert("Test submitted successfully!");
    };

    return (
        <Box className='main-container'>
            <Box className='content'>
                <Typography variant='h2' sx={{textAlign: 'center'}}>{test?.title}</Typography>
                <Box className="questions-container">
                    {questions.map((question) => (
                        <Card key={question.id} className="question-container">
                            <CardContent className="question-card-content">
                                <Typography variant="h4">{question.text}</Typography>
                                <Box className="answers-container">
                                    {user && user.role === "teacher" ? (
                                        question.answers.map((answer) => (
                                            <Typography
                                                key={answer.id}
                                                sx={{
                                                    color: answer.is_correct ? "success.main" : "#1A1A1A",
                                                }}
                                                variant="h3"
                                            >
                                                • {answer.text}
                                            </Typography>
                                        ))
                                    ) : question.is_multichoice ? (
                                        // Multiple choice (checkbox)
                                        question.answers.map((answer) => (
                                            <FormControlLabel
                                                key={answer.id}
                                                control={
                                                    <Checkbox
                                                        onChange={(e) =>
                                                            handleAnswerChange(question.id, answer.text, e.target.checked)
                                                        }
                                                    />
                                                }
                                                label={answer.text}
                                            />
                                        ))
                                    ) : (
                                        // Single choice (radio button) with RadioGroup
                                        <RadioGroup
                                            key={question.id}
                                            onChange={(e) =>
                                                handleSingleAnswerChange(question.id, e.target.value)
                                            }
                                        >
                                            {question.answers.map((answer) => (
                                                <FormControlLabel
                                                    key={answer.id}
                                                    value={answer.text}
                                                    control={<Radio />}
                                                    label={answer.text}
                                                />
                                            ))}
                                        </RadioGroup>
                                    )}
                                </Box>
                            </CardContent>
                        </Card>
                    ))}
                    {user && user.role === "student" && (
                        <Button
                            variant="contained"
                            color="primary"
                            fullWidth
                            sx={{ marginTop: 2 }}
                            onClick={handleSubmit}
                        >
                            Submit Test
                        </Button>
                    )}
                </Box>
            </Box>
        </Box>
    )
}