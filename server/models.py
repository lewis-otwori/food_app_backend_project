from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.orm import validates


db = SQLAlchemy()


class Owner(db.Model):
    __tablename__ = 'owner'
    owner_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    image = db.Column(db.String)

    locations = db.relationship('Location', backref='owner')
    restaurants= db.relationship('Restaurant', back_populates='owner')
    
   
class Location(db.Model):
    __tablename__ = 'location'
    location_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, ForeignKey('owner.owner_id'))
    name = db.Column(db.String)
    delivery_fee = db.Column(db.Integer)

    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.restaurant_id'))
    restaurant = db.relationship('Restaurant', backref='location')


class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, ForeignKey('menu.menu_id'))
    # customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    total_price = db.Column(db.Integer)
    order_date_and_time = db.Column(db.DateTime)
    address = db.Column(db.String)
    payment_method = db.Column(db.String)

    deliveries = db.relationship('Deliveries', backref='order')
    # menu = db.relationship('Menu', backref='menu_items')
    # customer = db.relationship('Customers', backref='orders')

class Driver(db.Model):
    __tablename__ = 'driver'
    driver_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    phone_number = db.Column(db.String)
    image = db.Column(db.String)
    current_location = db.Column(db.String)

    deliveries = db.relationship('Deliveries', backref='driver')


class Deliveries(db.Model):
    __tablename__ = 'deliveries'
    delivery_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey('order.order_id')) 
    driver_id = db.Column(db.Integer, ForeignKey('driver.driver_id'))
    delivery_date_and_time = db.Column(db.DateTime)
    dispatch = db.Column(db.Boolean, default=False)
    delivered = db.Column(db.Boolean, default=False)  
  
    
class Payment(db.Model):
    __tablename__ = 'payment'
    payment_id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.restaurant_id'))
    payment_type = db.Column(db.String)
    payment_amount = db.Column(db.Integer)
    payment_date_and_time = db.Column(db.Time)
    payment_status = db.Column(db.String)

class Customers(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    user_name = db.Column(db.String)
    password = db.Column(db.String)
    phone_number = db.Column(db.String)
    image = db.Column(db.String)

    # orders = db.relationship('Order', backref='customer')
    customerReviews = db.relationship('CustomerReviews', backref='customer')
    user = db.relationship('User', backref='customer', uselist=False)

class CustomerReviews(db.Model):
    __tablename__ = 'customerReviews'
    customerReview_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, ForeignKey('customers.customer_id'))
    rating = db.Column(db.Integer)
    review_comment = db.Column(db.String)
    review_date = db.Column(db.DateTime)
    
class RestaurantReviews(db.Model):
    __tablename__ = 'restaurantReviews'
    restaurantReview_id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.restaurant_id'))
    rating = db.Column(db.Integer)
    review_comment = db.Column(db.String)
    review_date = db.Column(db.DateTime)
    
class MenuReviews(db.Model):
    __tablename__ = 'menuReviews'
    restaurantReview_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, ForeignKey('menu.menu_id'))
    rating = db.Column(db.Integer)
    review_comment = db.Column(db.String)
    review_date = db.Column(db.DateTime)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    restaurant_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer,ForeignKey('owner.owner_id'))
    restaurant_name = db.Column(db.String)
    contact_number = db.Column(db.String)
    opening_hours = db.Column(db.Time)
    closing_hours = db.Column(db.Time)
    image = db.Column(db.String)
    payment_method = db.Column(db.String)
    
   
    menus = db.relationship('Menu', backref='restaurant')
    owner = db.relationship('Owner', back_populates='restaurants')
  



class Menu(db.Model):
    __tablename__ = 'menu'
    menu_id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.restaurant_id'))
    menu_name = db.Column(db.String)
    description = db.Column(db.String)
    prices = db.Column(db.Integer)
    
    menu_items = db.relationship('Order', backref='menu')
  

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    type = db.Column(db.Boolean, default=False)  
    blocked = db.Column(db.String)
    activity = db.Column(db.String)

class Favourites(db.Model):
    __tablename__ ='favourite'
    favourite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.user_id'))
    menu_id = db.Column(db.Integer, ForeignKey('menu.menu_id'))

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, ForeignKey('customers.customer_id'))
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.restaurant_id'))
    owner_id = db.Column(db.Integer, ForeignKey('owner.owner_id'))
    name = db.Column(db.String)
    password = db.Column(db.String)
    image = db.Column(db.String)
    
class SuperAdmin(db.Model):
    __tablename__ = 'superadmin'
    superadmin_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, ForeignKey('customers.customer_id'))
    restaurant_id = db.Column(db.Integer, ForeignKey('restaurant.restaurant_id'))
    owner_id = db.Column(db.Integer, ForeignKey('owner.owner_id'))
    name = db.Column(db.String)
    password = db.Column(db.String)
    image = db.Column(db.String)
    
    @validates("password")
    def validate_password(self, key, password):
        if password and len(password) > 100:
            raise ValueError('User password is not valid, please try again')
        return password

from marshmallow import Schema, fields
class OwnerSchema(Schema):
    owner_id = fields.Integer()
    name = fields.String()
    email = fields.String()
    password = fields.String()
    image = fields.String()

class LocationSchema(Schema):
    location_id = fields.Integer()
    owner_id = fields.Integer()
    name = fields.String()
    delivery_fee = fields.String()

class OrderSchema(Schema):
    order_id = fields.Integer()
    menu_id = fields.Integer(dump_only=True)
    total_price = fields.Integer()
    order_date_and_time = fields.DateTime()
    address = fields.String()
    payment_method = fields.String()


class DriverSchema(Schema):
    driver_id = fields.Integer()
    name = fields.String()
    email = fields.String()
    password = fields.String()
    phone_number = fields.String()
    image = fields.String()
    current_location = fields.String()


class DeliveriesSchema(Schema):
    delivery_id = fields.Integer()
    order_id = fields.Integer()
    driver_id = fields.Integer()
    delivery_date_and_time = fields.DateTime()
    dispatch = fields.Boolean()
    delivered = fields.Boolean()

class PaymentSchema(Schema):
    payment_id = fields.Integer()
    restaurant_id = fields.Integer()
    payment_type = fields.String()
    payment_amount = fields.Integer()
    payment_date_and_time = fields.DateTime()
    payment_status = fields.String()

class CustomersSchema(Schema):
    customer_id = fields.Integer()
    user_name = fields.String()
    password = fields.String()
    phone_number = fields.String()
    image = fields.String()

class CustomerReviewsSchema(Schema):
    customerReview_id = fields.Integer()
    customer_id = fields.Integer()
    rating = fields.Integer()
    review_comment = fields.String()
    review_date = fields.DateTime()

class RestaurantReviewsSchema(Schema):
    restaurantReview_id = fields.Integer()
    restaurant_id = fields.Integer()
    rating = fields.Integer()
    review_comment = fields.String()
    review_date = fields.DateTime()
    
class MenuReviewsSchema(Schema):
    menuReview_id = fields.Integer()
    menu_id = fields.Integer()
    rating = fields.Integer()
    review_comment = fields.String()
    review_date = fields.DateTime()
    
class MenuSchema(Schema):
    menu_id = fields.Integer()
    restaurant_id = fields.Integer()
    menu_name = fields.String()
    description = fields.String()
    prices = fields.Integer()
    
class RestaurantSchema(Schema):
    restaurant_id = fields.Integer()
    owner_id = fields.Integer()
    restaurant_name = fields.String()
    contact_number = fields.String()
    opening_hours = fields.Time()
    closing_hours = fields.Time()
    image = fields.String()
    payment_method = fields.String()
    menus = fields.Nested(MenuSchema, many=True)

class UserSchema(Schema):
    user_id = fields.Integer()
    user_name = fields.String()
    email = fields.String()
    password = fields.String()
    type = fields.Boolean()
    blocked = fields.String()
    activity = fields.String()
    
class FavouritesSchema(Schema):
  favourite_id = fields.Integer
  user_id = fields.Integer
  menu_id = fields.Integer

class AdminSchema(Schema):
    admin_id = fields.Integer()
    customer_id = fields.Integer()
    restaurant_id = fields.Integer()
    owner_id = fields.Integer()
    name = fields.String()
    password = fields.String()
    
class SuperAdminSchema(Schema):
    superadmin_id = fields.Integer()
    customer_id = fields.Integer()
    restaurant_id = fields.Integer()
    owner_id = fields.Integer()
    name = fields.String()
    password = fields.String()
