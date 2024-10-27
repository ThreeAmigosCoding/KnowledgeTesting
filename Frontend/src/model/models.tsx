export interface User {
    id: string;
    firstName: string;
    lastName: string;
    email: string;
    role: 'teacher' | 'student' | 'expert';
    password: string;
}



export interface Test {
    id: string;
    title: string;
    author: User;
    questions: Question[];
}



export interface Question {
    id: string;
    text: string;
    answers: Answer[];
}


export interface Answer {
    id: string;
    isCorrect: boolean;
    text: string;
}


export interface Result {
    id: string;
    test: Test;
    student: User;
    answers: Answer[];
}
