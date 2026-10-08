import streamlit as st
import requests
import os

# Backend API URL
# Local Docker: http://backend:8000
# Render: set API_URL environment variable
API_URL = os.getenv("API_URL", "http://backend:8000")

st.title("🚗 EV Purchase Prediction")

st.write(
    "Enter customer details to predict whether they will purchase an electric vehicle."
)

# Customer ID
customer_id = st.number_input(
    "Customer ID",
    min_value=0,
    value=668665,
    step=1
)

age = st.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=30
)

income = st.number_input(
    "Annual Income (USD)",
    min_value=0.0,
    value=50000.0
)

commute = st.number_input(
    "Daily Commute (km)",
    min_value=0.0,
    value=20.0
)

cars = st.number_input(
    "Number of Cars Owned",
    min_value=0,
    max_value=10,
    value=1
)

charging_home = st.number_input(
    "Charging Stations Near Home",
    min_value=0,
    value=2
)

charging_work = st.number_input(
    "Charging Stations Near Work",
    min_value=0,
    value=2
)

environmental = st.number_input(
    "Environmental Concern Level",
    min_value=0.0,
    max_value=10.0,
    value=4.0
)

gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

city = st.selectbox(
    "City Type",
    ["Rural", "Suburban", "Urban"]
)

car_type = st.selectbox(
    "Current Car Type",
    ["Sedan", "SUV", "Hatchback"]
)

home_charging = st.selectbox(
    "Home Charging Possible",
    ["Yes", "No"]
)

subsidy = st.selectbox(
    "Subsidy Available",
    ["Yes", "No"]
)

anxiety = st.selectbox(
    "Range Anxiety Level",
    ["Low", "Medium", "High"]
)


if st.button("Predict"):

    data = {
        "id": customer_id,
        "Age": age,
        "Annual_Income_USD": income,
        "Daily_Commute_km": commute,
        "Number_of_Cars_Owned": cars,
        "Charging_Stations_Near_Home": charging_home,
        "Charging_Stations_Near_Work": charging_work,
        "Environmental_Concern_Level": environmental,
        "Gender": gender,
        "City_Type": city,
        "Current_Car_Type": car_type,
        "Home_Charging_Possible": home_charging,
        "Subsidy_Available": subsidy,
        "Range_Anxiety_Level": anxiety
    }

    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=data
        )

        if response.status_code == 200:

            result = response.json()

            st.success(result)

        else:

            st.error(f"API Error: {response.status_code}")
            st.write(response.text)

    except requests.exceptions.RequestException as e:

        st.error("Could not connect to the backend.")
        st.write(str(e))