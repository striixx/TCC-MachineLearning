
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
import os

def load_model(model_path):
    """
    Loads a trained machine learning model.

    Args:
        model_path (str): The path to the saved model file.

    Returns:
        object: The loaded machine learning model.
    """
    try:
        model = joblib.load(model_path)
        print(f"Model loaded successfully from {model_path}")
        return model
    except FileNotFoundError:
        print(f"Error: Model file not found at {model_path}")
        return None
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return None

def preprocess_new_data(df):
    """
    Preprocesses new data for prediction, including scaling Time and Amount.
    Note: This assumes the scaler was fitted on the training data during preprocessing.
    For a robust deployment, the scaler object should also be saved and loaded.
    For simplicity in this example, a new scaler is fitted, which is not ideal for production.

    Args:
        df (pandas.DataFrame): New data to preprocess.

    Returns:
        pandas.DataFrame: Preprocessed data.
    """
    # Create a new scaler for demonstration. In a real scenario, load the fitted scaler.
    scaler = StandardScaler()
    df_processed = df.copy()
    if 'Amount' in df_processed.columns:
        df_processed['Amount'] = scaler.fit_transform(df_processed[['Amount']])
    if 'Time' in df_processed.columns:
        df_processed['Time'] = scaler.fit_transform(df_processed[['Time']])
    return df_processed

def make_prediction(model, data):
    """
    Makes predictions using the loaded model.

    Args:
        model (object): The trained machine learning model.
        data (pandas.DataFrame): Preprocessed data for prediction.

    Returns:
        numpy.ndarray: Predicted classes (0 or 1).
    """
    if model is None:
        return None
    print("Making predictions...")
    predictions = model.predict(data)
    return predictions

if __name__ == "__main__":
    # Example usage:
    # 1. Load a dummy dataset for prediction (replace with actual new data)
    # For this example, we'll use a small part of the original dataset
    from data_loader import load_data
    original_df = load_data("../data/creditcard.csv")

    if original_df is not None:
        # Simulate new data by taking a few rows from the original dataset
        new_data_sample = original_df.sample(n=10, random_state=42).drop("Class", axis=1)
        print("\nSample of new data for prediction:")
        print(new_data_sample.head())

        # Preprocess the new data
        processed_new_data = preprocess_new_data(new_data_sample)

        # Load the trained Random Forest model (assuming it was saved by train.py)
        model_path = "../models/random_forest.pkl"
        rf_model = load_model(model_path)

        if rf_model:
            predictions = make_prediction(rf_model, processed_new_data)
            if predictions is not None:
                print("\nPredictions for the new data:")
                print(predictions)
                print("\nPrediction complete.")

    print("\nNote: For a production system, ensure the same scaler used during training is applied to new data.")
