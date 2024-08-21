
import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Product from './Components/Product';
import ProductDetail from './Components/ProductDetail';
import Home from './Components/Home';
import RegisterForm from './Components/Auth/RegisterForm';
import LoginForm from './Components/Auth/LoginForm';
import Cart from './Components/Cart';
import CartPage from './Pages/CartPage';
// import OrderPage from './Pages/OrderPage';
import Checkout from './Components/Checkout';
import Header from './Components/Header'
import Profile from './Components/Profile';
import Support from "./Components/Support";
import Private from './Components/PrivateRoute';

function App() {
  return (
    
      <Router>
        <Header />
        <Home />
          <Routes>
            
            <Route path="/register" element={<RegisterForm />} />
            <Route path="/checkout" element={<Checkout />} />
            <Route path="/Cart" element={<Cart />} />
            <Route path="/CartPage" element={<CartPage />} />
            <Route path="/login" element={<LoginForm />} />
            <Route path="/products/:id" element={<ProductDetail />} />
            <Route path="/" element={<Product />}>
            <Route path='/support' element={<Support/>} />
            <Route path='/profile' element={<Profile/>}/>
            <Route path='*' element={<Private/>}/>
              
            </Route>

          </Routes>             
        
      </Router>
    
  );
};


export default App;
