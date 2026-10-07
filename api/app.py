from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import sys

from api import preprocessing

# The pickle was created with the module name "preprocessing"
sys.modules["preprocessing"] = preprocessing

from api.preprocessing import dropper, ordinalencoder, OHEEncoder


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="EV Purchase Prediction API",
    description="API for predicting whether a customer will buy an electric vehicle",
    version="1.0"
)


# --------------------------------------------------
# Load trained ML pipeline
# --------------------------------------------------

model = joblib.load("api/ev_purchase_model.pkl")


# --------------------------------------------------
# Input schema
# --------------------------------------------------

class EVInput(BaseModel):
    id:int
    Age: int
    Annual_Income_USD: float
    Daily_Commute_km: float
    Number_of_Cars_Owned: int

    Charging_Stations_Near_Home: int
    Charging_Stations_Near_Work: int

    Environmental_Concern_Level: float
    Gender: str
    City_Type: str
    Current_Car_Type: str

    Home_Charging_Possible: str
    Subsidy_Available: str
    Range_Anxiety_Level: str


# --------------------------------------------------
# Home endpoint
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "EV Purchase Prediction API is running"
    }


# --------------------------------------------------
# Prediction endpoint
# --------------------------------------------------

@app.post("/predict")
def predict(data: EVInput):

    # Convert Pydantic data into dictionary
    input_dict = data.model_dump()

    # Convert dictionary into DataFrame
    input_data = pd.DataFrame([input_dict])

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Get probability of class 1 (Yes)
    probability = model.predict_proba(input_data)[0][1]

    # Convert prediction into readable output
    result = "Yes" if prediction == 1 else "No"

    return {
        "prediction": result,
        "probability": round(float(probability), 4)
    }