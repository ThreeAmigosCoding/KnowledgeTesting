import {
    Chip,
    Table,
    TableHead,
    TableRow,
    TableCell,
    TableBody,
    Typography,
} from "@mui/material";
import React from "react";

type WorstFieldsRow = {
    difficulty?: string;
    incorrect_answers?: string | number;
    field?: string;
    test_title?: string;
};

const toNumber = (v: string | number | undefined) => {
    if (v === undefined || v === null || v === "") return 0;
    const n = typeof v === "string" ? parseFloat(v) : v;
    return Number.isFinite(n) ? n : 0;
};

const WorstFieldsTable: React.FC<{ rows: WorstFieldsRow[] }> = ({ rows }) => {
    if (!rows?.length) {
        return (
            <Typography variant="body2" sx={{ color: "text.secondary" }}>
                No results to display.
            </Typography>
        );
    }

    // Sort descending by incorrect answers
    const sorted = [...rows].sort(
        (a, b) => toNumber(b.incorrect_answers) - toNumber(a.incorrect_answers)
    );

    return (
        <Table size="small" aria-label="Worst Fields Table">
            <TableHead>
                <TableRow>
                    <TableCell>Field</TableCell>
                    <TableCell>Test Title</TableCell>
                    <TableCell>Difficulty</TableCell>
                    <TableCell align="right">Incorrect Answers</TableCell>
                </TableRow>
            </TableHead>

            <TableBody>
                {sorted.map((r, idx) => {
                    const incorrect = toNumber(r.incorrect_answers);

                    return (
                        <TableRow key={idx}>
                            <TableCell>
                                <Typography variant="subtitle2">
                                    {r.field ?? "—"}
                                </Typography>
                            </TableCell>

                            <TableCell>
                                <Typography variant="body2">
                                    {r.test_title ?? "—"}
                                </Typography>
                            </TableCell>

                            <TableCell>
                                <Typography variant="body2">
                                    {r.difficulty ?? "—"}
                                </Typography>
                            </TableCell>

                            <TableCell align="right">
                                <Chip size="small" label={String(incorrect)} />
                            </TableCell>
                        </TableRow>
                    );
                })}
            </TableBody>
        </Table>
    );
};

export default WorstFieldsTable;
