import React from "react";

const OrderConfirmation = ({ order }) => {
  return (
    <div className="order-confirmation">
      <h2>Thank you for your order!</h2>
      <p>Your order number is: {order.id}</p>
      <div className="order-summary">
        <h3>Order Summary</h3>
        {order.items.map((item) => (
          <div key={item.id} className="order-item">
            <p>{item.name}</p>
            <p>{item.quantity} x ${item.price}</p>
          </div>
        ))}
      </div>
      <p>Total: ${order.total}</p>
    </div>
  );
};

export default OrderConfirmation;
