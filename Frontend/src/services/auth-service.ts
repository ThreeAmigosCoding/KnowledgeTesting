import {jwtDecode} from "jwt-decode"
import {User} from "../model/models.tsx";

interface CustomJwtPayload {
    email: string;
    sub: string;
    role: string;
    [key: string]: any;
}


export function userFromToken(token: string) : User {
    const decodedToken = jwtDecode<CustomJwtPayload>(token);
    return <User>{email: decodedToken.email, id: Number(decodedToken.sub), role: decodedToken.role}
}