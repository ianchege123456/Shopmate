// src/components/ProductList.js

import React, { useEffect, useState } from 'react';
import { fetchProducts } from '../api';
import { Link } from 'react-router-dom';

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
            <h2 className="text-2xl font-bold mb-4">Product List</h2>            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {products.map(product => (
                    <div key={product.id} className="bg-white p-4 rounded-lg shadow-md">
                        <img src={product.image_url} alt={product.product} className="h-40 w-full object-cover rounded-t-lg mb-4" />
                        <h3 className="text-lg font-semibold">{product.product}</h3>
                        <p className="text-gray-600">{product.description}</p>
                        <p className="text-lg font-bold mt-2">Price: ${product.price}</p>
                        <p className="text-yellow-500 mt-1">Rating: {product.star} stars</p>
                        <Link to={`/products/${product.id}`}>
                            <button className="mt-4 w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
                                View Product
                            </button>
                        </Link>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Product;
