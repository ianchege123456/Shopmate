import React from 'react';
import ProductList from '../Components/Product';
import Header from '../Components/Header'
import Home from '../Components/Home'

const HomePage = () => {
  return (
    <div className="container">
      <Header />
      <Home />
      <ProductList />
    </div>
  );
};

export default HomePage;
