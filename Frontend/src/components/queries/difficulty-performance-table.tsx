import {
    Box,
    Chip,
    LinearProgress,
    Stack,
    Table,
    TableHead,
    TableRow,
    TableCell,
    TableBody,
    Typography,
} from "@mui/material";
import React from "react";

type DifficultyPerformanceRow = {
    graph_title?: string;
    first_name?: string;
    last_name?: string;
    very_easy_performance?: string | number | null;
    easy_performance?: string | number | null;
    medium_performance?: string | number | null;
    difficult_performance?: string | number | null;
    tests_taken?: string | number;
};

const pct = (v: string | number | null | undefined) => {
    if (v === undefined || v === null || v === "") return null;
    const n = typeof v === "string" ? parseFloat(v) : v;
    return Number.isFinite(n) ? Math.max(0, Math.min(100, n)) : null;
};

const fullName = (r: DifficultyPerformanceRow) =>
    [r.first_name, r.last_name].filter(Boolean).join(" ");

const ScoreBar: React.FC<{ value: number | null }> = ({ value }) => {
    if (value === null) {
        return (
            <Typography variant="body2" sx={{ color: "text.secondary" }}>
                N/A
            </Typography>
        );
    }

    return (
        <Stack direction="row" spacing={1} alignItems="center" sx={{ minWidth: 180 }}>
            <Box sx={{ flex: 1 }}>
                <LinearProgress variant="determinate" value={value} />
            </Box>
            <Typography variant="body2" sx={{ width: 50, textAlign: "right" }}>
                {value.toFixed(1)}%
            </Typography>
        </Stack>
    );
};

const DifficultyPerformanceTable: React.FC<{ rows: DifficultyPerformanceRow[] }> = ({ rows }) => {
    if (!rows?.length) {
        return (
            <Typography variant="body2" sx={{ color: "text.secondary" }}>
                No results to display.
            </Typography>
        );
    }

    // Group by graph title
    const groupedByGraph = rows.reduce((acc, row) => {
        const graphTitle = row.graph_title || "Unknown Graph";
        if (!acc[graphTitle]) {
            acc[graphTitle] = [];
        }
        acc[graphTitle].push(row);
        return acc;
    }, {} as Record<string, DifficultyPerformanceRow[]>);

    return (
        <Box>
            {Object.entries(groupedByGraph).map(([graphTitle, graphRows]) => (
                <Box key={graphTitle} sx={{ mb: 4 }}>
                    <Typography variant="h6" sx={{ mb: 2, color: "primary.main" }}>
                        {graphTitle}
                    </Typography>

                    <Table size="small" aria-label={`Difficulty Performance Table for ${graphTitle}`}>
                        <TableHead>
                            <TableRow>
                                <TableCell>Student</TableCell>
                                <TableCell align="right">Tests Taken</TableCell>
                                <TableCell>Very Easy</TableCell>
                                <TableCell>Easy</TableCell>
                                <TableCell>Medium</TableCell>
                                <TableCell>Difficult</TableCell>
                            </TableRow>
                        </TableHead>

                        <TableBody>
                            {graphRows.map((r, idx) => {
                                const veryEasy = pct(r.very_easy_performance);
                                const easy = pct(r.easy_performance);
                                const medium = pct(r.medium_performance);
                                const difficult = pct(r.difficult_performance);

                                return (
                                    <TableRow key={idx}>
                                        <TableCell>
                                            <Typography variant="subtitle2">{fullName(r)}</Typography>
                                        </TableCell>

                                        <TableCell align="right">
                                            <Chip size="small" label={String(r.tests_taken ?? "0")} />
                                        </TableCell>

                                        <TableCell>
                                            <ScoreBar value={veryEasy} />
                                        </TableCell>

                                        <TableCell>
                                            <ScoreBar value={easy} />
                                        </TableCell>

                                        <TableCell>
                                            <ScoreBar value={medium} />
                                        </TableCell>

                                        <TableCell>
                                            <ScoreBar value={difficult} />
                                        </TableCell>
                                    </TableRow>
                                );
                            })}
                        </TableBody>
                    </Table>
                </Box>
            ))}
        </Box>
    );
};

export default DifficultyPerformanceTable;