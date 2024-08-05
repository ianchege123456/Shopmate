// src/pages/ProductsPage.js
import React from 'react';
import ProductList from '../components/Product/ProductList';
import Pagination from '../components/Pagination';
import Filter from '../components/Filter';

const ProductsPage = () => {
  return (
    <div>
      <Filter />
      <ProductList />
      <Pagination />
    </div>
  );
};

export default ProductsPage;
