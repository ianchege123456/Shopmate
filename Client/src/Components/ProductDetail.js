import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { fetchProduct, addToCart } from '../api'; // Import the addToCart function
import { useStateValue } from '../ContextAPI/StateProvider';

const ProductDetail = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [{ cart }, dispatch] = useStateValue();  // Using context for global state
  const navigate = useNavigate();

  useEffect(() => {
    const loadProduct = async () => {
      try {
        const data = await fetchProduct(id);
        setProduct(data);
      } catch (err) {
        setError('Failed to load product');
      } finally {
        setLoading(false);
      }
    };

    loadProduct();
  }, [id]);

  const handleAddToCart = async () => {
    if (!product) return;

    try {
      await addToCart(product.id, 1);  // Add product to cart with default quantity of 1

      // Update the global state
      dispatch({
        type: 'ADD_TO_CART',
        item: {
          id: product.id,
          name: product.product,
          price: product.price,
          quantity: 1,
          image: product.image_url
        }
      });

      // Navigate to /CartPage
      navigate('/CartPage');
    } catch (err) {
      setError('Failed to add item to cart');
      console.error('Add to cart failed', err);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!product) return <p>No product found</p>;

  return (
    <div className="container mx-auto p-4 grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="flex justify-center">
        <img 
          src={product.image_url} 
          alt={product.product} 
          className="w-full h-auto object-cover rounded-lg shadow-md" 
        />
      </div>
      <div>
        <h2 className="text-2xl font-bold mb-4">{product.product}</h2>
        <p className="mb-4">{product.description}</p>
        <p className="text-lg font-semibold mb-4">Price: ${product.price}</p>
        <p className="text-lg mb-4">Rating: {product.star} stars</p>
        
        <button 
          onClick={handleAddToCart} 
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
        >
          Add to Cart
        </button>
      </div>
    </div>
  );
};

export default ProductDetail;
