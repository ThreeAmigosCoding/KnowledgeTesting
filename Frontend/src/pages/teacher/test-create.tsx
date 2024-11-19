import {
    Box,
    Typography,
    Card,
    CardContent,
    Button,
    TextField,
    Switch,
    IconButton, FormControl, InputLabel, Select, MenuItem,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import './tests.css';
import api from "../../config/axios-config.tsx";
import { useEffect, useState } from "react";
import {Answer, Graph, Question, Test, Node, Edge} from "../../model/models.tsx";
import { useNavigate } from "react-router-dom";
import KnowledgeGraph from "../../components/graph/knowledge-graph.tsx";

export default function TestCreate() {
    const navigate = useNavigate();
    const [testTitle, setTestTitle] = useState<string>("");
    const [newQuestionText, setNewQuestionText] = useState<string>("");
    const [newAnswerText, setNewAnswerText] = useState<string>("");
    const [newAnswers, setNewAnswers] = useState<Answer[]>([]);
    const [questions, setQuestions] = useState<Question[]>([]);

    const [availableGraphs, setAvailableGraphs] = useState<Graph[]>([]);
    const [selectedGraphId, setSelectedGraphId] = useState<number | undefined>();

    const [availableNodes, setAvailableNodes] = useState<Node[]>([]);
    const [selectedNodeId, setSelectedNodeId] = useState<number | undefined>();

    const [availableEdges, setAvailableEdges] = useState<Edge[]>([]);

    useEffect(() => {
        fetchGraphs().then(() => {});
    }, []);

    const fetchGraphs = async () => {
        try {
            // const author_id = 1;
            const response = await api.get<Graph[]>(`get-graphs`);
            if (response.status === 200) {
                setAvailableGraphs(response.data);

            }
        }
        catch (error) {
            alert(error)
        }
    }

    useEffect(() => {
        if (availableGraphs[0]) handleGraphChange(availableGraphs[0].id as number);
    }, [availableGraphs]);

    const handleGraphChange = (graphId: number) => {
        setSelectedGraphId(graphId);
        const nodes  = availableGraphs.find(g => g.id == graphId)?.nodes
        if (nodes) {setAvailableNodes(nodes); setSelectedNodeId(nodes[0].id);}

        const edges  = availableGraphs.find(g => g.id == graphId)?.edges
        if (edges) setAvailableEdges(edges)
    }

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
            selectedNodeId &&
            newAnswers.length >= 2 &&
            newAnswers.some((answer) => answer.is_correct) &&
            !newAnswers.every((answer) => answer.is_correct)
        ) {
            const isMultiChoice = newAnswers.filter(answer => answer.is_correct).length > 1;
            const newQuestion: Question = {
                text: newQuestionText,
                answers: newAnswers,
                is_multichoice: isMultiChoice,
                node_id: selectedNodeId
            };
            setQuestions((prevQuestions) => [...prevQuestions, newQuestion]);
            setNewQuestionText("");
            setNewAnswers([]);
        }
    };

    const topologicalSort = () => {
        const sortedNodes: Node[] = [];
        const visited = new Set<string>();
        const tempVisited = new Set<string>();

        const visit = (node: Node) => {
            if (tempVisited.has(node.title)) {
                throw new Error("Graph has cycles!");
            }
            if (!visited.has(node.title)) {
                tempVisited.add(node.title);
                const outgoingEdges = availableEdges.filter(edge => edge.source === node.title);
                outgoingEdges.forEach(edge => {
                    const targetNode = availableNodes.find(n => n.title === edge.target);
                    if (targetNode) visit(targetNode);
                });
                tempVisited.delete(node.title);
                visited.add(node.title);
                sortedNodes.push(node);
            }
        };

        availableNodes.forEach(node => {
            if (!visited.has(node.title)) visit(node);
        });

        return sortedNodes;
    };


    const getOrderedQuestions = () => {
        const sortedNodes = topologicalSort();
        const nodeOrder = sortedNodes.map(node => node.id);

        return questions.slice().sort((a, b) => {
            return nodeOrder.indexOf(a.node_id) - nodeOrder.indexOf(b.node_id);
        });
    };

    const deleteQuestion = (index: number) => {
        setQuestions((prevQuestions) =>
            prevQuestions.filter((_, qIndex) => qIndex !== index)
        );
    };

    const isAddQuestionDisabled = !(
        newQuestionText.trim() &&
        selectedNodeId &&
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
                graph_id: selectedGraphId,
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
                        <FormControl fullWidth variant="outlined" sx={{ marginBottom: 2 }}>
                            <InputLabel id="dynamic-select-label">Choose Graph</InputLabel>
                            <Select
                                labelId="dynamic-select-label"
                                id="dynamic-select"
                                value={selectedGraphId ?? ""}
                                onChange={e => handleGraphChange(e.target.value as number)}
                                label="Choose Graph"
                                variant="outlined">
                                {availableGraphs.map((item, index) => (
                                    <MenuItem key={index} value={item.id}>
                                        {item.id} - {item.title}
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                        <Box className="test-create-graph-container">
                            <KnowledgeGraph nodes={availableNodes} links={availableEdges} />
                        </Box>
                    </Box>
                    <Box className="test-create-panel">
                        <FormControl fullWidth variant="outlined" sx={{ marginBottom: 2 }}>
                            <InputLabel id="dynamic-select-label-node">Choose Question Field</InputLabel>
                            <Select
                                labelId="dynamic-select-label-node"
                                value={selectedNodeId ?? ""}
                                onChange={e => setSelectedNodeId(e.target.value as number)}
                                label="Choose Question Field"
                                variant="outlined">
                                {availableNodes.map((item, index) => (
                                    <MenuItem key={index} value={item.id}>
                                        {index + 1} - {item.title}
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl>
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
                        {getOrderedQuestions().map((question, qIndex) => (
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
