import {
    Box,
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

type TopStudentsRow = {
    avg_score_percent?: string | number;
    first_name?: string;
    last_name?: string;
};

const pct = (v: string | number | undefined) => {
    if (v === undefined || v === null || v === "") return 0;
    const n = typeof v === "string" ? parseFloat(v) : v;
    return Number.isFinite(n) ? Math.max(0, Math.min(100, n)) : 0;
};

const fullName = (r: TopStudentsRow) =>
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

const TopStudentsTable: React.FC<{ rows: TopStudentsRow[] }> = ({ rows }) => {
    if (!rows?.length) {
        return (
            <Typography variant="body2" sx={{ color: "text.secondary" }}>
                No results to display.
            </Typography>
        );
    }

    const sorted = [...rows].sort((a, b) => pct(b.avg_score_percent) - pct(a.avg_score_percent));

    return (
        <Table size="small" aria-label="Top Students Table">
            <TableHead>
                <TableRow>
                    <TableCell>Student</TableCell>
                    <TableCell>Average Score</TableCell>
                </TableRow>
            </TableHead>

            <TableBody>
                {sorted.map((r, idx) => {
                    const avg = pct(r.avg_score_percent);

                    return (
                        <TableRow key={idx}>
                            <TableCell>
                                <Typography variant="subtitle2">{fullName(r)}</Typography>
                            </TableCell>
                            <TableCell>
                                <ScoreBar value={avg} />
                            </TableCell>
                        </TableRow>
                    );
                })}
            </TableBody>
        </Table>
    );
};

export default TopStudentsTable;
