import {createContext, useState, useContext, ReactNode, useEffect} from 'react';
import {User} from "../model/models.tsx";
import {userFromToken} from "../services/auth-service.ts";


interface UserContextProps {
    user: User | null;
    setUser: (user: User | null) => void;
}

const UserContext = createContext<UserContextProps>({
    user: null,
    setUser: () => {}
});

export const UserProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(() => {
        const token = localStorage.getItem('token');
        return token ? userFromToken(token) : null;
    });

    useEffect(() => {
        if (!user) {
            localStorage.removeItem('token');
        }
    }, [user]);

    return (
        <UserContext.Provider value={{ user, setUser }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = () => useContext(UserContext);
