// src/components/ProductDetail.js

import React, { useEffect, useState } from 'react';
import { fetchProduct } from '../api';
import { useParams } from 'react-router-dom';

const ProductDetail = () => {
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadProduct = async () => {
            try {
                const data = await fetchProduct(id);
                setProduct(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        loadProduct();
    }, [id]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;
    if (!product) return <p>No product found</p>;

    return (
        <div>
            <h2>{product.product}</h2>
            <img src={product.image} alt={product.product} />
            <p>{product.description}</p>
            <p>Price: ${product.price}</p>
            <p>Rating: {product.star} stars</p>
        </div>
    );
};

export default ProductDetail;