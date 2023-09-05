from sqlalchemy import create_engine;
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, backref
from sqlalchemy.ext.declarative import declarative_base
import random
from faker import Faker
fake = Faker()


Base = declarative_base()

engine = create_engine('sqlite:///restaurants.db')


restaurant_customer = Table(
    'restaurant_customer',
    Base.metadata,
    Column('customer_id', ForeignKey('customers.id'), primary_key=True),
    Column('restaurant_id', ForeignKey('restaurants.id'), primary_key=True),
    extend_existing=True,
)



class Restaurant(Base):
    __tablename__ = "restaurants"
    
    id = Column(Integer(), primary_key = True)
    name = Column(String(), index = True)
    price = Column(Integer())
    
    reviews = relationship('Review', backref=backref('restaurant'))
    customers = relationship('Customer', secondary= restaurant_customer, back_populates='restaurants')

    def __repr__(self):
        return f"Resturant name : {self.name}, price: {self.price}"
    
        
        
class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer(), primary_key = True)
    first_name = Column(String(), index = True)
    last_name = Column(String())
    
    reviews = relationship('Review', backref=backref('customer'))
    restaurants = relationship('Restaurant', secondary=restaurant_customer, back_populates='customers')

    def __repr__(self):
        return f"Customers firstname : {self.first_name}, price: {self.last_name}"
    
        
    
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer(), primary_key = True)
    star_rating= Column(Integer())
    comment= Column(String())
    
    
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))

    
    
    def get_customer(self):
        return self.customer

    # @property
    def get_restaurant(self):
        return self.restaurant

    def __repr__(self):
        return (f"Customer({self.customer_id}) | Restaurant({self.restaurant_id}) | star-rating({self.star_rating}) |"
                f" {self.comment}: {self.star_rating} stars\n")
    
    



    
    
    
    