from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

# Load dataset (Ensure CSV exists and is properly loaded)
DATA_PATH = "materials.csv"
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of app.py
DATA_PATH = os.path.join(BASE_DIR, "sustainable_recommender", "backend", "materials.csv")


try:
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()  # Remove extra spaces in column names
    df["Material Type"] = df["Material Type"].astype(str).fillna("")
    df["Recyclable"] = df["Recyclable"].astype(str).str.lower().map({"true": True, "false": False})
    df["Compostable"] = df["Compostable"].astype(str).str.lower().map({"true": True, "false": False})
except FileNotFoundError:
    df = pd.DataFrame(columns=["Material Type", "Recyclable", "Compostable"])
    
# Generate TF-IDF matrix for material descriptions (only if data is available)
if not df.empty and "Material Type" in df.columns:
    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf_vectorizer.fit_transform(df["Material Type"])
else:
    tfidf_matrix = None  # Handle empty dataset case

# Helper function to parse boolean values from request parameters
def parse_bool(value):
    if value is None:
        return None
    return value.lower() == "true"

# Function to recommend materials based on filtering
def recommend_packaging(material_type=None, recyclable=None, compostable=None):
    filtered_df = df.copy()

    # Filter by material type (case-insensitive substring match)
    if material_type:
        filtered_df = filtered_df[
            filtered_df["Material Type"].str.lower().str.contains(str(material_type).lower(), na=False)
        ]

    # Filter by recyclable status
    if recyclable is not None:
        filtered_df = filtered_df[filtered_df["Recyclable"] == recyclable]

    # Filter by compostable status
    if compostable is not None:
        filtered_df = filtered_df[filtered_df["Compostable"] == compostable]

    return filtered_df.to_dict(orient="records")

# Function to find similar materials based on TF-IDF similarity
def get_similar_materials(material_type):
    if tfidf_matrix is None or df.empty:
        return []  # Handle empty dataset case

    material_type = str(material_type).lower()
    material_index = df[df["Material Type"].str.lower() == material_type].index

    if material_index.empty:
        return []

    material_index = material_index[0]  # Extract integer index
    cosine_similarities = cosine_similarity(tfidf_matrix[material_index], tfidf_matrix).flatten()
    similar_indices = cosine_similarities.argsort()[::-1][1:4]  # Get top 3 similar materials

    return df.iloc[similar_indices].to_dict(orient="records")

# Home page route
@app.route("/")
def home():
    return render_template("index.html")

# API Endpoint for recommendations
@app.route("/recommend", methods=["GET"])
def recommend():
    material_type = request.args.get("material_type")
    recyclable = parse_bool(request.args.get("recyclable"))
    compostable = parse_bool(request.args.get("compostable"))

    recommendations = recommend_packaging(material_type, recyclable, compostable)

    # If no direct matches, find similar materials
    if not recommendations and material_type:
        recommendations = get_similar_materials(material_type)

    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
