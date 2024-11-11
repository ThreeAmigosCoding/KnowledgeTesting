import {
    Box,
    Typography,
    Card,
    CardContent,
    Button,
    TextField,
    Switch,
    IconButton,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import './tests.css';
import api from "../../config/axios-config.tsx";
import { useEffect, useState } from "react";
import { Answer, Question, Test } from "../../model/models.tsx";
import { useNavigate } from "react-router-dom";

export default function TestCreate() {
    const navigate = useNavigate();
    const [testTitle, setTestTitle] = useState<string>("");
    const [newQuestionText, setNewQuestionText] = useState<string>("");
    const [newAnswerText, setNewAnswerText] = useState<string>("");
    const [newAnswers, setNewAnswers] = useState<Answer[]>([]);
    const [questions, setQuestions] = useState<Question[]>([]);

    const addAnswer = () => {
        if (newAnswerText.trim()) {
            const newAnswer: Answer = { text: newAnswerText, is_correct: false };
            setNewAnswers((prevAnswers) => [...prevAnswers, newAnswer]);
            setNewAnswerText("");
        }
    };

    const removeAnswer = (index: number) => {
        setNewAnswers((prevAnswers) =>
            prevAnswers.filter((_, i) => i !== index)
        );
    };

    const toggleCorrectAnswer = (index: number) => {
        setNewAnswers((prevAnswers) =>
            prevAnswers.map((answer, i) =>
                i === index ? { ...answer, is_correct: !answer.is_correct } : answer
            )
        );
    };

    const addQuestion = () => {
        if (
            newQuestionText.trim() &&
            newAnswers.length >= 2 &&
            newAnswers.some((answer) => answer.is_correct) &&
            !newAnswers.every((answer) => answer.is_correct)
        ) {
            const isMultiChoice = newAnswers.filter(answer => answer.is_correct).length > 1;
            const newQuestion: Question = {
                text: newQuestionText,
                answers: newAnswers,
                is_multichoice: isMultiChoice
            };
            setQuestions((prevQuestions) => [...prevQuestions, newQuestion]);
            setNewQuestionText("");
            setNewAnswers([]);
        }
    };

    const deleteQuestion = (index: number) => {
        setQuestions((prevQuestions) =>
            prevQuestions.filter((_, qIndex) => qIndex !== index)
        );
    };

    const isAddQuestionDisabled = !(
        newQuestionText.trim() &&
        newAnswers.length >= 2 &&
        newAnswers.some((answer) => answer.is_correct) &&
        !newAnswers.every((answer) => answer.is_correct)
    );

    const isSaveTestDisabled = !(
        testTitle.trim() &&
        questions.length != 0
    );

    const saveTest = async () => {
        try {
            const test: Test = {
                title: testTitle,
                author_id: 1, // TODO FIX THIS
                graph_id: 1,
                questions: questions
            }
            const response = await api.post<Test>(`create-test`, test);
            if (response.status === 201) {
                alert("Test created successfully.")
                navigate("/")
            }
        }
        catch (error) {
            alert(error)
        }
    }

    return (
        <Box className="main-container">
            <Box className="test-create-content">
                <TextField
                    id="test-title"
                    name="test-title"
                    label="Test Title"
                    value={testTitle}
                    onChange={(e) => setTestTitle(e.target.value)}
                />
                <Box className="panels-container">
                    <Box className="test-create-panel">
                        <TextField
                            id="new-question-text"
                            name="new-question-text"
                            label="Question"
                            value={newQuestionText}
                            fullWidth
                            onChange={(e) => setNewQuestionText(e.target.value)}
                        />
                        <Box id="new-answer-container">
                            <TextField
                                id="new-answer-text"
                                name="new-answer-text"
                                label="Answer"
                                value={newAnswerText}
                                onChange={(e) => setNewAnswerText(e.target.value)}
                            />
                            <Button
                                sx={{
                                    fontSize: "larger",
                                    textTransform: "capitalize",
                                    maxWidth: "300px",
                                }}
                                id="add-answer"
                                variant="contained"
                                color="primary"
                                onClick={addAnswer}
                            >
                                Add Answer
                            </Button>
                        </Box>
                        <Box className="answers-preview">
                            {newAnswers.map((answer, index) => (
                                <Box key={index} display="flex" alignItems="center">
                                    <Typography>{answer.text}</Typography>
                                    <Switch
                                        checked={answer.is_correct}
                                        onChange={() => toggleCorrectAnswer(index)}
                                        color="primary"
                                    />
                                    <IconButton
                                        color="secondary"
                                        onClick={() => removeAnswer(index)}
                                    >
                                        <DeleteIcon />
                                    </IconButton>
                                </Box>
                            ))}
                        </Box>
                        <Button
                            sx={{
                                fontSize: "larger",
                                textTransform: "capitalize",
                            }}
                            fullWidth
                            id="add-question"
                            variant="contained"
                            color="primary"
                            onClick={addQuestion}
                            disabled={isAddQuestionDisabled}
                        >
                            Add Question
                        </Button>
                    </Box>
                    <Box className="test-create-panel">
                        <Box className="questions-title-and-save-button">
                            <Typography variant="h3">Questions</Typography>
                            <Button
                                sx={{
                                    fontSize: "larger",
                                    textTransform: "capitalize",
                                }}
                                id="save-test"
                                variant="contained"
                                color="primary"
                                onClick={saveTest}
                                disabled={isSaveTestDisabled}
                            >
                                Save Test
                            </Button>
                        </Box>
                        {questions.map((question, qIndex) => (
                            <Card key={qIndex} className="question-container">
                                <CardContent className="question-card-content" sx={{ position: "relative" }}>
                                    <IconButton
                                        color="secondary"
                                        onClick={() => deleteQuestion(qIndex)}
                                        sx={{ position: "absolute", top: 5, right: 5 }}
                                    >
                                        <DeleteIcon />
                                    </IconButton>
                                    <Typography variant="h3">{question.text}</Typography>
                                    <Box className="answers-container">
                                        {question.answers.map((answer, aIndex) => (
                                            <Typography
                                                key={aIndex}
                                                sx={{
                                                    color: answer.is_correct ? "success.main" : "#1A1A1A",
                                                }}
                                                variant="h4"
                                            >
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
        </Box>
    );
}
