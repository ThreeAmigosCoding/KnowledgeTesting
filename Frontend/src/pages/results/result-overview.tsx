import {Box, Card, CardContent, Typography} from "@mui/material";
import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import api from "../../config/axios-config.tsx";
import {Question, Result} from "../../model/models.tsx";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import CancelIcon from "@mui/icons-material/Cancel";


export default function ResultOverview() {
    const { id } = useParams<{ id: string; }>();

    const [result, setResult] = useState<Result>();
    const [questions, setQuestions] = useState<Question[]>([]);



    useEffect(() => {
        fetchResult().then(() => {})
    }, []);

    const fetchResult = async () => {
        try {
            const result_id = id?.valueOf()
            const response = await api.get<Result>(`get-result`, {
                params: { resultId: result_id }
            });
            if (response.status === 200) {
                setResult(response.data);
                setQuestions(response.data.test.questions as Question[]);
            }
        }
        catch (error) {
            alert(error)
        }
    }

    return (
        <Box className='main-container'>
            <Box className='content'>
                <Typography variant='h1' sx={{textAlign: 'center'}}>Result for test: {result?.test?.title}</Typography>
                <Box className="questions-container">
                    {
                        questions.map((question) => {
                            const studentAnswers = result?.student_answers[question.id] || [];

                            const correctAnswers = question.answers
                                .filter((answer) => answer.is_correct)
                                .map((answer) => answer.id);

                            const isCorrect =
                                studentAnswers.length === correctAnswers.length &&
                                studentAnswers.every((id: number) => correctAnswers.includes(id));

                            return (
                                <Card key={question.id} className="question-container">
                                    <CardContent className="question-card-content">
                                        <Box display="flex" alignItems="center" gap={1}>
                                            <Typography variant="h4">{question.text}</Typography>
                                            {isCorrect ? (
                                                <CheckCircleIcon sx={{ color: "success.main" }} />
                                            ) : (
                                                <CancelIcon sx={{ color: "error.main" }} />
                                            )}
                                        </Box>
                                        {question.answers.map((answer) => {
                                            const isChosen = studentAnswers.includes(answer.id as number);

                                            const backgroundColor = isChosen
                                                ? answer.is_correct
                                                    ? "success.light"
                                                    : "error.light"
                                                : "transparent";

                                            return (
                                                <Typography
                                                    key={answer.id}
                                                    sx={{
                                                        color: answer.is_correct && !isChosen ? "success.main" : "#1A1A1A",
                                                        backgroundColor,
                                                        padding: "4px 8px",
                                                        borderRadius: "4px"
                                                    }}
                                                    variant="h3"
                                                >
                                                    • {answer.text}
                                                </Typography>
                                            );
                                        })}
                                    </CardContent>
                                </Card>
                            );
                        })
                    }
                </Box>
            </Box>
        </Box>
    )

}
