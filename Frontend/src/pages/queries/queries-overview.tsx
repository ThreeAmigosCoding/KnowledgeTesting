import React, { useCallback, useMemo, useState } from "react";
import "./queries.css";
import { Divider, Typography, Box } from "@mui/material";
import QueryCard, { QueryDefinition, QueryParameterValueMap } from "./query-card";
import {QueriesService} from "../../services/queries-service.ts";
import AverageScoresTable from "../../components/queries/average-scores-table.tsx";
import ProblematicTopicsTable from "../../components/queries/problematic-topics-table.tsx";
import PrerequisiteMasteryTable from "../../components/queries/prerequisite-mastery-table.tsx";
import DifficultyPerformanceTable from "../../components/queries/difficulty-performance-table.tsx";


const service = new QueriesService();

const QueriesOverview: React.FC = () => {
    const queries: QueryDefinition[] = useMemo(
        () => [
            {
                id: "average-scores",
                name: "Score",
                description: "Per-student summary: total tests taken, average score (%), and best single-test score (%).",
                parameters: [
                    { name: "first_name", optional: true, valueType: "string", label: "Name" },
                    { name: "last_name", optional: true, valueType: "string", label: "Surname" },
                    { name: "min_avg_score", optional: true, valueType: "number", label: "Min Average Score" },
                    { name: "max_avg_score", optional: true, valueType: "number", label: "Max Average Score" },
                ],
            },
            {
                id: "problematic-topics",
                name: "Problematic Topics",
                description: "For each student and knowledge graph, pinpoints the weakest topic — the one with the highest error rate. Shows error count, total questions, and error percentage.",
                parameters: [
                    { name: "first_name", optional: true, valueType: "string", label: "Name" },
                    { name: "last_name", optional: true, valueType: "string", label: "Surname" },
                    { name: "graph_title", optional: true, valueType: "string", label: "Title" },
                    { name: "error_percentage", optional: true, valueType: "number", label: "Error percentge" },
                ],
            },
            {
                id: "prerequisite-mastery",
                name: "Prerequisite Mastery",
                description: "Flags topics where both the topic and its prerequisites are weak. Shows the topic, its underperforming prerequisites, and average correctness for each.",
                parameters: [
                    { name: "first_name", optional: true, valueType: "string", label: "Name" },
                    { name: "last_name", optional: true, valueType: "string", label: "Surname" },
                    { name: "topic", optional: true, valueType: "string", label: "Topic" },
                    { name: "weak_prerequisites", optional: true, valueType: "string", label: "Weak prerequisites" },
                ],
            },
            {
                id: "difficulty-performance-analysis",
                name: "Difficulty Performance Analysis",
                description: "Breaks down student performance by question difficulty (very easy, easy, medium, difficult) per graph.",
                parameters: [
                    { name: "first_name", optional: true, valueType: "string", label: "Name" },
                    { name: "last_name", optional: true, valueType: "string", label: "Surname" },
                    { name: "graph_title", optional: true, valueType: "string", label: "Graph Title" },
                ],
            }
        ],
        []
    );

    const [activeResult, setActiveResult] = useState<any>(null);
    const [activeQueryId, setActiveQueryId] = useState<string | null>(null);

    const handleExecute = useCallback(
        async (queryId: string, values: QueryParameterValueMap) => {
            setActiveQueryId(queryId);
            try {
                const result = await service.execute(queryId, values);
                setActiveResult(result);
            } catch (err: any) {
                setActiveResult({
                    error: true,
                    message: err?.message ?? "Unexpected error while executing query.",
                });
            }
        },
        []
    );

    return (
        <div className="main-queries-container">
            <div className="queries-container">
                <Typography variant="h2">
                    Queries
                </Typography>
                <Divider />
                {queries.map((q) => (
                    <QueryCard
                        key={q.id}
                        id={q.id}
                        name={q.name}
                        description={q.description}
                        parameters={q.parameters}
                        onExecute={handleExecute}
                    />
                ))}
            </div>

            <div className="query-result-container">
                <Typography variant="h2">Result</Typography>
                <Divider />

                <Box>
                    <Typography variant="body2" sx={{ color: "text.secondary", mb: 1 }}>
                        {activeQueryId
                            ? `Query: ${queries.find((q) => q.id === activeQueryId)?.name ?? activeQueryId}`
                            : "No query executed yet."}
                    </Typography>

                    {!activeResult ? (
                        <Typography variant="body2" sx={{ color: "text.secondary" }}>—</Typography>
                    ) : activeResult?.error ? (
                        <pre style={{ margin: 0, whiteSpace: "pre-wrap", wordBreak: "break-word", color: "crimson" }}>
                            {JSON.stringify(activeResult, null, 2)}
                          </pre>
                    ) : activeQueryId === "average-scores" ? (
                            <AverageScoresTable rows={Array.isArray(activeResult) ? activeResult : []} />
                    ) : activeQueryId === "problematic-topics" ? (
                            <ProblematicTopicsTable rows={Array.isArray(activeResult) ? activeResult : []} />
                    ) : activeQueryId === "prerequisite-mastery" ? (
                            <PrerequisiteMasteryTable rows={Array.isArray(activeResult) ? activeResult : []} />
                    ) : activeQueryId === "difficulty-performance-analysis" ? (
                            <DifficultyPerformanceTable rows={Array.isArray(activeResult) ? activeResult : []} />
                    ) : (
                        <pre style={{ margin: 0, whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
                            {JSON.stringify(activeResult, null, 2)}
                          </pre>
                    )}
                </Box>
            </div>
        </div>
    );
};

export default QueriesOverview;