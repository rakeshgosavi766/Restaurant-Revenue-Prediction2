from pydantic import BaseModel

class PredictionInput(BaseModel):
    seating_capacity: int
    average_meal_price: float
    marketing_budget: float
    weekend_reservations: int
    weekday_reservations: int
    social_media_followers: int


class PredictionResponse(BaseModel):
    predicted_revenue: float


class PredictionOut(BaseModel):
    id: int
    seating_capacity: int
    average_meal_price: float
    marketing_budget: float
    weekend_reservations: int
    weekday_reservations: int
    predicted_revenue: float
    social_media_followers: int

    class Config:
        from_attributes = True


class LoginInput(BaseModel):
    username: str
    password: str