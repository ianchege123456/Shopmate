import React, { useEffect, useState } from 'react';
import { fetchCartItems, fetchProduct } from '../api';

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [discount, setDiscount] = useState(0); // Assuming discount is fetched or calculated elsewhere
  const [shipping, setShipping] = useState(10); // Default shipping cost

  useEffect(() => {
    const loadCartItems = async () => {
      try {
        const items = await fetchCartItems();
        const productDetailsPromises = items.map(item => fetchProduct(item.product_id));
        const products = await Promise.all(productDetailsPromises);

        // Combine cart items with product details
        const combinedItems = items.map((item, index) => ({
          ...item,
          ...products[index],
          quantity: item.quantity
        }));

        setCartItems(combinedItems);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadCartItems();
  }, []);

  const calculateSubtotal = () => {
    return cartItems.reduce((sum, item) => {
      const price = parseFloat(item.price) || 0;  // Ensure price is a number
      const quantity = parseInt(item.quantity, 10) || 0;  // Ensure quantity is an integer
      return sum + price * quantity;
    }, 0);
  };

  const calculateTotal = () => {
    const subtotal = calculateSubtotal();
    return subtotal - discount + shipping;
  };

  const handleQuantityChange = (id, quantity) => {
    // Implement quantity change logic
  };

  const handleRemoveFromCart = (id) => {
    // Implement remove from cart logic
  };

  if (loading) return <p className="text-center mt-4">Loading...</p>;
  if (error) return <p className="text-center text-red-500 mt-4">Error: {error}</p>;

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Your Shopping Cart</h2>
      {cartItems.length === 0 ? (
        <p className="text-center">Your cart is empty</p>
      ) : (
        <>
          <div className="space-y-4">
            {cartItems.map((item) => (
              <div key={item.id} className="flex items-center justify-between p-4 bg-gray-100 rounded-md shadow">
                <div>
                  <p className="font-semibold">{item.name}</p>
                  <p>${item.price.toFixed(2)}</p>
                </div>
                <input
                  type="number"
                  value={item.quantity}
                  min="1"
                  onChange={(e) => handleQuantityChange(item.id, e.target.value)}
                  className="w-16 p-2 border rounded-md"
                />
                <button
                  onClick={() => handleRemoveFromCart(item.id)}
                  className="text-red-500 hover:text-red-700 font-semibold"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>

          <div className="mt-6 p-4 bg-gray-100 rounded-md shadow">
            <p className="font-semibold">Subtotal: ${calculateSubtotal().toFixed(2)}</p>
            <p>Discount: -${discount.toFixed(2)}</p>
            <p>Shipping: ${shipping.toFixed(2)}</p>
            <h3 className="text-xl font-bold">Total: ${calculateTotal().toFixed(2)}</h3>
          </div>
        </>
      )}
    </div>
  );
};

export default Cart;
