from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from sqlalchemy.orm import Session
import joblib
import numpy as np

from database import engine, Base, get_db
from schemas import PredictionInput, LoginInput
from crud import (
    save_prediction,
    get_all_predictions,
    login_user
)

app = FastAPI(title="Restaurant Revenue Prediction API")

# Session
app.add_middleware(
    SessionMiddleware,
    secret_key="restaurant123"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
Base.metadata.create_all(bind=engine)

# ML Model
model = joblib.load("restaurant_revenue_model.pkl")

# Static
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):

    if "user" not in request.session:
        return RedirectResponse(url="/")

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={}
    )


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@app.post("/login")
async def login(
    request: Request,
    data: LoginInput,
    db: Session = Depends(get_db)
):

    user = login_user(db, data.username, data.password)

    if user:

        request.session["user"] = user.username

        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": "Invalid Username or Password"
        }
    )
# ================= DASHBOARD =================

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):

    if "user" not in request.session:
        return RedirectResponse(url="/")

    predictions = get_all_predictions(db)

    total = len(predictions)

    if total > 0:
        revenues = [p.predicted_revenue for p in predictions]
        average = round(sum(revenues) / total, 2)
        highest = max(revenues)
        lowest = min(revenues)
    else:
        average = highest = lowest = 0

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "total_predictions": total,
            "average_revenue": average,
            "highest_revenue": highest,
            "lowest_revenue": lowest
        }
    )


# ================= HOME PAGE =================

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):

    if "user" not in request.session:
        return RedirectResponse(url="/")

    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={}
    )


# ================= PREDICT PAGE =================

@app.get("/predict-page", response_class=HTMLResponse)
async def predict_page(request: Request):

    if "user" not in request.session:
        return RedirectResponse(url="/")

    return templates.TemplateResponse(
        request=request,
        name="predict.html",
        context={}
    )


# ================= HISTORY PAGE =================

@app.get("/history", response_class=HTMLResponse)
async def history(request: Request, db: Session = Depends(get_db)):

    if "user" not in request.session:
        return RedirectResponse(url="/")

    predictions = get_all_predictions(db)

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "predictions": predictions
        }
    )
# ================= LOGOUT =================

@app.get("/logout")
async def logout(request: Request):

    request.session.clear()

    return RedirectResponse(url="/", status_code=303)


# ================= PREDICT API =================

@app.post("/predict")
def predict(data: PredictionInput, db: Session = Depends(get_db)):

    features = np.array([[
        data.seating_capacity,
        data.average_meal_price,
        data.marketing_budget,
        data.social_media_followers,
        data.weekend_reservations,
        data.weekday_reservations
    ]])

    prediction = float(model.predict(features)[0])

    save_prediction(db, data, prediction)

    return {
        "predicted_revenue": prediction
    }


# ================= HISTORY API =================

@app.get("/predictions")
def get_predictions(db: Session = Depends(get_db)):
    return get_all_predictions(db)