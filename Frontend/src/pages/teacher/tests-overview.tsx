import { Box, Typography, Card, CardContent } from "@mui/material";
import './tests.css';
import {Test} from "../../model/models.tsx";

const tests: Test[] = [
    {
        id: "1",
        title: "Math Basics",
        author: {
            id: "101",
            firstName: "Alice",
            lastName: "Anderson",
            email: "alice@example.com",
            role: "teacher",
            password: "password123"
        },
        questions: [
            {
                id: "q1",
                text: "What is 2 + 2?",
                answers: [
                    { id: "a1", isCorrect: true, text: "4" },
                    { id: "a2", isCorrect: false, text: "3" },
                    { id: "a3", isCorrect: false, text: "5" },
                ]
            }
        ]
    },
    {
        id: "2",
        title: "History Quiz",
        author: {
            id: "102",
            firstName: "Bob",
            lastName: "Brown",
            email: "bob@example.com",
            role: "teacher",
            password: "password123"
        },
        questions: [
            {
                id: "q2",
                text: "Who was the first president of the United States?",
                answers: [
                    { id: "a4", isCorrect: true, text: "George Washington" },
                    { id: "a5", isCorrect: false, text: "Abraham Lincoln" },
                    { id: "a6", isCorrect: false, text: "Thomas Jefferson" },
                ]
            }
        ]
    },
    {
        id: "3",
        title: "Science Fundamentals",
        author: {
            id: "103",
            firstName: "Charlie",
            lastName: "Clark",
            email: "charlie@example.com",
            role: "teacher",
            password: "password123"
        },
        questions: [
            {
                id: "q3",
                text: "What is the chemical symbol for water?",
                answers: [
                    { id: "a7", isCorrect: true, text: "H2O" },
                    { id: "a8", isCorrect: false, text: "CO2" },
                    { id: "a9", isCorrect: false, text: "O2" },
                ]
            }
        ]
    }
];

export default function TestsOverview() {

    return (
        <Box className='main-container'>
            <Box className='content'>
                <Typography variant='h1'>Tests</Typography>
                <Box className="tests-container">
                    {tests.map((test) => (
                        <Card key={test.id} className="test-card">
                            <CardContent className="test-card-content">
                                <Typography variant="h2">{test.title}</Typography>
                                <Typography variant="h4">
                                    Author: {test.author.firstName} {test.author.lastName}
                                </Typography>
                                <Typography variant="h5">
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