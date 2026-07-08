from sqlalchemy.orm import Session
from models import RestaurantPrediction
from models import User

def save_prediction(db: Session, data, prediction: float):
    new_prediction = RestaurantPrediction(
        seating_capacity=data.seating_capacity,
        average_meal_price=data.average_meal_price,
        marketing_budget=data.marketing_budget,
        weekend_reservations=data.weekend_reservations,
        weekday_reservations=data.weekday_reservations,
        predicted_revenue=prediction,
        social_media_followers=data.social_media_followers
    )

    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    return new_prediction


def get_all_predictions(db: Session):
    return db.query(RestaurantPrediction).all()
from models import User

def login_user(db, username, password):
    return db.query(User).filter(
        User.username == username,
        User.password == password
    ).first()