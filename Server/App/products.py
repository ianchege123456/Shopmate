from flask import Blueprint, request, jsonify
from . import db
from .models import Product

bp = Blueprint('products', __name__, url_prefix='/api/products')

@bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.as_dict() for product in products]), 200

@bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.as_dict()), 200

@bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product(name=data['name'], description=data['description'], price=data['price'])
    db.session.add(product)
    db.session.commit()
    return jsonify(product.as_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get_or_404(id)
    product.name = data['name']
    product.description = data['description']
    product.price = data['price']
    db.session.commit()
    return jsonify(product.as_dict()), 200

@bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200
