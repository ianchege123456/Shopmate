// src/components/ProductList.js

import React, { useEffect, useState } from 'react';
import { fetchProducts } from '../api';

const Product = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadProducts = async () => {
            try {
                const data = await fetchProducts({
                    category: 'Supermarket',
                    minPrice: 0,
                    maxPrice: 5000,
                    sortBy: 'price',
                    page: 1,
                    perPage: 10
                });
                setProducts(data.products);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        loadProducts();
    }, []);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div>
            <h2>Product List</h2>            
            <div className="product-grid">
                {products.map(product => (
                    <div key={product.id} className="product-card">
                        <img src={product.image} alt={product.product} />
                        <h3>{product.product}</h3>
                        <p>{product.description}</p>
                        <p>Price: ${product.price}</p>
                        <p>Rating: {product.star} stars</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Product;
