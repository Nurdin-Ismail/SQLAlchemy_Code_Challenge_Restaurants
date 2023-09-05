from faker import  Faker
import random


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Customer, Restaurant, Review

if __name__ == '__main__':
    engine = create_engine('sqlite:///restaurants.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Customer).delete()
    session.query(Review).delete()
    session.query(Restaurant).delete()

    fake = Faker()

    # ------------------------ Populate customer table --------------------------
    customers = []
    for i in range(10):
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        session.add(customer)
        session.commit()
        customers.append(customer)
        

    # ----------------------- Populate restaurants table -----------------------
    restaurants = []
    for i in range(10):
        restaurant = Restaurant(
            name=fake.unique.name(),
            price=random.randint(4000,10000)
        )
        session.add(restaurant)
        session.commit()
        restaurants.append(restaurant)

    # ------------------------ Populate reviews table ----------------------------
    reviews = []
    for restaurant in restaurants:
        for i in range(random.randint(1,5)):
            customer = random.choice(customers)
            if restaurant not in customer.restaurants:

                customer.restaurants.append(restaurant)
                session.add(customer)
                session.commit()
            
            review = Review(
                star_rating=random.randint(0, 10),
                comment=fake.sentence(),
                restaurant_id=restaurant.id,
                customer_id=customer.id,
            )

            reviews.append(review)

    session.bulk_save_objects(reviews)
    session.commit()
    session.close()