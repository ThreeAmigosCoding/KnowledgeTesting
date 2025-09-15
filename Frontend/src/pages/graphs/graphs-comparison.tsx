import {Box, FormControl, InputLabel, MenuItem, Select, Typography, useTheme} from "@mui/material";
import {useParams} from "react-router-dom";
import api from "../../config/axios-config.tsx";
import {Edge, Graph, Node, Test} from "../../model/models.tsx";
import {useEffect, useState} from "react";
import './graph.css';
import KnowledgeGraph from "../../components/graph/knowledge-graph.tsx";


export default function GraphsComparison() {

    const { id } = useParams<{ id: string; }>();
    const [test, setTest] = useState<Test>();

    const [assumedNodes, setAssumedNodes] = useState<Node[]>([]);
    const [assumedEdges, setAssumedEdges] = useState<Edge[]>([]);


    const [selectedGraphId, setSelectedGraphId] = useState<number | undefined>();
    const [generatedGraphs, setGeneratedGraphs] = useState<Graph[]>([]);

    const [generatedNodes, setGeneratedNodes] = useState<Node[]>([]);
    const [generatedEdges, setGeneratedEdges] = useState<Edge[]>([]);

    const theme = useTheme();


    useEffect(() => {
        fetchAssumedGraph().then(() => {})
        fetchTest().then(() => {})
    }, []);

    useEffect(() => {
        if (generatedGraphs[0]) handleGraphChange(generatedGraphs[0].id as number);
    }, [generatedGraphs]);

    const fetchAssumedGraph = async () => {
        try {
            const response = await api.get<Graph>(`get-graph-by-test-id`, {
                params: { id }
            });
            if (response.status === 200) {
                const nodes =  response.data.nodes.map(node => ({
                    ...node,
                    color: theme.palette.primary.main,
                }))
                setAssumedNodes(nodes)

                const edges = response.data.edges.map(edge => ({
                    ...edge,
                    color: theme.palette.secondary.contrastText,
                }))
                setAssumedEdges(edges)
                if (response.data.id) fetchGeneratedGraphs(response.data.id).then(() => {});
            }
        }
        catch (error) {
            alert(error)
        }
    }

    const fetchGeneratedGraphs = async (assumedGraphId: number) => {
        try {
            const response = await api.get<Graph[]>(`get-generated-graphs`, {
                params: { assumedGraphId }
            });
            if (response.status === 200) {
                setGeneratedGraphs(response.data);
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

    const handleGraphChange = (graphId: number) => {
        setSelectedGraphId(graphId);
        const generatedGraph = generatedGraphs.find(g => g.id === graphId);
        const generatedNodes = generatedGraph?.nodes || [];
        const generatedEdges = generatedGraph?.edges || [];

        const updatedAssumedNodes = assumedNodes.map(assumedNode => {
            // console.log(assumedNode);
            // console.log(generatedNodes);
            const correspondingGeneratedNode = generatedNodes.find(node => node.title === assumedNode.title);
            if (!correspondingGeneratedNode) {
                return { ...assumedNode, color: theme.palette.error.main };
            } else {
                const assumedNodeEdges = assumedEdges.filter(
                    edge => edge.source.title === assumedNode.title || edge.target.title === assumedNode.title
                );
                const generatedNodeEdges = generatedEdges.filter(
                    edge => edge.source === assumedNode.title || edge.target === assumedNode.title
                );

                const hasDifferentEdges = assumedNodeEdges.some(
                    assumedEdge =>
                        !generatedNodeEdges.find(
                            generatedEdge =>
                                generatedEdge.source === assumedEdge.source.title &&
                                generatedEdge.target === assumedEdge.target.title
                        )
                );

                if (hasDifferentEdges) {
                    return { ...assumedNode, color: theme.palette.primary.light };
                }
                return { ...assumedNode, color: theme.palette.primary.main };
            }

        });

        const updatedAssumedEdges = assumedEdges.map(assumedEdge => {
            const correspondingGeneratedEdge = generatedEdges.find(edge => {
                    return edge.source == assumedEdge.source.title && edge.target == assumedEdge.target.title
                }

            );
            if (!correspondingGeneratedEdge) {
                return { ...assumedEdge, color: theme.palette.error.main, source: assumedEdge.source.title, target: assumedEdge.target.title };
            }
            return { ...assumedEdge, color: theme.palette.secondary.contrastText, source: assumedEdge.source.title, target: assumedEdge.target.title };
        });

        const updatedGeneratedNodes = generatedNodes.map(generatedNode => {
            const correspondingAssumedNode = assumedNodes.find(node => node.title === generatedNode.title);
            if (correspondingAssumedNode) {

                const assumedNodeEdges = assumedEdges.filter(
                    edge => edge.source.title === generatedNode.title || edge.target.title === generatedNode.title
                );
                const generatedNodeEdges = generatedEdges.filter(
                    edge => edge.source === generatedNode.title || edge.target === generatedNode.title
                );

                const hasDifferentEdges = assumedNodeEdges.some(
                    assumedEdge =>
                        !generatedNodeEdges.find(
                            generatedEdge =>
                                generatedEdge.source === assumedEdge.source.title &&
                                generatedEdge.target === assumedEdge.target.title
                        )
                );

                if (hasDifferentEdges) {
                    return { ...generatedNode, color: theme.palette.primary.light };
                }
            }
            return { ...generatedNode, color: theme.palette.primary.main };
        });

        const updatedGeneratedEdges = generatedEdges.map(generatedEdge => {
            const correspondingAssumedEdge = assumedEdges.find(edge => {

                    return edge.source.title === generatedEdge.source && edge.target.title === generatedEdge.target
                }
            );
            if (!correspondingAssumedEdge) {
                return { ...generatedEdge, color: theme.palette.error.main};
            }

            return { ...generatedEdge, color: theme.palette.secondary.contrastText};
        });
        console.log(generatedEdges);
        console.log(updatedGeneratedEdges);

        setAssumedNodes(updatedAssumedNodes);
        setAssumedEdges(updatedAssumedEdges);
        setGeneratedNodes(updatedGeneratedNodes);
        setGeneratedEdges(updatedGeneratedEdges);
    }

    return (
        <Box className='main-container'>
            <Box className='content'>
                <Box className='header-content'>
                    <Typography variant='h2' sx={{textAlign: 'center'}}>{test?.title}</Typography>
                    <Typography variant='h2' sx={{textAlign: 'center'}}>Graphs Comparison</Typography>
                    <FormControl variant="outlined" sx={{minWidth: "25%"}}>
                        <InputLabel id="dynamic-select-label">Choose Graph</InputLabel>
                        <Select
                            labelId="dynamic-select-label"
                            id="dynamic-select"
                            value={selectedGraphId ?? ""}
                            onChange={e => handleGraphChange(e.target.value as number)}
                            label="Choose Graph"
                            variant="outlined">
                            {generatedGraphs.map((item, index) => (
                                <MenuItem key={index} value={item.id}>
                                    {item.id} - {item.title}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Box>
                <Box className='graphs-comparison-container'>
                    <Box sx={{display: 'flex', flexDirection: 'column', gap: '20px'}}>
                        <Typography variant='h3' sx={{textAlign: 'center'}}>Assumed Graph</Typography>
                        <Box className='graph-comparison-container'>
                            <KnowledgeGraph nodes={assumedNodes} links={assumedEdges} />
                        </Box>
                    </Box>
                    <Box sx={{display: 'flex', flexDirection: 'column', gap: '20px'}}>
                        <Typography variant='h3' sx={{textAlign: 'center'}}>Generated Graph</Typography>
                        <Box className='graph-comparison-container'>
                            <KnowledgeGraph nodes={generatedNodes} links={generatedEdges} />
                        </Box>
                    </Box>
                </Box>
            </Box>
        </Box>
    )
}