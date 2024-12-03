export interface User {
    id: number;
    first_name?: string;
    last_name?: string;
    email: string;
    role: 'teacher' | 'student' ;
    password?: string;
}



export interface Test {
    id?: number;
    title: string;
    author?: User;
    author_id?: number;
    graph_id?: number;
    questions: number[] | Question[]; // TODO FIX THIS
}



export interface Question {
    id: number;
    text: string;
    is_multichoice?: boolean;
    node_id?: number;
    answers: Answer[];
}


export interface Answer {
    id?: number;
    is_correct: boolean;
    text: string;
}


export interface Result {
    id: number;
    test: Test;
    student: User;
    student_answers: Record<number, number[]>;
    is_used: boolean;
    timestamp: string;
}


export interface Node {
    id?: number;
    title: string;
}

export interface Edge {
    id?: number;
    source: string;
    target: string;
}

export interface Graph {
    id?: number;
    title: string;
    nodes: Node[];
    edges: Edge[];
}

export interface TestSubmission {
    test_id: number,
    student_id: number,
    answers: number[]
}


