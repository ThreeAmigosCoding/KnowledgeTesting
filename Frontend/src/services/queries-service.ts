export class QueriesService {

    async execute(id: string, params: Record<string, any>) {
        switch (id) {
            case "get-all-students":
                return this.getAllStudents(params);
            default:
                throw new Error(`No service method registered for id "${id}".`);
        }
    }

    private async getAllStudents(params: Record<string, any>) {
        const qs = new URLSearchParams();
        Object.entries(params).forEach(([k, v]) => {
            if (v === undefined || v === "") return;
            qs.append(k, String(v));
        });

        const url = `/api/students${qs.toString() ? `?${qs.toString()}` : ""}`;
        const res = await fetch(url, { method: "GET" });

        if (!res.ok) {
            const text = await res.text().catch(() => "");
            throw new Error(`API ${res.status} ${res.statusText}${text ? `: ${text}` : ""}`);
        }

        return res.json();
    }
}