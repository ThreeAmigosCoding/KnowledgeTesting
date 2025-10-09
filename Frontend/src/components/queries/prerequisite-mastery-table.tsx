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

type TopicRow = {
  avg_prereq_performance?: string | number; // 0–100 or 0–1
  avg_topic_performance?: string | number;  // 0–100 or 0–1
  first_name?: string;
  last_name?: string;
  prerequisites_count?: string | number;
  topic?: string;
  weak_prerequisites?: string;
};

const toNumber = (v: string | number | undefined) => {
  if (v === undefined || v === null || v === "") return NaN;
  return typeof v === "string" ? parseFloat(v) : v;
};

// Accepts either 0–100 or 0–1 and returns clamped 0–100
const pct = (v: string | number | undefined) => {
  const n = toNumber(v);
  if (!Number.isFinite(n)) return 0;
  const asPct = n <= 1 ? n * 100 : n;
  return Math.max(0, Math.min(100, asPct));
};

const fullName = (r: TopicRow) =>
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

const PrerequisiteMasteryTable: React.FC<{ rows: TopicRow[] }> = ({ rows }) => {
  if (!rows?.length) {
    return (
      <Typography variant="body2" sx={{ color: "text.secondary" }}>
        No results to display.
      </Typography>
    );
  }

  // Sort by weakest topics first (lowest avg_topic_performance)
  const sorted = [...rows].sort(
    (a, b) => pct(a.avg_topic_performance) - pct(b.avg_topic_performance)
  );

  return (
    <Table size="small" aria-label="Topics & Prerequisites Table">
      <TableHead>
        <TableRow>
          <TableCell>Student</TableCell>
          <TableCell>Topic</TableCell>
          <TableCell>Weak Prerequisites</TableCell>
          <TableCell align="right">Prereq Count</TableCell>
          <TableCell>Avg Prereq Performance</TableCell>
          <TableCell>Avg Topic Performance</TableCell>
        </TableRow>
      </TableHead>

      <TableBody>
        {sorted.map((r, idx) => {
          const prereqPct = pct(r.avg_prereq_performance);
          const topicPct = pct(r.avg_topic_performance);

          return (
            <TableRow key={idx}>
              <TableCell>
                <Typography variant="subtitle2">{fullName(r)}</Typography>
              </TableCell>

              <TableCell>
                <Typography variant="body2" color="text.secondary">
                  {r.topic ?? "-"}
                </Typography>
              </TableCell>

              <TableCell>
                <Chip size="small" label={r.weak_prerequisites ?? "-"} />
              </TableCell>

              <TableCell align="right">
                <Chip
                  size="small"
                  label={String(r.prerequisites_count ?? "0")}
                  variant="outlined"
                />
              </TableCell>

              <TableCell>
                <ScoreBar value={prereqPct} />
              </TableCell>

              <TableCell>
                <ScoreBar value={topicPct} />
              </TableCell>
            </TableRow>
          );
        })}
      </TableBody>
    </Table>
  );
};

export default PrerequisiteMasteryTable;
