import {Box, Card, CardContent, Typography, useTheme} from "@mui/material";
import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import api from "../../config/axios-config.tsx";
import {Graph, Question, Result, Node, Edge} from "../../model/models.tsx";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import CancelIcon from "@mui/icons-material/Cancel";
import KnowledgeGraph from "../../components/graph/knowledge-graph.tsx";
import {useUser} from "../../context/user-context.tsx";


export default function ResultOverview() {
    const { id } = useParams<{ id: string; }>();
    const theme = useTheme();
    const { user } = useUser();

    const [result, setResult] = useState<Result>();
    const [questions, setQuestions] = useState<Question[]>([]);

    const [nodes, setNodes] = useState<Node[]>([]);
    const [edges, setEdges] = useState<Edge[]>([]);


    useEffect(() => {
        fetchResult().then(() => {})
    }, []);

    useEffect(() => {
        if (result) fetchGraph(result.test.id).then(() => {})
    }, [result]);

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

    const fetchGraph = async (id: number) => {
        try {
            const response = await api.get<Graph>(`get-graph-by-test-id`, {
                params: { id }
            });
            if (response.status === 200 && result) {
                const nodes = response.data.nodes.map(node => {
                    console.log(questions)
                    const relatedQuestion = questions.find(q => q.node === node.id);
                    if (!relatedQuestion) return { ...node, color: theme.palette.primary.main };

                    const studentAnswers = result.student_answers[relatedQuestion.id] || [];
                    const correctAnswers = relatedQuestion.answers
                        .filter(answer => answer.is_correct)
                        .map(answer => answer.id);

                    const isCorrect =
                        studentAnswers.length === correctAnswers.length &&
                        studentAnswers.every((id: number) => correctAnswers.includes(id));

                    return {
                        ...node,
                        color: isCorrect ? theme.palette.success.main : theme.palette.error.main,
                        questionText: relatedQuestion.text
                    };
                });
                setNodes(nodes)

                const edges = response.data.edges.map(edge => ({
                    ...edge,
                    color: theme.palette.secondary.contrastText,
                }))
                setEdges(edges)
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
                <Box sx={{
                    display: "flex",
                    gap: "10px",
                    maxHeight: "calc(100vh - 220px)"
                }}>
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
                    { user && user.role === "teacher" && <Box
                        sx={{
                            minWidth: "600px"
                        }}
                    >
                        <KnowledgeGraph nodes={nodes} links={edges}/>
                    </Box>}
                </Box>

            </Box>
        </Box>
    )

}
