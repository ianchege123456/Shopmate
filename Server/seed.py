from app import app, db
from datetime import datetime
from models import db, User, Product, Wishlist, Favorite, CartItem, Order, Review, SupportRequest, Category

# Push an application context
with app.app_context():

# Drop all tables and create them again
    db.drop_all()
    db.create_all()

# Add sample data
    user = User(username='admin', email='admin@example.com', password='password')
    db.session.add(user)
    db.session.commit()
    
    
    product = Product(name='Test Product', description='This is a test product.', price=10.0)
    db.session.add(product)
    db.session.commit()


    order = Order( 
        id='12345',
        user_id=user.id,
        product_id=product.id,
        total_amount=0.0,
        taxes=0.0,
        shipping_cost=0.0,
        discount=0.0,
        order_total=0.0,
        shipping_address='123 Main St, Anytown, USA',  # Provide a valid shipping address
        status='Processing',
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        quantity=1
    )
    db.session.add(order)
    db.session.commit()


    cart_item = CartItem(user=user, product=product, quantity=2)
    db.session.add(cart_item)
    db.session.commit()

    print("Database seeded successfully!")
