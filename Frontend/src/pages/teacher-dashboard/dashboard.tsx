import "./dashboard.css"
import {useUser} from "../../context/user-context.tsx";
import {QueriesService} from "../../services/queries-service.ts";
import React, {useEffect, useState} from "react";
import {Cell, Legend, Pie, PieChart, ResponsiveContainer} from "recharts";
import AverageScoresTable from "../../components/queries/average-scores-table.tsx";
import TopStudentsTable from "../../components/queries/top-10-students-table.tsx";
import {forceManyBody} from "d3";
import {Typography} from "@mui/material";
import WorstFieldsTable from "../../components/queries/top-10-worst-fields-table.tsx";

const COLORS = [
    "#0088FE",
    "#00C49F",
    "#FFBB28",
    "#FF8042",
    "#A28BFF",
    "#FF6699",
    "#33CC99",
    "#9966FF",
    "#66CCFF",
    "#FFCC66",
];

export default function Dashboard() {

    const { user } = useUser();
    const service = new QueriesService();


    const [ctxData, setCtxData] = useState<any>([]);
    const [languageData, setLanguageData] = useState<any>([]);
    const [top10Students, setTop10Students] = useState<any>(null)
    const [topWorstFields, setTopWorstFields] = useState<any>(null)
    const [error, setError] = useState<string | null>(null);


    useEffect(() => {
        let mounted = true;
        async function load() {
            setError(null);
            try {
                const res = await service.testsByContext?.(user?.email ?? "");
                if (!mounted) return;
                setCtxData(Array.isArray(res) ? res : []);
            } catch (e: any) {
                if (!mounted) return;
                setError(e?.message ?? "Failed to load tests by context.");
            }

            try {
                const res = await service.testsByLanguage?.(user?.email ?? "");
                if (!mounted) return;
                setLanguageData(Array.isArray(res) ? res : []);
            } catch (e: any) {
                if (!mounted) return;
                setError(e?.message ?? "Failed to load tests by context.");
            }

            try {
                const res = await service.top10FromTeacher?.(user?.email ?? "");
                if (!mounted) return;
                setTop10Students(Array.isArray(res) ? res : []);
            } catch (e: any) {
                if (!mounted) return;
                setError(e?.message ?? "Failed to load top 10 students.");
            }

            try {
                const res = await service.topWorstFields?.(user?.email ?? "");
                if (!mounted) return;
                setTopWorstFields(Array.isArray(res) ? res : []);
            } catch (e: any) {
                if (!mounted) return;
                setError(e?.message ?? "Failed to load top 10 students.");
            }
        }
        load();
        return () => {
            mounted = false;
        };
    }, [user?.email]);


    const pieDataContext = ctxData
        .map((d) => ({ name: d.context || "unknown", value: Number(d.test_count || 0) }))
        .sort((a, b) => b.value - a.value);

    const pieDataLanguage = languageData
        .map((d) => ({ name: d.language || "unknown", value: Number(d.test_count || 0) }))
        .sort((a, b) => b.value - a.value);


    return (
        <div className="main-dashboard-container">
            <div className="pie-chart-wrapper-container">
                <div className="pie-chart-container">
                    <Typography variant="h2">Tests by Context</Typography>
                    {error && (
                        <div className="error-text" role="alert">
                            {error}
                        </div>
                    )}
                    {!error && (
                        <div style={{ width: "100%", height: 250 }}>
                            <ResponsiveContainer>
                                <PieChart>

                                    <Pie
                                        data={pieDataContext}
                                        dataKey="value"
                                        nameKey="name"
                                        cx="50%"
                                        cy="45%"
                                        outerRadius={80}
                                        label={(entry) => `${entry.name} (${entry.value})`}
                                        isAnimationActive
                                    >
                                        {pieDataContext.map((_, idx) => (
                                            <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
                                        ))}
                                    </Pie>
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                    )}
                </div>

                <div className="pie-chart-container">
                    <Typography variant="h2">Tests by Language</Typography>
                    {error && (
                        <div className="error-text" role="alert">
                            {error}
                        </div>
                    )}
                    {!error && (
                        <div style={{ width: "100%", height: 250 }}>
                            <ResponsiveContainer>
                                <PieChart>

                                    <Pie
                                        data={pieDataLanguage}
                                        dataKey="value"
                                        nameKey="name"
                                        cx="50%"
                                        cy="45%"
                                        outerRadius={80}
                                        label={(entry) => `${entry.name} (${entry.value})`}
                                        isAnimationActive
                                    >
                                        {pieDataLanguage.map((_, idx) => (
                                            <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
                                        ))}
                                    </Pie>
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                    )}
                </div>
            </div>

            <div className="table-container-wrapper">
                <div className="table-container">
                    <Typography variant="h2">Top 10 teachers students</Typography>
                    <TopStudentsTable rows={Array.isArray(top10Students) ? top10Students : []} />
                </div>

                <div className="table-container">
                    <Typography variant="h2">Worst answered fields</Typography>
                    <WorstFieldsTable rows={Array.isArray(topWorstFields) ? topWorstFields : []} />
                </div>
            </div>

        </div>
    );
}