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

type AverageScoreRow = {
    avg_score_percent?: string | number;
    best_score_percent?: string | number;
    first_name?: string;
    last_name?: string;
    tests_taken?: string | number;
};

const pct = (v: string | number | undefined) => {
    if (v === undefined || v === null || v === "") return 0;
    const n = typeof v === "string" ? parseFloat(v) : v;
    return Number.isFinite(n) ? Math.max(0, Math.min(100, n)) : 0;
};

const fullName = (r: AverageScoreRow) =>
    [r.first_name, r.last_name].filter(Boolean).join(" ");

const ScoreBar: React.FC<{ value: number; label?: string }> = ({ value}) => (
    <Stack direction="row" spacing={1} alignItems="center" sx={{ minWidth: 180 }}>
        <Box sx={{ flex: 1 }}>
            <LinearProgress variant="determinate" value={value} />
        </Box>
        <Typography variant="body2" sx={{ width: 50, textAlign: "right" }}>
            {value.toFixed(1)}%
        </Typography>
    </Stack>
);

const AverageScoresTable: React.FC<{ rows: AverageScoreRow[] }> = ({ rows }) => {
    if (!rows?.length) {
        return (
            <Typography variant="body2" sx={{ color: "text.secondary" }}>
                No results to display.
            </Typography>
        );
    }

    const sorted = [...rows].sort((a, b) => {
        const ad = pct(a.avg_score_percent);
        const bd = pct(b.avg_score_percent);
        if (bd !== ad) return bd - ad;
        return pct(b.best_score_percent) - pct(a.best_score_percent);
    });

    return (
        <Table size="small" aria-label="Average Scores Table">
            <TableHead>
                <TableRow>
                    <TableCell>Student</TableCell>
                    <TableCell align="right">Tests Taken</TableCell>
                    <TableCell>Average Score</TableCell>
                    <TableCell>Best Score</TableCell>
                </TableRow>
            </TableHead>

            <TableBody>
                {sorted.map((r, idx) => {
                    const avg = pct(r.avg_score_percent);
                    const best = pct(r.best_score_percent);

                    return (
                        <TableRow key={idx}>
                            <TableCell>
                                <Typography variant="subtitle2">{fullName(r)}</Typography>
                            </TableCell>

                            <TableCell align="right">
                                <Chip size="small" label={String(r.tests_taken ?? "0")} />
                            </TableCell>

                            <TableCell>
                                <ScoreBar value={avg} />
                            </TableCell>

                            <TableCell>
                                <ScoreBar value={best} />
                            </TableCell>
                        </TableRow>
                    );
                })}
            </TableBody>
        </Table>
    );
};

export default AverageScoresTable;