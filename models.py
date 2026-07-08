from sqlalchemy import Column, Integer, Float, String
from database import Base

class RestaurantPrediction(Base):
    __tablename__ = "restaurant_predictions"

    id = Column(Integer, primary_key=True, index=True)

    seating_capacity = Column(Integer)
    average_meal_price = Column(Float)
    marketing_budget = Column(Float)
    weekend_reservations = Column(Integer)
    weekday_reservations = Column(Integer)
    social_media_followers = Column(Integer)
    predicted_revenue = Column(Float)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100), nullable=False)