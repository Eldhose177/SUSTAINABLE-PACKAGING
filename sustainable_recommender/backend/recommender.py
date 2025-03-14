import requests
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to load large dataset (For now, simulate with a small example)
def load_data():
    # Replace this with actual large datasets or CSV files
    data = {
        'Material': ['Plastic', 'Cardboard', 'Biodegradable', 'Glass', 'Aluminum'],
        'Carbon_Footprint': [8.5, 3.0, 1.0, 5.0, 4.5],  # Carbon footprint in kg CO2
        'Recyclable': [1, 1, 1, 1, 0],  # 1 = recyclable, 0 = not recyclable
        'Water_Usage': [20, 5, 2, 15, 10],  # Water usage in liters
        'Cost': [0.5, 0.2, 0.7, 1.0, 0.8],  # Cost per unit (arbitrary units)
    }
    
    df = pd.DataFrame(data)
    return df

# Function to get carbon intensity data from an external API (simulated)
def get_carbon_intensity():
    # Example: Carbon Intensity API (real API call would look like this)
    url = "https://api.carbonintensity.org.uk/intensity"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Here, you would process the data accordingly (this is a sample)
        return data
    else:
        return {"error": "Failed to fetch data from API"}

# Function to preprocess and compute recommendations using Cosine Similarity
def recommend_sustainable_packaging(user_data, df):
    # User input vector: (Carbon footprint, Recyclable, Water usage, Cost)
    user_vector = np.array([
        user_data['Carbon_Footprint'],
        user_data['Recyclable'],
        user_data['Water_Usage'],
        user_data['Cost']
    ]).reshape(1, -1)
    
    # Create feature matrix for the packaging data
    packaging_data = df[['Carbon_Footprint', 'Recyclable', 'Water_Usage', 'Cost']].values
    
    # Calculate cosine similarity
    similarity_scores = cosine_similarity(user_vector, packaging_data)
    
    # Add similarity scores to the dataframe
    df['Similarity'] = similarity_scores.flatten()
    
    # Sort by similarity to get the most similar packaging options
    recommendations = df.sort_values(by='Similarity', ascending=False).head(3)
    
    return recommendations[['Material', 'Similarity']].to_dict(orient='records')

# Flask route for receiving recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    # Get data from the POST request
    user_data = {
        'Material': request.json.get('Material'),
        'Carbon_Footprint': request.json.get('Carbon_Footprint'),
        'Recyclable': request.json.get('Recyclable'),
        'Water_Usage': request.json.get('Water_Usage'),
        'Cost': request.json.get('Cost')
    }
    
    # Load the dataset (can be replaced with real large datasets or API)
    df = load_data()

    # Call function to calculate recommendations
    recommendations = recommend_sustainable_packaging(user_data, df)
    
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)