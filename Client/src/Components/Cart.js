import React from 'react'
import { useStateValue } from "../ContextAPI/StateProvider";
import "./Cart.css";

function Cart() {
    const [{ cart, discount, shipping }, dispatch] = useStateValue();
  

  const calculateSubtotal = () => {
    return cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  };

  const calculateTotal = () => {
    const subtotal = calculateSubtotal();
    return subtotal - discount + shipping;
  };

  const handleQuantityChange = (id, quantity) => {
    dispatch({
      type: "UPDATE_QUANTITY",
      id,
      quantity: parseInt(quantity),
    });
  };

  const handleRemoveFromCart = (id) => {
    dispatch({
      type: "REMOVE_FROM_CART",
      id: id,
    });
  };
  return (
    <div className="cart">
      <h2>Your Shopping Cart</h2>
      {cart.length === 0 ? (
        <p>Your cart is empty</p>
      ) : (
        <>
          {cart.map((item) => (
            <div key={item.id} className="cart-item">
              <p>{item.name}</p>
              <p>${item.price}</p>
              <input
                type="number"
                value={item.quantity}
                min="1"
                onChange={(e) => handleQuantityChange(item.id, e.target.value)}
              />
              <button onClick={() => handleRemoveFromCart(item.id)}>Remove</button>
            </div>
          ))}
          <div className="cart-summary">
            <p>Subtotal: ${calculateSubtotal()}</p>
            <p>Discount: -${discount}</p>
            <p>Shipping: ${shipping}</p>
            <h3>Total: ${calculateTotal()}</h3>
          </div>
        </>
      )}
    </div>
  );
};

export default Cart