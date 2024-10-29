export interface User {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    role: 'teacher' | 'student' | 'expert';
    password: string;
}



export interface Test {
    id: number;
    title: string;
    author: User;
    questions: number[];
}



export interface Question {
    id: number;
    text: string;
    answers: Answer[];
}


export interface Answer {
    id: number;
    is_correct: boolean;
    text: string;
}


export interface Result {
    id: number;
    test: Test;
    student: User;
    answers: Answer[];
}
