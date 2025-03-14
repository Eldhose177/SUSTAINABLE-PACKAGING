import pandas as pd

def get_recommendations(material, df):
    """
    Given a material, return the top sustainable alternatives.
    """
    material = material.lower()

    # Example logic: Filter materials with similar properties
    alternatives = df[df['category'] == df[df['material'].str.lower() == material]['category'].values[0]]

    return alternatives['material'].tolist() if not alternatives.empty else ["No alternatives found"]
