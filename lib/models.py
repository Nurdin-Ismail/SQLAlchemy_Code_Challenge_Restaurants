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

    def get_reviews(self):
        
        return self.reviews
    
    def get_customers(self):
       
        return self.customers
    
    def all_reviews(self):
        
        reviews = [review.full_review() for review in self.get_reviews()]
        return reviews
    
    @classmethod
    def fanciest(cls):
        
        restaurant = session.query(cls).order_by(desc(cls.price)).first()
        return restaurant
    

    def __repr__(self):
        return f"Resturant name : {self.name}, price: {self.price}"
    
        
        
class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer(), primary_key = True)
    first_name = Column(String(), index = True)
    last_name = Column(String())
    
    reviews = relationship('Review', backref=backref('customer'))
    restaurants = relationship('Restaurant', secondary=restaurant_customer, back_populates='customers')
    

    def full_name(self):
        
        return f"{self.first_name} {self.last_name}"

    def get_reviews(self):
        
        return self.reviews
    
    def get_restaurants(self):
        
        return self.restaurants
    
    def favorite_restaurant(self):
        
        review = max(self.get_reviews(), key=lambda a: a.star_rating)
        return review.get_restaurant()
    
    def add_review(self, restaurant, rating):
        
        review = Review(
            customer_id=self.id,
            restaurant_id=restaurant.id,
            star_rating=rating)
        
        session = Session.object_session(self)
        session.add(review)
        session.commit()

    def delete_reviews(self, restaurant):
        
        session = Session.object_session(self)
        delete_q = Review.__table__.delete().where(Review.customer_id==self.id).where(Review.restaurant_id==restaurant.id)
        # reviews = session.query(Review).filter_by(customer_id=self.id, restaurant_id=restaurant.id)[0]
        session.execute(delete_q)
        session.commit()


    def __repr__(self):
        return f"Customers firstname : {self.first_name}, price: {self.last_name}"
    
        
    
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer(), primary_key = True)
    star_rating= Column(Integer())
    comment= Column(String())
    
    
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))

    
    @property
    def get_customer(self):
        return self.customer

    # @property
    def get_restaurant(self):
        return self.restaurant

    def __repr__(self):
        return (f"Customer({self.customer_id}) | Restaurant({self.restaurant_id}) | star-rating({self.star_rating}) |"
                f" {self.comment}: {self.star_rating} stars\n")
    
    



    
    
    
    