from app import app, db
from datetime import datetime
from models import db, User, Product, Wishlist, Favorite, CartItem, Order, Review, SupportRequest, Category

# Push an application context
with app.app_context():

# Drop all tables and create them again
    db.drop_all()
    db.create_all()

# Add sample data
    user = User(username='admin', email='admin@example.com', password='Dc12345')
    db.session.add(user)
    db.session.commit()
    
    
    # Create categories
    supermarket = Category(name='Supermarket')
    phones_tablets = Category(name='Phones and Tablets')
    electronics = Category(name='Electronics')
    sports = Category(name='Sports')
    computing = Category(name='Computing')

    # Add categories to session
    db.session.add_all([supermarket, phones_tablets, electronics, sports, computing])

    # Create products
    products = [
        Product(name="Cocksoda", description="Coca-cola Soda, 2 Liters", price=1.5, image_url="https://i.pinimg.com/564x/4e/a9/47/4ea94754274457a5ebab344b99b2acaa.jpg", star=3, category=supermarket),
        Product(name="Lato Milk", description="Lato Milk - 400g", price=13667, image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSDCMCiEJ1g2dPVRhtOP0ZM9SAa3DCkuRz74w&s", star=4, category=supermarket),
        Product(name="Omo Soap", description="Sunlight 2 In 1 Clean & Sakura Fresh Laundry Detergent Washing Powder - 1kg", price=5900, image_url="https://i.pinimg.com/564x/8f/87/3d/8f873de65a696b56e3052fd4766cabda.jpg", star=5, category=supermarket),
        Product(name="Pasta", description="Golda Penne Rigate - 500g", price=4.9, image_url="https://i.pinimg.com/564x/6b/4b/0d/6b4b0d39d3399afbc0367e37e530f82d.jpg", star=3, category="Supermarket"),
        Product(name="Sugar", description="Kinyara Sugar Kinyara Irresistibly Sweet Sugar - 1Kg", price=3.4, image_url="https://i.pinimg.com/564x/30/22/88/302288d5f278e7c6ae3d3453e3eeb3ce.jpg", star=4, category="Supermarket"),
        Product(name="Earphones", description="Generic Bluetooth Wireless Earphones With Charging Case", price=18.5, image_url="https://i.pinimg.com/564x/a6/93/ef/a693ef6706ceb3d2a535037812f923e1.jpg", star=1, category="Phones and Tablets"),
        Product(name="I phone 12", description="I phone 15 pro 2023 8gb ram 128 HD memory", price=2000, image_url="https://i.pinimg.com/564x/d1/49/fe/d149fe070890679fc07e4a4228b56606.jpg", star=4, category="Phones and Tablets"),
        Product(name="Nokia", description="Nokia 105 DS'' Dual Sim, FM Radio, Black", price=5.9, image_url="https://i.pinimg.com/564x/0d/e5/47/0de5476920098705dd0f3982890b310d.jpg", star=3, category="Phones and Tablets"),
        Product(name="Techno", description="Huawei Y5 Prime (2018)  2GB RAM 5000mAh - Green", price=330, image_url="https://i.pinimg.com/564x/b0/58/53/b0585324676742f81a3b1c8bf427516f.jpg", star=4, category="Phones and Tablets"),
        Product(name="Tablet", description="Note 4 Plus 4G LTE Tablet 4GB RAM 64GB Dual Sim", price=350, image_url="https://i.pinimg.com/236x/a1/5d/d9/a15dd968a1061092132584d82f1a0a6d.jpg", star=5, category="Phones and Tablets"),
        Product(name="Speaker", description="Golden Tech 5.1Sub-woofer - Black", price=455, image_url="https://i.pinimg.com/236x/f2/71/d4/f271d4b8bd4fb6ffe4ed880d8fa8d9c5.jpg", star=2, category="Electronics"),
        Product(name="Speaker", description="Generic GO 2 Speaker Wireless Portable Music Player IPX7", price=118.623, image_url="https://i.pinimg.com/236x/68/99/bf/6899bfc10ee4aec50a77bc7ba2e22d55.jpg", star=1, category="Electronics"),
        Product(name="Hisense", description="Hisense 55'' Inch 4K Ultra HD Smart TV - Black", price=2590, image_url="https://i.pinimg.com/236x/0a/d9/c8/0ad9c8cdba2fc39a36636de0c37545e4.jpg", star=3, category="Electronics"),
        Product(name="Samsung", description="Samsung 55'', Smart LED TV, Curve UHD TV4K - Black", price=5500, image_url="https://i.pinimg.com/236x/35/a0/5e/35a05ef5e8e5f548861f30abed0b3e2e.jpg", star=3, category="Electronics"),
        Product(name="Hisense", description="Hisense 55'' Inch 4K Ultra HD", price=550, image_url="https://i.pinimg.com/236x/33/53/69/335369c1a2c426958a222fa322cc5e8b.jpg", star=2, category="Electronics"),
        Product(name="Armband", description="Other Captain's - Black.", price=18, image_url="https://i.pinimg.com/236x/29/52/5b/29525b9ce65af681abb43cc21344f199.jpg", star=2, category="Sports"),
        Product(name="Generic Ball", description="Generic Spectacular Size 5 Football /Soccer Ball - White/Blue", price=35, image_url="https://i.pinimg.com/236x/73/6e/d9/736ed979cc1ddfb38671834e0c3a56b1.jpg", star=1, category="Sports"),
        Product(name="Ball", description="Spectacular Size 5 Football", price=30, image_url="https://i.pinimg.com/236x/27/af/67/27af676bb35e2e39fccb2dd67eff8aaf.jpg", star=4, category="Sports"),
        Product(name="Trainner", description="Generic Electric Muscle Training Abdominal Machine - Black", price=24.7, image_url="https://i.pinimg.com/736x/d5/c3/c3/d5c3c3e3f13902d310b2b45c29c22daf.jpg", star=4, category="Sports"),
        Product(name="Waist traner", description="Generic Waist Trainer Belt Waist Cincher Trimmer - Sport Girdle Belt", price=55.426, image_url="https://i.pinimg.com/236x/f7/fa/f9/f7faf982f6d66a3366fafdb07115db20.jpg", star=5, category="Sports"),
        Product(name="Dell", description="DELL DELL Refurbished  Core i5 4GB RAM 500GB ROM - Black", price=859.02, image_url="https://i.pinimg.com/236x/c3/79/8b/c3798b0707ea20ad11af9cf73228c3d6.jpg", star=2, category="Computing"),
        Product(name="Scan Disk", description="4 In 1 High Speed 128GB USB-3.0 Flash Drive-Gold", price=19, image_url="https://i.pinimg.com/236x/fc/eb/48/fceb48c1b5a8294cba3f6d02a86f3025.jpg", star=1, category="Computing"),
        Product(name="Hard Disk", description="Transcend 1TB Transcend Portable USB 3.0 Hard Disk - Black, Green", price=210, image_url="https://i.pinimg.com/236x/da/28/ec/da28ec2f6926fd5959915da0b3050490.jpg", star=5, category="Computing"),
        Product(name="Mouse", description="Generic 2.4 GHz Ultra Slim Wireless Mouse - Black", price=15, image_url="https://i.pinimg.com/236x/12/4c/06/124c06bae6de302c4b4e5cb352b1f3ef.jpg", star=4, category="Computing"),
        Product(name="Printer", description="Hp Deskjet All-in-One Inkjet Printer- White", price=175, image_url="https://i.pinimg.com/236x/4c/e3/fd/4ce3fde59ae258b2f94b0a15b1e37a20.jpg", star=3, category="Computing"),
            ]
    db.session.bulk_save_objects(products)
    db.session.commit()


    order = Order( 
        id='12345',
        user_id=user.id,
        product_id=products.id,
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


    cart_item = CartItem(user=user, product=products, quantity=2)
    db.session.add(cart_item)
    db.session.commit()

    print("Database seeded successfully!")
