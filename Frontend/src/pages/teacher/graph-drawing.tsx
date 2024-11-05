import {useEffect, useState} from "react";
import {Box} from "@mui/material";
import KnowledgeGraph from "../../components/graph/knowledge-graph.tsx";
import "./graph.css";

export default function GraphDrawing(){
    const [nodes, setNodes] = useState<{id: string, data?: string}[]>([]);
    const [links, setLinks] = useState<{source: string, target: string}[]>([]);

    useEffect(() => {
        const newNodes = [{ id: "aaaaaaaaaaaaaaaaa", data: "ahahahah" }, { id: "bb" }, { id: "cc" }];
        const newLinks = [{ source: "aaaaaaaaaaaaaaaaa", target: "bb" }, { source: "bb", target: "cc" }];

        setNodes(newNodes);
        setLinks(newLinks);
    }, []);
    return (
        <Box className="main-graph-container">
            <Box className="graph-options-container">

            </Box>
            <Box className="graph-container">
                <KnowledgeGraph nodes={nodes} links={links} />
            </Box>
        </Box>

    )
}