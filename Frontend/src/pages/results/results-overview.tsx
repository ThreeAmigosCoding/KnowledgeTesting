import {Box, Button, Card, CardContent, Typography, useTheme} from "@mui/material";
import './results.css'
import {useEffect, useState} from "react";
import {Result} from "../../model/models.tsx";
import api from "../../config/axios-config.tsx";
import {formatTimestamp} from "../../utils/converter.tsx";
import {useNavigate, useParams} from "react-router-dom";
import {useUser} from "../../context/user-context.tsx";
import { LocalizationProvider } from '@mui/x-date-pickers-pro/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers-pro/AdapterDayjs';
import { DateRangePicker } from '@mui/x-date-pickers-pro/DateRangePicker';
import dayjs, { Dayjs } from 'dayjs';


export default function ResultsOverview() {

    const navigate = useNavigate();
    const [results, setResults] = useState<Result[]>([]);
    const { user } = useUser();

    const { testId } = useParams<{testId : string; }>();
    const [testTitle, setTestTitle] = useState<string>('');

    const [dateRange, setDateRange] = useState<[Dayjs | null, Dayjs | null]>([null, null]);

    const theme = useTheme();

    useEffect(() => {
        fetchResults().then(() => {})
    }, []);

    const fetchResults = async () => {
        if (!user) return;
        if (user.role === "student") {
            try {
                const studentId = user.id;
                const response = await api.get<Result[]>(`get-results`, {
                    params: { studentId: studentId }
                });
                if (response.status === 200) {
                    setResults(response.data);
                }
            }
            catch (error) {
                alert(error)
            }
        }
        else {
            try {
                const response = await api.get<Result[]>(`get-results`, {
                    params: { testId: testId }
                });
                if (response.status === 200) {
                    setResults(response.data);
                    if (!testTitle) {
                        setTestTitle(response.data[0].test.title);
                    }
                }
            }
            catch (error) {
                alert(error)
            }
        }
    }

    const handleDateChange = (newValue: [Dayjs | null, Dayjs | null]) => {
        setDateRange(newValue);
    };

    const isWithinDateRange = (timestamp: string): boolean => {
        if (!dateRange[0] || !dateRange[1]) return false;
        const startDate = dateRange[0];
        const endDate = dateRange[1];
        const resultDate = dayjs(timestamp);
        return resultDate.isAfter(startDate) && resultDate.isBefore(endDate);
    };

    const openResult = (resultId: number) => {
        navigate(`/result/${resultId}`);
    };

    const generateGraph = async () => {
        if (!user) return;
        if (user.role === "teacher") {
            if (!dateRange[0] || !dateRange[1]) {
                alert("Please select a valid date range.");
                return;
            }

            try {
                const requestBody = {
                    test_id: testId,
                    start_date: dateRange[0].valueOf() / 1000,
                    end_date: dateRange[1].valueOf() / 1000,
                };

                const response = await api.post(`generate-graph`, requestBody);
                if (response.status === 200) {
                    alert('Graph generated successfully!');
                }
            } catch (error) {
                alert(error);
            }
        }
    }

    return (
        <Box className='main-container'>
            <Box className='content'>
                {user && user.role === "teacher" ? (
                    <Typography variant='h1' sx={{textAlign: 'center'}}>Results for: {testTitle}</Typography>
                ) : (
                    <Typography variant='h1' sx={{textAlign: 'center'}}>Results</Typography>
                )}
                {user && user.role === "teacher" &&
                    <Box className='date-pickers-container'>
                        <LocalizationProvider dateAdapter={AdapterDayjs}>
                            <DateRangePicker
                                localeText={{ start: 'Start date', end: 'End date' }}
                                value={dateRange}
                                onChange={handleDateChange}
                            />
                        </LocalizationProvider>
                        <Button
                            variant="contained"
                            color="primary"
                            disabled={!dateRange[0] || !dateRange[1]}
                            sx={{
                                fontSize: "medium",
                                textTransform: "capitalize",
                                maxWidth: "300px"
                            }}
                            onClick={generateGraph}
                        >
                            Generate Graph
                        </Button>
                    </Box>
                }
                <Box className="results-container">
                    {results.map((result) => user && user.role === "teacher" ? (
                        <Card
                            key={result.id}
                            className="result-card"
                            sx={{ backgroundColor: isWithinDateRange(result.timestamp) ? theme.palette.success.light : "" }}
                            onClick={() => openResult(result.id as number)}>
                            <CardContent className="result-card-content">
                                <Typography variant="h2">
                                    {result.student?.first_name} {result.student?.last_name}
                                </Typography>
                                <Typography variant="h3">
                                    {formatTimestamp(result.timestamp)}
                                </Typography>
                            </CardContent>
                        </Card>
                    ) : (
                        <Card
                            key={result.id}
                            className="result-card"
                            onClick={() => openResult(result.id as number)}>
                            <CardContent className="result-card-content">
                                <Typography variant="h2">{result.test.title}</Typography>
                                <Typography variant="h3">
                                    Author: {result.test?.author?.first_name} {result.test?.author?.last_name}
                                </Typography>
                                <Typography variant="h4">
                                    Questions: {result.test.questions.length}
                                </Typography>
                                <Typography variant="h5">
                                    {formatTimestamp(result.timestamp)}
                                </Typography>
                            </CardContent>
                        </Card>
                    ))}
                </Box>
            </Box>
        </Box>
    )
}