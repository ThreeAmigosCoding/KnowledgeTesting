import {Box, FormControl, InputLabel, MenuItem, Select, Typography} from "@mui/material";
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
                setAssumedNodes(response.data.nodes)
                setAssumedEdges(response.data.edges)
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
                setGeneratedGraphs(response.data)
                console.log(response.data)
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
        const nodes  = generatedGraphs.find(g => g.id == graphId)?.nodes
        if (nodes) setGeneratedNodes(nodes)

        const edges  = generatedGraphs.find(g => g.id == graphId)?.edges
        if (edges) setGeneratedEdges(edges)
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