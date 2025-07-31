

import os
import pickle
import numpy as np
import random # For adding a bit of randomness to confidence

# Dummy feature list - Ensure these are added in your Django Admin Symptom model
DUMMY_FEATURE_LIST = [
    'Fever', 'Cough', 'Headache', 'Fatigue', 'Chest Pain',
    'Nausea', 'Vomiting', 'Shortness of Breath', 'Diarrhea', 'Muscle Pain',
    'Sore Throat', 'Runny Nose', 'Abdominal Pain', 'Joint Pain', 'Skin Rash',
    'Dizziness', 'Blurry Vision'
]
# Dummy diseases for simulation (these don't directly map to DUMMY_FEATURE_LIST yet)
DUMMY_DISEASES = [
    'Common Cold', 'Flu', 'Bronchitis', 'Heart Condition', 'Gastroenteritis',
    'Allergies', 'Migraine', 'Chickenpox', 'Dehydration', 'Viral Fever'
]


_model = None

def load_model():
    """
    Loads the trained machine learning model.
    For now, we'll just indicate a dummy model is "loaded".
    """
    global _model
    if _model is None:
        print("ML Model (or dummy placeholder) initialized.")
        _model = "DUMMY_MODEL" # For now, we'll always use a dummy model.
    return _model

def preprocess_symptoms(selected_symptoms, feature_list):
    """
    Preprocesses selected symptoms into a numerical array suitable for the model.
    Assumes selected_symptoms is a list of symptom names (strings).
    """
    input_vector = np.zeros(len(feature_list))
    for i, feature in enumerate(feature_list):
        if feature in selected_symptoms:
            input_vector[i] = 1
    return input_vector.reshape(1, -1) # Reshape for single prediction

def predict_disease(selected_symptoms):
    """
    Makes a prediction based on the selected symptoms using enhanced dummy logic.
    This function simulates a more "intelligent" response.
    """
    load_model() # Ensure model is loaded

    # Convert selected_symptoms to a set for faster lookup
    symptoms_set = set(selected_symptoms)

    # --- Rule-based Dummy Predictions (Enhanced) ---

    # Common Cold / Flu
    if "Fever" in symptoms_set and "Cough" in symptoms_set:
        if "Shortness of Breath" in symptoms_set or "Chest Pain" in symptoms_set:
            return {
                "predicted_disease": "Flu with complications",
                "confidence": 0.90,
                "suggestions": ["Seek immediate medical attention.", "Rest, hydrate, avoid public places."]
            }
        elif "Headache" in symptoms_set and "Fatigue" in symptoms_set and "Muscle Pain" in symptoms_set:
            return {
                "predicted_disease": "Flu",
                "confidence": 0.85,
                "suggestions": ["Rest, stay hydrated, consider over-the-counter flu remedies. Consult a doctor if symptoms worsen."]
            }
        elif "Sore Throat" in symptoms_set or "Runny Nose" in symptoms_set:
            return {
                "predicted_disease": "Common Cold",
                "confidence": 0.75,
                "suggestions": ["Rest, drink fluids, use saline nasal spray. Symptoms usually resolve in a week."]
            }

    # Gastroenteritis (Stomach Flu)
    if "Nausea" in symptoms_set and "Vomiting" in symptoms_set:
        if "Diarrhea" in symptoms_set and "Abdominal Pain" in symptoms_set:
            return {
                "predicted_disease": "Gastroenteritis (Stomach Flu)",
                "confidence": 0.92,
                "suggestions": ["Stay hydrated with oral rehydration solutions. Eat bland foods. Consult a doctor if dehydration is severe or symptoms persist."]
            }

    # Heart Condition (High Alert)
    if "Chest Pain" in symptoms_set:
        if "Shortness of Breath" in symptoms_set or "Dizziness" in symptoms_set or "Fatigue" in symptoms_set:
            return {
                "predicted_disease": "Potential Heart Condition",
                "confidence": 0.98,
                "suggestions": ["**This is a critical symptom combination. Seek emergency medical attention IMMEDIATELY.**"]
            }

    # Allergies
    if "Runny Nose" in symptoms_set and "Cough" in symptoms_set and "Sore Throat" not in symptoms_set and "Fever" not in symptoms_set:
        return {
            "predicted_disease": "Seasonal Allergies",
            "confidence": 0.70,
            "suggestions": ["Consider over-the-counter antihistamines. Avoid allergens if known. Consult an allergist for persistent symptoms."]
        }

    # Migraine
    if "Headache" in symptoms_set:
        if "Nausea" in symptoms_set or "Blurry Vision" in symptoms_set:
            return {
                "predicted_disease": "Migraine",
                "confidence": 0.80,
                "suggestions": ["Rest in a dark, quiet room. Over-the-counter pain relievers may help. Consult a doctor for diagnosis and management."]
            }

    # Skin Conditions
    if "Skin Rash" in symptoms_set:
        if "Fever" in symptoms_set and "Fatigue" in symptoms_set:
            return {
                "predicted_disease": "Possible Viral Infection (e.g., Chickenpox, Measles)",
                "confidence": 0.88,
                "suggestions": ["Consult a doctor for diagnosis. Avoid scratching. Isolate if contagious."]
            }
        else:
             return {
                "predicted_disease": "Skin Irritation/Allergy",
                "confidence": 0.60,
                "suggestions": ["Identify potential irritants. Keep the area clean. Consult a dermatologist if persistent."]
            }

    # General Viral/Bacterial Infection (catch-all for milder symptoms)
    if len(symptoms_set) >= 1: # If at least one symptom is selected
        if ("Fever" in symptoms_set or "Fatigue" in symptoms_set or "Muscle Pain" in symptoms_set):
            return {
                "predicted_disease": "General Viral Infection",
                "confidence": 0.65,
                "suggestions": ["Rest, hydrate, monitor symptoms. Consult a doctor if symptoms worsen or new symptoms appear."]
            }

    # Fallback for less specific or uncommon combinations
    if len(symptoms_set) > 0:
        return {
            "predicted_disease": "Needs more information or professional diagnosis",
            "confidence": round(0.4 + random.random() * 0.2, 2), # Random confidence between 40-60%
            "suggestions": ["The combination of symptoms is not specific enough for a clear prediction. Please provide more details or consult a doctor for accurate diagnosis."]
        }
    else: # No symptoms selected (should be caught by frontend, but for backend robustness)
        return {
            "predicted_disease": "No symptoms provided",
            "confidence": 0.0,
            "suggestions": ["Please select symptoms to get a prediction."]
        }

# Initialize model when this module is imported
load_model()