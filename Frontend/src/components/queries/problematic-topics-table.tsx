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

type ProblematicTopicRow = {
    error_count?: string | number;
    error_percentage?: string | number;
    first_name?: string;
    last_name?: string;
    graph_title?: string;
    total_questions?: string | number;
    weakest_topic?: string;
};

const pct = (v: string | number | undefined) => {
    if (v === undefined || v === null || v === "") return 0;
    const n = typeof v === "string" ? parseFloat(v) : v;
    return Number.isFinite(n) ? Math.max(0, Math.min(100, n)) : 0;
};

const fullName = (r: ProblematicTopicRow) =>
    [r.first_name, r.last_name].filter(Boolean).join(" ");

const ScoreBar: React.FC<{ value: number }> = ({ value }) => (
    <Stack direction="row" spacing={1} alignItems="center" sx={{ minWidth: 180 }}>
        <Box sx={{ flex: 1 }}>
            <LinearProgress variant="determinate" value={value} />
        </Box>
        <Typography variant="body2" sx={{ width: 50, textAlign: "right" }}>
            {value.toFixed(1)}%
        </Typography>
    </Stack>
);

const ProblematicTopicsTable: React.FC<{ rows: ProblematicTopicRow[] }> = ({ rows }) => {
    if (!rows?.length) {
        return (
            <Typography variant="body2" sx={{ color: "text.secondary" }}>
                No results to display.
            </Typography>
        );
    }

    const sorted = [...rows].sort(
        (a, b) => pct(b.error_percentage) - pct(a.error_percentage)
    );

    return (
        <Table size="small" aria-label="Problematic Topics Table">
            <TableHead>
                <TableRow>
                    <TableCell>Student</TableCell>
                    <TableCell>Graph</TableCell>
                    <TableCell>Weakest Topic</TableCell>
                    <TableCell align="right">Error Count</TableCell>
                    <TableCell align="right">Total Questions</TableCell>
                    <TableCell>Error Percentage</TableCell>
                </TableRow>
            </TableHead>

            <TableBody>
                {sorted.map((r, idx) => {
                    const errorPct = pct(r.error_percentage);
                    return (
                        <TableRow key={idx}>
                            <TableCell>
                                <Typography variant="subtitle2">{fullName(r)}</Typography>
                            </TableCell>

                            <TableCell>
                                <Typography variant="body2" color="text.secondary">
                                    {r.graph_title}
                                </Typography>
                            </TableCell>

                            <TableCell>
                                <Chip size="small" label={r.weakest_topic ?? "-"} />
                            </TableCell>

                            <TableCell align="right">
                                <Chip
                                    size="small"
                                    label={String(r.error_count ?? "0")}
                                    color="error"
                                    variant="outlined"
                                />
                            </TableCell>

                            <TableCell align="right">
                                <Chip
                                    size="small"
                                    label={String(r.total_questions ?? "0")}
                                    color="default"
                                    variant="outlined"
                                />
                            </TableCell>

                            <TableCell>
                                <ScoreBar value={errorPct} />
                            </TableCell>
                        </TableRow>
                    );
                })}
            </TableBody>
        </Table>
    );
};

export default ProblematicTopicsTable;
