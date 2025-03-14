from flask import Flask, request, jsonify
import pandas as pd
from recommender import get_recommendations

app = Flask(__name__)

# Load the dataset (ensure 'materials.csv' exists)
df = pd.read_csv("materials.csv")

@app.route('/')
def home():
    return jsonify({"message": "Sustainable Recommender API is running!"})

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    material = data.get("material")

    if not material:
        return jsonify({"error": "Material is required"}), 400

    recommendations = get_recommendations(material, df)
    return jsonify({"recommendations": recommendations})

if __name__ == '__main__':
    app.run(debug=True)
