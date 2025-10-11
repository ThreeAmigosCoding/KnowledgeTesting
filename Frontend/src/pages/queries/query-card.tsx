import React, { useMemo, useState } from "react";
import {
    Box,
    Button,
    Card,
    CardContent,
    Stack,
    TextField,
    Typography,
    Tooltip,
    FormControlLabel,
    Checkbox,
} from "@mui/material";

export type ValueType = "string" | "number" | "boolean";

export type QueryParameter = {
    name: string;
    optional: boolean;
    label?: string;
    valueType: ValueType;
};

export type QueryDefinition = {
    id: string;
    name: string;
    description: string;
    parameters: QueryParameter[];
};

export type QueryParameterValueMap = Record<string, string | number | boolean | undefined>;

type Props = QueryDefinition & {
    onExecute: (id: string, values: QueryParameterValueMap) => void | Promise<void>;
};

const toTitle = (s: string) =>
    s.replace(/[-_]/g, " ").replace(/\b\w/g, (m) => m.toUpperCase());

const QueryCard: React.FC<Props> = ({ id, name, description, parameters, onExecute }) => {
    const [values, setValues] = useState<QueryParameterValueMap>({});
    const [touched, setTouched] = useState<Record<string, boolean>>({});
    const [submitting, setSubmitting] = useState(false);

    const requiredMissing = useMemo(() => {
        return parameters
            .filter((p) => !p.optional)
            .filter((p) => {
                const v = values[p.name];
                if (p.valueType === "string") return v === undefined || String(v).trim() === "";
                if (p.valueType === "number") return v === undefined || v === "" || Number.isNaN(Number(v));
                if (p.valueType === "boolean") return v === undefined;
                return false;
            })
            .map((p) => p.name);
    }, [parameters, values]);

    const hasErrors = requiredMissing.length > 0;

    const handleChange =
        (p: QueryParameter) => (e: React.ChangeEvent<HTMLInputElement>) => {
            setTouched((t) => ({ ...t, [p.name]: true }));

            if (p.valueType === "boolean") {
                setValues((v) => ({ ...v, [p.name]: e.target.checked }));
                return;
            }
            if (p.valueType === "number") {
                const raw = e.target.value;
                setValues((v) => ({ ...v, [p.name]: raw === "" ? undefined : Number(raw) }));
                return;
            }

            // string
            setValues((v) => ({ ...v, [p.name]: e.target.value }));
        };

    const showError = (p: QueryParameter) => !p.optional && touched[p.name] && requiredMissing.includes(p.name);

    const getHelperText = (p: QueryParameter) => {
        if (showError(p)) return "This field is required.";
        if (p.valueType === "number" && touched[p.name] && values[p.name] !== undefined && Number.isNaN(Number(values[p.name] as number))) {
            return "Enter a valid number.";
        }
        return " ";
    };

    const reset = () => {
        setValues({});
        setTouched({});
    };

    const onRun = async () => {
        setTouched((t) => {
            const all: Record<string, boolean> = { ...t };
            parameters.forEach((p) => (all[p.name] = true));
            return all;
        });

        if (hasErrors) return;

        setSubmitting(true);
        try {
            await onExecute(id, values);
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <Card className="query-card" variant="outlined">
            <CardContent sx={{ width: "100%" }}>
                <Box mb={2}>
                    <Typography variant="h6" fontWeight={700}>
                        {name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        {description}
                    </Typography>
                </Box>

                <Stack direction="row" spacing={2} useFlexGap flexWrap="wrap">
                    {parameters.map((p) => {
                        const label = p.label ?? toTitle(p.name);
                        const commonProps = {
                            key: p.name,
                            name: p.name,
                        };

                        if (p.valueType === "boolean") {
                            return (
                                <FormControlLabel
                                    key={p.name}
                                    control={
                                        <Checkbox
                                            checked={Boolean(values[p.name])}
                                            onChange={handleChange(p)}
                                        />
                                    }
                                    label={label + (p.optional ? " (optional)" : " *")}
                                />
                            );
                        }

                        return (
                            <TextField
                                {...commonProps}
                                label={label + (p.optional ? "" : " *")}
                                type={p.valueType === "number" ? "number" : "text"}
                                value={values[p.name] ?? ""}
                                onChange={handleChange(p)}
                                error={showError(p)}
                                helperText={getHelperText(p)}
                                size="small"
                            />
                        );
                    })}
                </Stack>

                <Stack direction="row" spacing={1} mt={2}>
                    <Tooltip title={hasErrors ? "Fill all required fields to run" : "Execute this query"}>
            <span>
              <Button variant="contained" onClick={onRun} disabled={submitting || hasErrors}>
                {submitting ? "Running..." : "Run"}
              </Button>
            </span>
                    </Tooltip>

                    <Button variant="text" onClick={reset} disabled={submitting}>
                        Reset
                    </Button>
                </Stack>
            </CardContent>
        </Card>
    );
};

export default QueryCard;