import os
import sys
from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, verify_jwt_in_request
from werkzeug.security import generate_password_hash, check_password_hash
from models import  User, Product, Wishlist, Favorite, CartItem, Order, Review, SupportRequest, Category, db
import logging
from datetime import datetime
from flask_cors import CORS
from flask_mail import Mail, Message


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config["MAIL_SERVER"] = "live.smtp.mailtrap.io"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "your_email@gmail.com"
app.config["MAIL_PASSWORD"] = "your_password"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# postgresql://shopmate_bwbg_user:KsZRkRdSwBtbHiJ3LVSkle5v5LHA8zMg@dpg-cqoc95dsvqrc73feukd0-a.oregon-postgres.render.com/shopmate_bwbg



db.init_app(app)

mail = Mail(app)
jwt = JWTManager(app)
cors = CORS(app)
migrate = Migrate(app, db)



app.logger.setLevel(logging.DEBUG)


@app.route('/')
def index():
    return "Welcome to ShopMate!"



# Create a file handler
handler = logging.FileHandler('app.log')
handler.setLevel(logging.DEBUG)


# Create a formatter and attach it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


# Add the handler to the logger
app.logger.addHandler(handler)


#Authentication Endpoints    
auth_bp = Blueprint('auth_bp', __name__)

def jwt_required(fn):
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify(msg=str(e)), 401
    wrapper.__name__ = fn.__name__
    return wrapper

def admin_required(fn):
    def wrapper(*args, **kwargs):
        @jwt_required()
        def inner_wrapper():
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            if user and user.is_admin:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403
        return inner_wrapper()
    wrapper.__name__ = fn.__name__
    return wrapper

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400
    
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user is None or not user.check_password(password):
        return jsonify({"msg": "Invalid username or password"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(username=user.username, email=user.email), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(username=user.username, email=user.email, preferences=user.preferences), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    user = User.query.get(user_id)
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.preferences = data.get('preferences', user.preferences)
    db.session.commit()
    return jsonify(message="Profile updated successfully"), 200

@auth_bp.route('/wishlist', methods=['POST'])
@jwt_required
def add_to_wishlist():
    user_id = get_jwt_identity()
    product_id = request.json.get('product_id')
    wishlist_item = Wishlist(user_id=user_id, product_id=product_id)
    db.session.add(wishlist_item)
    db.session.commit()
    return jsonify(message="Product added to wishlist"), 201

@auth_bp.route('/favorites', methods=['POST'])
@jwt_required
def add_to_favorites():
    user_id = get_jwt_identity()
    product_id = request.json.get('product_id')
    favorite_item = Favorite(user_id=user_id, product_id=product_id)
    db.session.add(favorite_item)
    db.session.commit()
    return jsonify(message="Product added to favorites"), 201



# Define a logger
logger = logging.getLogger("my_logger")


# Create a Blueprint for logging and monitoring
logging_bp = Blueprint("logging_bp", __name__)

@logging_bp.route("/log", methods=["POST"])
@jwt_required
def log_event():
    # Log user actions, API requests, and errors
    event = request.json["event"]
    logger.info(event)
    return jsonify({"message": "Event logged"})

@logging_bp.route("/monitor", methods=["GET"])
@jwt_required
def monitor_system():
    # Monitor system health and identify issues
    system_status = {"status": "healthy"}
    logger.info("System health check")
    return jsonify(system_status)


# Products Blueprint
product_bp = Blueprint('products_bp', __name__)

# products
@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

@product_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict()), 200

@product_bp.route('/products', methods=['POST'])
@jwt_required
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        stock=data['stock'],
        category_id=data['category_id']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@product_bp.route('/products/<int:id>', methods=['PUT'])
@jwt_required
def update_product(id):
    data = request.get_json()
    product = Product.query.get_or_404(id)

    product.name = data['name']
    product.description = data['description']
    product.price = data['price']
    product.category_id = data['category_id']

    db.session.commit()
    return jsonify(product.to_dict()), 200

@product_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200


#categories
@product_bp.route('/categories', methods=['POST'])
@jwt_required
def create_category():
    data = request.get_json()
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.to_dict()), 201

@product_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories]), 200

@product_bp.route('/categories/<int:id>', methods=['PUT'])
@jwt_required
def update_category(id):
    data = request.get_json()
    category = Category.query.get(id)
    if not category:
        return jsonify({"message": "Category not found"}), 404
    category.name = data.get('name', category.name)
    db.session.commit()
    return jsonify(category.to_dict()), 200

@product_bp.route('/categories/<int:id>', methods=['DELETE'])
@jwt_required
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"message": "Category not found"}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200


# Reviews
@product_bp.route('/products/<int:product_id>/reviews', methods=['POST'])
@jwt_required
def create_review(product_id):
    data = request.get_json()
    new_review = Review(user_id=data['user_id'], product_id=product_id, rating=data['rating'], comment=data['comment'])
    db.session.add(new_review)
    db.session.commit()
    return jsonify(new_review.to_dict()), 201

@product_bp.route('/products/<int:product_id>/reviews', methods=['GET'])
def get_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    return jsonify([review.to_dict() for review in reviews]), 200

@product_bp.route('/reviews', methods=['POST'])
@jwt_required
def submit_review():
    data = request.get_json()
    new_review = Review(
        user_id=data['user_id'],
        product_id=data['product_id'],
        rating=data['rating'],
        comment=data['comment']
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify(new_review.to_dict()), 201


# Orders Blueprint
carts_bp = Blueprint('carts_bp', __name__)

# View cart items  
@carts_bp.route('/carts', methods=['GET'])
@jwt_required
def view_cart():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    return jsonify([item.to_dict() for item in cart_items]), 200

# Add item to cart
@carts_bp.route('/cart', methods=['POST'])
@jwt_required
def add_to_cart():
    data = request.get_json()
    user_id = get_jwt_identity()
    product_id = data['product_id']
    quantity = data['quantity']
    
    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
    
    db.session.add(cart_item)
    db.session.commit()
    return jsonify(cart_item.to_dict()), 201

# Update item quantity in cart
@carts_bp.route('/cart/<int:product_id>', methods=['PUT'])
@jwt_required
def update_cart(product_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first_or_404()
    cart_item.quantity = data['quantity']
    db.session.commit()
    return jsonify(cart_item.to_dict()), 200

# Remove item from cart
@carts_bp.route('/cart/<int:product_id>', methods=['DELETE'])
@jwt_required
def remove_from_cart(product_id):
    user_id = get_jwt_identity()
    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Item removed from cart'}), 200

# Checkout and create order
orders_bp = Blueprint('orders_bp', __name__)

@orders_bp.route('/checkout', methods=['POST'])
@jwt_required
def checkout():
    user_id = get_jwt_identity()
    data = request.get_json()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    shipping_address = data['shipping_address']
    
    if not cart_items:
        return jsonify({'message': 'Cart is empty'}), 400

     # Calculate taxes, discounts, and shipping costs
    total_amount = 0
    for item in cart_items:
        product = Product.query.get(item.product_id)
        total_amount += product.price * item.quantity

    taxes = total_amount * 0.1  # Example tax calculation (10%)
    shipping_cost = 10.00  # Flat shipping rate (example)
    discount = 0.0  # Example: no discount
    
    order_total = total_amount + taxes + shipping_cost - discount

    order = Order(
        user_id=user_id, 
        total_amount=total_amount,
        taxes=taxes,
        shipping_cost=shipping_cost,
        discount=discount,
        order_total=order_total, 
        status='Pending', 
        shipping_address=shipping_address,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
)
    db.session.add(order)
    db.session.commit()

     # Clear the cart
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Order placed successfully', 'order_id': order.id}), 201
@orders_bp.route('/orders', methods=['GET'])
@jwt_required
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders]), 200

@jwt_required
def get_order_history():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([order.to_dict() for order in orders]), 200

@orders_bp.route('/orders/<int:id>', methods=['GET'])
@jwt_required
def get_order_detail():
    order = Order.query.get_or_404(id)
    return jsonify(order.to_dict()), 200

@orders_bp.route('/orders/<int:id>/status', methods=['PUT'])
@jwt_required
def update_order_status(id):
    data = request.get_json()
    order = Order.query.get_or_404(id)
    order.status = data['status']
    order.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(order.to_dict()), 200

@orders_bp.route("/orders/<int:order_id>/track", methods=["GET"])
@jwt_required
def get_tracking_number(order_id):
    order = Order.query.get(order_id)
    return jsonify({"tracking_number": order.tracking_number})

@orders_bp.route('/orders/<int:id>/return', methods=['POST'])
@jwt_required
def handle_return(id):
    order = Order.query.get_or_404(id)
    order.status = 'Returned'
    order.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Order marked as returned'}), 200

@orders_bp.route('/orders/<int:id>/cancel', methods=['POST'])
@jwt_required
def handle_cancellation(id):
    order = Order.query.get_or_404(id)
    order.status = 'Cancelled'
    order.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Order marked as cancelled'}), 200

@orders_bp.route('/orders/<int:id>/shipping', methods=['POST'])
@jwt_required
def generate_shipping_notification(id):
    order = Order.query.get_or_404(id)
    # Logic for generating shipping notification, for example, sending an email to the user
    user_email = order.user.email  # Assuming User model has an email attribute
    product_name = order.product.name  # Assuming Product model has a name attribute

    # Here we could use an email service, for example, Flask-Mail or a third-party service like SendGrid
    send_email(
        to=user_email,
        subject='Your order has been shipped',
        body=f'Dear {order.user.username}, your order for {product_name} has been shipped!'
    )
    return jsonify({'message': 'Shipping notification generated'}), 200


@orders_bp.route("/orders/<int:order_id>/returns", methods=["POST"])
@jwt_required
def create_return(order_id):
    # Create a new return
    reason = request.json["reason"]
    # Send return notification using Flask-Mail
    msg = Message("Return Requested", sender="your_email@example.com", recipients=["customer_email@example.com"])
    msg.body = "We have received your return request."
    mail.send(msg)
    return jsonify({"message": "Return created"})


@orders_bp.route("/orders/<int:order_id>/returns/<int:return_id>", methods=["PUT"])
@jwt_required
def update_return_status(order_id, return_id):
    # Update return status
    status = request.json["status"]
    # Send return update notification using Flask-Mail
    msg = Message("Return Update", sender="your_email@example.com", recipients=["customer_email@example.com"])
    msg.body = "Your return has been updated."
    mail.send(msg)
    return jsonify({"message": "Return status updated"})


@orders_bp.route("/orders/<int:order_id>/cancel", methods=["POST"])
@jwt_required
def cancel_order(order_id):
    # Cancel an order
    # Send cancellation notification using Flask-Mail
    msg = Message("Order Cancelled", sender="your_email@example.com", recipients=["customer_email@example.com"])
    msg.body = "Your order has been cancelled."
    mail.send(msg)
    return jsonify({"message": "Order cancelled"})

def send_email(to, subject, body):
    # This is a placeholder for the actual email sending logic
   
    print(f"Sending email to {to} with subject '{subject}' and body '{body}'")


# Support Blueprint
support_bp = Blueprint('support_bp', __name__)

# Initialize Flask-Mail
mail = Mail()

@support_bp.route('/support', methods=['POST'])
@jwt_required
def create_support_request():
    user_id = get_jwt_identity()
    data = request.get_json()
    subject = data['subject']
    message = data['message']
    
    support_request = SupportRequest(
        user_id=user_id,
        subject=subject,
        message=message,
        status='Pending',
        created_at=datetime.utcnow()
    )
    db.session.add(support_request)
    db.session.commit()
    
    # Send an email to the support team
    send_support_email(subject, message)
    
    return jsonify(support_request.to_dict()), 201

@support_bp.route('/support', methods=['GET'])
@jwt_required
def get_support_requests():
    user_id = get_jwt_identity()
    support_requests = SupportRequest.query.filter_by(user_id=user_id).all()
    
    return jsonify([req.to_dict() for req in support_requests]), 200

@support_bp.route('/support/<int:id>', methods=['GET'])
@jwt_required
def get_support_request(id):
    support_request = SupportRequest.query.get_or_404(id)
    return jsonify(support_request.to_dict()), 200

@support_bp.route('/support/<int:id>', methods=['PUT'])
@jwt_required
def update_support_request(id):
    data = request.get_json()
    support_request = SupportRequest.query.get_or_404(id)
    support_request.status = data['status']
    db.session.commit()
    
    return jsonify(support_request.to_dict()), 200

def send_support_email(subject, message):
    msg = Message(subject, recipients=["support@yourdomain.com"])
    msg.body = message
    mail.send(msg)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(product_bp, url_prefix='/products')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(carts_bp, url_prefix='/carts')
app.register_blueprint(support_bp, url_prefix='/support')
app.register_blueprint(logging_bp, url_prefix='/logging')


#initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()