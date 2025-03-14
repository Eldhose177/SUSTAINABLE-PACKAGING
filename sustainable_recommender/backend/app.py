from flask import Flask, request, jsonify
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os

app = Flask(__name__)

# Load dataset safely
DATA_PATH = "materials.csv"

if not os.path.exists(DATA_PATH):
    print(f"Error: {DATA_PATH} not found. Please ensure the file exists.")
    df = pd.DataFrame(columns=["Material Type", "Recyclable", "Compostable"])
else:
    df = pd.read_csv(DATA_PATH)

# Ensure necessary columns exist
required_columns = {"Material Type", "Recyclable", "Compostable"}
if not required_columns.issubset(df.columns):
    print("Error: Required columns missing in CSV.")
    df = pd.DataFrame(columns=list(required_columns))

# Generate TF-IDF matrix safely
if not df.empty:
    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf_vectorizer.fit_transform(df["Material Type"].astype(str))
else:
    tfidf_matrix = None

# Simple recommendation function
def recommend_packaging(material_type=None, recyclable=None, compostable=None):
    try:
        filtered_df = df.copy()

        if material_type:
            filtered_df = filtered_df[filtered_df["Material Type"].str.lower().eq(material_type.lower())]

        if recyclable is not None:
            filtered_df = filtered_df[filtered_df["Recyclable"].astype(str).eq(str(recyclable).lower())]

        if compostable is not None:
            filtered_df = filtered_df[filtered_df["Compostable"].astype(str).eq(str(compostable).lower())]

        return filtered_df.to_dict(orient="records")

    except Exception as e:
        print(f"Error in recommend_packaging: {e}")
        return []

# Advanced recommendation function based on similarity
def get_similar_materials(material_type):
    try:
        if tfidf_matrix is None or df.empty:
            return []

        material_index = df[df["Material Type"].str.lower() == material_type.lower()].index

        if material_index.empty:
            return []

        material_index = material_index[0]
        cosine_similarities = cosine_similarity(tfidf_matrix[material_index], tfidf_matrix).flatten()
        similar_indices = cosine_similarities.argsort()[::-1][1:4]  # Top 3 similar materials

        return df.iloc[similar_indices].to_dict(orient="records")

    except Exception as e:
        print(f"Error in get_similar_materials: {e}")
        return []

# API Endpoint to get recommendations
@app.route("/recommend", methods=["GET"])
def recommend():
    try:
        material_type = request.args.get("material_type")
        recyclable = request.args.get("recyclable", type=lambda x: x.lower() == "true")
        compostable = request.args.get("compostable", type=lambda x: x.lower() == "true")

        recommendations = recommend_packaging(material_type, recyclable, compostable)

        if not recommendations and material_type:
            recommendations = get_similar_materials(material_type)

        return jsonify(recommendations)

    except Exception as e:
        print(f"Error in /recommend endpoint: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)

