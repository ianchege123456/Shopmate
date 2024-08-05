import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ProductContext } from '../context/ProductContext';

import { Register, Login } from './Components/Auth';
import HomePage from './Pages/Homepage';
import ProfilePage from './Pages/ProfilePage';

function App() {
    return (
        <AuthProvider>
            <Router>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/profile" element={<ProfilePage />} />
                    <Route path="/products" component={<ProductsPage />} />
                </Routes>
            </Router>
        </AuthProvider>
    );
}

export default App;
