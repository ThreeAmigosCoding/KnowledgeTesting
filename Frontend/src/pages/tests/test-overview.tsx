import {Box, Typography, Card, CardContent, FormControlLabel, Checkbox, Radio, Button, RadioGroup} from "@mui/material";
import './tests.css';
import api from "../../config/axios-config.tsx";
import {useEffect, useState} from "react";
import {Question, Test, TestSubmission} from "../../model/models.tsx";
import {useNavigate, useParams} from "react-router-dom";
import {useUser} from "../../context/user-context.tsx";


export default function TestOverview() {

    const navigate = useNavigate();

    const { id } = useParams<{ id: string; }>();
    const [questions, setQuestions] = useState<Question[]>([]);
    const [test, setTest] = useState<Test>();

    const [answers, setAnswers] = useState<Record<number, number[]>>({});

    const {user} = useUser();

    const [canEdit, setCanEdit] = useState<boolean>(false);

    useEffect(() => {
        fetchTest().then(() => {});
    }, []);

    useEffect(() => {
        if (test) checkCanEdit().then(() => {});
    }, [test]);

    const checkCanEdit = async () => {
        try {
            const test_id = id?.valueOf()
            const response = await api.get(`check-results`, {
                params: { test_id }
            });
            if (response.status === 200) {
                setCanEdit(true);
            }
        }
        catch (error) {
            console.log(error);
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
                setQuestions(response.data.questions as Question[]);
            }
        }
        catch (error) {
            alert(error)
        }
    }

    const handleAnswerChange = (questionId: number | undefined, answerId: number | undefined, isChecked: boolean) => {
        if (questionId && answerId) {
            setAnswers((prev) => {
                const updated = { ...prev };
                if (!updated[questionId]) {
                    updated[questionId] = [];
                }

                if (isChecked) {
                    updated[questionId].push(answerId);
                } else {
                    updated[questionId] = updated[questionId].filter((id) => id !== answerId);
                }
                return updated;
            });
        }

    };

    const handleSingleAnswerChange = (questionId: number | undefined, answerId: number) => {
        if (questionId) {
            setAnswers((prev) => ({
                ...prev,
                [questionId]: [answerId]
            }));
        }
    };

    const handleSubmit = async () => {
        if (!test || !user || !test.id || user.role !== "student") return;

        const testSubmission: TestSubmission = {
            test_id: test.id,
            student_id: user.id,
            answers: Object.values(answers).flat()
        };

        try {
            const response = await api.post('/submit-test', testSubmission);
            if (response.status === 201) {
                alert("Test submitted successfully!");
            } else {
                alert("Failed to submit the test.");
            }
        } catch (error) {
            console.error("Error submitting test:", error);
            alert("There was an error submitting the test.");
        }
    };

    const openGraphsComparison = () => {
        navigate(`/graphs-comparison/${id}`);
    };

    const exportToQTI = async () => {
        try {
            const test_id = id?.valueOf();

            const response = await api.get(`export-test`, {
                params: { test_id },
                responseType: 'blob'
            });

            const blob = new Blob([response.data], { type: response.headers['content-type'] });

            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = `${test_id}-QTI.xml`;
            link.click();

            window.URL.revokeObjectURL(link.href);
        }
        catch (error) {
            alert(error)
        }
    }

    const openResults = () => {
        navigate(`/results/${id}`);
    };

    const openEditTest = () => {
        navigate(`/test-create/${id}`);
    };


    return (
        <Box className='main-container'>
            <Box className='content'>
                <Typography variant='h1' sx={{textAlign: 'center'}}>{test?.title}</Typography>
                {user && user.role === "teacher" && (

                    <Box className='top-buttons-container'>

                        <Button
                            variant="contained"
                            color="primary"
                            sx={{
                                fontSize: "medium",
                                textTransform: "capitalize",
                                maxWidth: "300px"
                            }}
                            onClick={openGraphsComparison}
                        >
                            Graphs
                        </Button>
                  
                        <Button
                            variant="contained"
                            color="primary"
                            sx={{
                                fontSize: "medium",
                                textTransform: "capitalize",
                                maxWidth: "300px"
                            }}
                            onClick={openResults}
                        >
                            Results

                        </Button>

                        <Button
                            variant="contained"
                            color="primary"
                            sx={{
                                fontSize: "medium",
                                textTransform: "capitalize",
                                maxWidth: "300px"
                            }}

                            onClick={exportToQTI}
                        >
                            Export to QTI
                        </Button>

                        <Button
                            variant="contained"
                            color="primary"
                            sx={{
                                fontSize: "medium",
                                textTransform: "capitalize",
                                maxWidth: "300px"
                            }}
                            disabled={!canEdit}
                            onClick={openEditTest}
                        >
                            Edit
                        </Button>
                    </Box>
                )}
                <Box className="questions-container">
                    {user && user.role === "teacher" && (
                        <Typography variant='h2'>Questions</Typography>
                    )}
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
                                        question.answers.map((answer) => (
                                            <FormControlLabel
                                                key={answer.id}
                                                control={
                                                    <Checkbox
                                                        onChange={(e) =>
                                                            handleAnswerChange(question.id, answer.id, e.target.checked)
                                                        }
                                                    />
                                                }
                                                label={answer.text}
                                            />
                                        ))
                                    ) : (
                                        <RadioGroup
                                            key={question.id}
                                            onChange={(e) =>
                                                handleSingleAnswerChange(question.id, Number(e.target.value))
                                            }
                                        >
                                            {question.answers.map((answer) => (
                                                <FormControlLabel
                                                    key={answer.id}
                                                    value={answer.id}
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
                            sx={{
                                fontSize: "medium",
                                textTransform: "capitalize"
                            }}
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