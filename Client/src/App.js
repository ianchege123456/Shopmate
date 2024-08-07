import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './Context/AuthContext';
import { ProductContext } from './Context/ProductsContext';
import ProductsPage from './Pages/ProductsPage'
import { Register, Login } from './Components/Auth';
import HomePage from './Pages/Homepage';
import ProfilePage from './Pages/ProfilePage';

function App() {
    return (
        <AuthProvider>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/profile" element={<ProfilePage />} />
                    <Route path="/products" component={<ProductsPage />} />
                </Routes>
        </AuthProvider>
    );
}

export default App;
