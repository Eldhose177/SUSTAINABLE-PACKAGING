from fastapi import FastAPI
from pydantic import BaseModel
from model import calculate_carbon_footprint

app = FastAPI()

# Define request structure
class UserInput(BaseModel):
    distance: float
    electricity: float
    food: str

@app.post("/calculate")
def calculate(data: UserInput):
    total_co2, recommendation = calculate_carbon_footprint(data.distance, data.electricity, data.food)
    return {"total_co2": total_co2, "recommendation": recommendation}

@app.get("/")
def home():
    return {"message": "Carbon Tracker API Running!"}
