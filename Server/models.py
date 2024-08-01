from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    cart_items = db.relationship('CartItem', backref='user', lazy=True)
    preferences = db.Column(db.Text, nullable=True)
    wishlists = db.relationship('Wishlist', backref='user', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)
        

    serialize_only = ('id', 'username', 'email', 'created_at')

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address, "Invalid email address"
        return address
    
    @validates('username')
    def validate_username(self, key, username):
        assert len(username) >= 3, "Username must be at least 3 characters long"
        return username


    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at
        }
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'
        
class Category(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

    serialize_only = ('id', 'name')
    
    @validates('name')
    def validate_name(self, key, name):
        assert len(name) >= 2, "Category name must be at least 2 characters long"
        return name


class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    orders = db.relationship('Order', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)

    serialize_only = ('id', 'name', 'description', 'price', 'category_id', 'created_at')

    @validates('name')
    def validate_name(self, key, name):
        assert len(name) >= 2, "Product name must be at least 2 characters long"
        return name

    @validates('price')
    def validate_price(self, key, price):
        assert price >= 0, "Price must be non-negative"
        return price

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'created_at': self.created_at
        }
        
class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CartItem(db.Model, SerializerMixin):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    serialize_only = ('id', 'user_id', 'product_id', 'quantity', 'created_at')
    
    @validates('quantity')
    def validate_quantity(self, key, quantity):
        assert quantity > 0, "Quantity must be positive"
        return quantity

class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    taxes = db.Column(db.Float, nullable=False)
    shipping_cost = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    order_total = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='Processing')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    serialize_only = ('id', 'user_id', 'total_amount', 'taxes', 'shipping_cost', 'discount', 'order_total', 'shipping_address', 'status', 'created_at')
    
    @validates('total_amount', 'taxes', 'shipping_cost', 'discount', 'order_total')
    def validate_non_negative(self, key, value):
        assert value >= 0, f"{key} must be non-negative"
        return value

    @validates('shipping_address')
    def validate_shipping_address(self, key, address):
        assert len(address) > 0, "Shipping address cannot be empty"
        return address


    def to_dict(self):
        return {
                
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    @validates('rating')
    def validate_rating(self, key, rating):
        assert 1 <= rating <= 5, "Rating must be between 1 and 5"
        return rating

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at
        }
class SupportRequest(db.Model, SerializerMixin):
    __tablename__ = 'support_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    serialize_only = ('id', 'user_id', 'subject', 'message', 'status', 'created_at', 'updated_at')

    @validates('subject')
    def validate_subject(self, key, subject):
        assert len(subject) > 0, "Subject cannot be empty"
        return subject

    @validates('message')
    def validate_message(self, key, message):
        assert len(message) > 0, "Message cannot be empty"
        return message