import api from "../config/axios-config.tsx";

export type QueryParams = Record<string, string | number | boolean | undefined>;

export class QueriesService {
    async execute(id: string, params: QueryParams) {
        switch (id) {
            case "average-scores":
                return this.averageScores(params);
            case "problematic-topics":
                return this.problematicTopics(params)
            case "prerequisite-mastery":
                return this.prerequisiteMastery(params)
            default:
                throw new Error(`No service method registered for id "${id}".`);
        }
    }

    private async averageScores(params: QueryParams) {
        try {
            const cleanParams: Record<string, any> = {};
            for (const [key, value] of Object.entries(params)) {
                if (value !== undefined && value !== "") {
                    cleanParams[key] = value;
                }
            }

            const response = await api.post("queries/average-scores", cleanParams);

            if (response.status === 200) {
                return response.data;
            } else {
                throw new Error(`Unexpected status ${response.status}`);
            }
        } catch (error: any) {
            console.error("Error fetching average scores:", error);
            throw error;
        }
    }

    private async problematicTopics(params: QueryParams) {
        try {
            const cleanParams: Record<string, any> = {};
            for (const [key, value] of Object.entries(params)) {
                if (value !== undefined && value !== "") {
                    cleanParams[key] = value;
                }
            }

            const response = await api.post("queries/problematic-topics", cleanParams);

            if (response.status === 200) {
                return response.data;
            } else {
                throw new Error(`Unexpected status ${response.status}`);
            }
        } catch (error: any) {
            console.error("Error fetching average scores:", error);
            throw error;
        }
    }

    private async prerequisiteMastery(params: QueryParams) {
        try {
            const cleanParams: Record<string, any> = {};
            for (const [key, value] of Object.entries(params)) {
                if (value !== undefined && value !== "") {
                    cleanParams[key] = value;
                }
            }

            const response = await api.post("queries/prerequisite-mastery", cleanParams);

            if (response.status === 200) {
                return response.data;
            } else {
                throw new Error(`Unexpected status ${response.status}`);
            }
        } catch (error: any) {
            console.error("Error fetching average scores:", error);
            throw error;
        }
    }

    public async testsByContext(teacherMail: string) {
        const response = await api.get(`queries/test-count-by-context/${teacherMail}`);

        if (response.status === 200) {
            return response.data;
        } else {
            throw new Error(`Unexpected status ${response.status}`);
        }
    }

    public async testsByLanguage(teacherMail: string) {
        const response = await api.get(`queries/test-count-by-language/${teacherMail}`);

        if (response.status === 200) {
            return response.data;
        } else {
            throw new Error(`Unexpected status ${response.status}`);
        }
    }

    public async top10FromTeacher(teacherMail: string) {
        const response = await api.get(`queries/top-10-from-teacher/${teacherMail}`);

        if (response.status === 200) {
            return response.data;
        } else {
            throw new Error(`Unexpected status ${response.status}`);
        }
    }

    public async topWorstFields(teacherMail: string) {
        const response = await api.get(`queries/top-worst-fields/${teacherMail}`);

        if (response.status === 200) {
            return response.data;
        } else {
            throw new Error(`Unexpected status ${response.status}`);
        }
    }
    
}