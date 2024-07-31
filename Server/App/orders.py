from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db
from .models import Order, User, Product, Cart

bp = Blueprint('orders', __name__, url_prefix='/api/orders')

# Helper function to calculate the total amount of an order
def calculate_total_amount(cart_items):
    total = 0
    for item in cart_items:
        product = Product.query.get(item.product_id)
        total += product.price * item.quantity
    return total

# Route to place an order
@bp.route('/', methods=['POST'])
@jwt_required()
def place_order():
    user_id = get_jwt_identity()['id']
    user = User.query.get_or_404(user_id)
    
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({'message': 'Cart is empty'}), 400

    total_amount = calculate_total_amount(cart_items)
    order = Order(user_id=user.id, total_amount=total_amount)
    db.session.add(order)
    db.session.commit()
    
    # Clear the cart
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()
    
    return jsonify({'message': 'Order placed successfully', 'order_id': order.id}), 201

# Route to view order history
@bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()['id']
    orders = Order.query.filter_by(user_id=user_id).all()
    
    orders_list = []
    for order in orders:
        order_data = {
            'id': order.id,
            'created_at': order.created_at,
            'total_amount': order.total_amount,
            'status': order.status
        }
        orders_list.append(order_data)
    
    return jsonify(orders_list), 200

# Route to get order details by order ID
@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_order(id):
    user_id = get_jwt_identity()['id']
    order = Order.query.filter_by(id=id, user_id=user_id).first_or_404()
    
    order_data = {
        'id': order.id,
        'created_at': order.created_at,
        'total_amount': order.total_amount,
        'status': order.status
    }
    
    return jsonify(order_data), 200

# Route to update order status (admin only)
@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_order_status(id):
    # Assuming there's a mechanism to check if the user is an admin
    if not get_jwt_identity().get('is_admin'):
        return jsonify({'message': 'Permission denied'}), 403

    order = Order.query.get_or_404(id)
    data = request.get_json()
    order.status = data.get('status', order.status)
    db.session.commit()
    
    return jsonify({'message': 'Order status updated successfully'}), 200

# Route to handle returns or cancellations
@bp.route('/<int:id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(id):
    user_id = get_jwt_identity()['id']
    order = Order.query.filter_by(id=id, user_id=user_id).first_or_404()
    
    if order.status not in ['Pending', 'Processing']:
        return jsonify({'message': 'Order cannot be cancelled'}), 400

    order.status = 'Cancelled'
    db.session.commit()
    
    return jsonify({'message': 'Order cancelled successfully'}), 200
