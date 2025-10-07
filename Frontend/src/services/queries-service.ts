import api from "../config/axios-config.tsx";

export type QueryParams = Record<string, string | number | boolean | undefined>;

export class QueriesService {
    async execute(id: string, params: QueryParams) {
        switch (id) {
            case "average-scores":
                return this.averageScores(params);
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
}