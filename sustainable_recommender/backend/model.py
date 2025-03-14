import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Sample dataset of sustainable lifestyle options
lifestyle_data = np.array([
    [1, 0, 0],  # Public Transport
    [0, 1, 0],  # Solar Energy
    [0, 0, 1],  # Vegan Diet
    [0.5, 0.5, 0]  # Hybrid Lifestyle
])

recommendations = ["Use public transport!", "Switch to solar energy!", "Try a vegan diet!", "Hybrid lifestyle is great!"]

def calculate_carbon_footprint(distance, electricity, food):
    # Carbon emission factors (kg CO2 per activity)
    car_emission = distance * 0.25  
    electricity_emission = electricity * 0.6  
    food_emission = {"Vegan": 2, "Vegetarian": 3, "Mixed (Meat & Veg)": 5, "Meat-heavy": 7}[food]

    total_co2 = car_emission + electricity_emission + food_emission

    # Convert user data into a vector for similarity
    user_vector = np.array([[car_emission, electricity_emission, food_emission]])
    similarities = cosine_similarity(user_vector, lifestyle_data)

    best_match = np.argmax(similarities)
    return total_co2, recommendations[best_match]
