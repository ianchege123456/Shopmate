import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    const login = async (email, password) => {
        try {
            const response = await axios.post('/api/auth/login', { email, password });
            setUser(response.data.user);
            localStorage.setItem('token', response.data.token);
        } catch (error) {
            console.error('Login failed:', error);
        }
    };

    const register = async (username, email, password) => {
        try {
            const response = await axios.post('/api/auth/register', { username, email, password });
            setUser(response.data.user);
            localStorage.setItem('token', response.data.token);
        } catch (error) {
            console.error('Registration failed:', error);
        }
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('token');
    };

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            // Fetch user data with token
            axios.get('/api/auth/me', { headers: { Authorization: `Bearer ${token}` } })
                .then(response => setUser(response.data.user))
                .catch(() => logout());
        }
    }, []);

    return (
        <AuthContext.Provider value={{ user, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
