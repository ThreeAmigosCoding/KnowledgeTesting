import React, { useCallback, useMemo, useState } from "react";
import "./queries.css";
import { Divider, Typography, Paper } from "@mui/material";
import QueryCard, { QueryDefinition, QueryParameterValueMap } from "./query-card";
import {QueriesService} from "../../services/queries-service.ts";


const service = new QueriesService();

const QueriesOverview: React.FC = () => {
    const queries: QueryDefinition[] = useMemo(
        () => [
            {
                id: "get-all-students",
                name: "Get all students",
                parameters: [
                    { name: "name", optional: true, valueType: "string", label: "Name" },
                    { name: "surname", optional: true, valueType: "string", label: "Surname" },
                    { name: "age", optional: false, valueType: "number", label: "Age" },
                ],
            },
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
                        parameters={q.parameters}
                        onExecute={handleExecute}
                    />
                ))}
            </div>

            <div className="query-result-container">
                <Typography variant="h2">
                    Result
                </Typography>
                <Divider />
                <Paper variant="outlined" sx={{ p: 2, minHeight: 200 }}>
                    <Typography variant="body2" sx={{ color: "text.secondary", mb: 1 }}>
                        {activeQueryId ? `Query: ${activeQueryId}` : "No query executed yet."}
                    </Typography>
                    <pre style={{ margin: 0, whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
          {activeResult ? JSON.stringify(activeResult, null, 2) : "—"}
        </pre>
                </Paper>
            </div>
        </div>
    );
};

export default QueriesOverview;