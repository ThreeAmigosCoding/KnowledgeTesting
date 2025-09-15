import {useEffect, useState} from "react";
import {Box, Button, TextField, Typography, useTheme} from "@mui/material";
import KnowledgeGraph from "../../components/graph/knowledge-graph.tsx";
import "./graph.css";
import {Node, Edge, Graph} from "../../model/models.tsx";
import api from "../../config/axios-config.tsx";

export default function GraphDrawing(){
    const [nodes, setNodes] = useState<Node[]>([]);
    const [links, setLinks] = useState<Edge[]>([]);
    const [graphTitle, setGraphTitle] = useState<string>("");
    const [nodeTitle, setNodeTitle] = useState<string>("");
    const [sourceNodeTitle, setSourceNodeTitle] = useState<string>("");
    const [targetNodeTitle, setTargetNodeTitle] = useState<string>("");

    const theme = useTheme();

    useEffect(() => {
        console.log(links)
    }, [links]);

    const addNode = () => {
        if (nodeTitle.trim() === "") return;

        const nodeExists = nodes.some((node) => node.title === nodeTitle);
        if (nodeExists) {
            alert("Node with the same title already exists.");
            return;
        }

        const newNode = { title: nodeTitle, color: theme.palette.primary.main };
        setNodes((prevNodes) => [...prevNodes, newNode]);
        setNodeTitle("");
    };

    const removeNode = () => {
        if (nodeTitle.trim() === "") return;

        setNodes((prevNodes) => prevNodes.filter((node) => node.title !== nodeTitle));

        setLinks((prevLinks) =>
            prevLinks.filter((link) => link.source.title !== nodeTitle && link.target.title !== nodeTitle)
        );

        setNodeTitle("");
    };

    const addEdge = () => {
        if (sourceNodeTitle.trim() === "" || targetNodeTitle.trim() === "") return;

        const sourceNodeExists = nodes.some((node) => node.title === sourceNodeTitle);
        const targetNodeExists = nodes.some((node) => node.title === targetNodeTitle);

        if (!sourceNodeExists || !targetNodeExists) {
            alert("Both source and target nodes must exist.");
            return;
        }

        const linkExists = links.some(
            (link) => link.source === sourceNodeTitle && link.target === targetNodeTitle
        );
        if (linkExists) {
            alert("Edge between these nodes already exists.");
            return;
        }

        const newLink: Edge = { source: sourceNodeTitle, target: targetNodeTitle, color: theme.palette.secondary.contrastText };
        setLinks((prevLinks) => [...prevLinks, newLink]);
        setSourceNodeTitle("");
        setTargetNodeTitle("");
    };

    const removeEdge = () => {
        if (sourceNodeTitle.trim() === "" || targetNodeTitle.trim() === "") return;

        setLinks((prevLinks) =>
            prevLinks.filter(
                (link) => !(link.source.title === sourceNodeTitle && link.target.title === targetNodeTitle)
            )
        );

        setSourceNodeTitle("");
        setTargetNodeTitle("");
    };

    const saveGraph = async () => {
        try {
            const graph: Graph = {
                title: graphTitle,
                nodes: nodes,
                edges: links,
            }
            console.log(graph)
            const response = await api.post<Graph>("/save-graph", graph);
            if (response.status == 201) {
                alert("Graph created");
            }
        } catch (error) {
            alert(error)
        }

    }

    return (
        <Box className="main-graph-container">
            <Box className="graph-options-container">
                <Typography variant="h2">Graph Editor</Typography>
                <TextField
                    id="graph-title"
                    name="graph-title"
                    label="Graph Title"
                    value={graphTitle}
                    onChange={(e) => setGraphTitle(e.target.value)}
                />
                <Box className="add-node-container">
                    <TextField
                        id="node-title"
                        name="node-title"
                        label="Node Title"
                        value={nodeTitle}
                        onChange={(e) => setNodeTitle(e.target.value)}
                    />
                    <Button
                        sx={{
                            fontSize: "medium",
                            textTransform: "capitalize"
                        }}
                        id="add-node-button"
                        variant="contained" color="primary"
                        disabled={nodeTitle.trim() === ""}
                        onClick={addNode}>
                        Add Node
                    </Button>
                    <Button
                        sx={{
                            fontSize: "medium",
                            textTransform: "capitalize"
                        }}
                        id="remove-node-button"
                        variant="contained" color="error"
                        disabled={nodeTitle.trim() === ""}
                        onClick={removeNode}>
                        Remove Node
                    </Button>
                </Box>
                <Box className="add-edge-container">
                    <TextField
                        id="source-title"
                        name="source-title"
                        label="Source Node Title"
                        value={sourceNodeTitle}
                        onChange={(e) => setSourceNodeTitle(e.target.value)}
                    />
                    <TextField
                        id="target-title"
                        name="target-title"
                        label="Target Node Title"
                        value={targetNodeTitle}
                        onChange={(e) => setTargetNodeTitle(e.target.value)}
                    />
                    <Button
                        sx={{
                            fontSize: "medium",
                            textTransform: "capitalize",
                            minWidth: "160px"
                        }}
                        id="add-edge-button"
                        variant="contained" color="primary"
                        disabled={sourceNodeTitle.trim() === "" || targetNodeTitle.trim() === ""}
                        onClick={addEdge}>
                        Add Edge
                    </Button>
                    <Button
                        sx={{
                            fontSize: "medium",
                            textTransform: "capitalize",
                            minWidth: "160px"
                        }}
                        id="remove-edge-button"
                        variant="contained" color="error"
                        disabled={sourceNodeTitle.trim() === "" || targetNodeTitle.trim() === ""}
                        onClick={removeEdge}>
                        Remove Edge
                    </Button>
                </Box>
                <Button
                    sx={{
                        fontSize: "large",
                        textTransform: "capitalize"
                    }}
                    id="save-graph-button"
                    variant="contained" color="primary"
                    disabled={graphTitle.trim() === ""}
                    onClick={saveGraph}>
                    Save
                </Button>
            </Box>
            <Box className="graph-container">
                <KnowledgeGraph nodes={nodes} links={links} />
            </Box>
        </Box>

    )
}