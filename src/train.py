import os
os.environ["LOKY_MAX_CPU_COUNT"] = str(os.cpu_count())
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import joblib

# Ensure the models directory exists for saving models
if not os.path.exists("../models"):
    os.makedirs("../models")

def train_models(X_train, y_train):
    """
    Trains Logistic Regression, Random Forest, and Neural Network models.

    Args:
        X_train (pandas.DataFrame): Training features.
        y_train (pandas.Series): Training target.

    Returns:
        dict: A dictionary containing the trained models.
    """
    print("\n--- Training Machine Learning Models ---")

    models = {
        'Logistic Regression': LogisticRegression(solver='liblinear', random_state=42, class_weight='balanced'),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'),
        'Neural Network': MLPClassifier(hidden_layer_sizes=(100, 50), activation='relu', solver='adam', max_iter=200, random_state=42)
    }

    trained_models = {}
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        trained_models[name] = model
        model_path = f"../models/{name.replace(' ', '_').lower()}.pkl"
        joblib.dump(model, model_path)
        print(f"Model {name} trained and saved to {model_path}")

    print("\nAll models trained and saved.")
    return trained_models

if __name__ == "__main__":
    # Example usage: Assumes processed data is in ../data/processed/
    X_train_res = pd.read_csv("../data/processed/X_train_res.csv")
    y_train_res = pd.read_csv("../data/processed/y_train_res.csv").squeeze()

    if X_train_res is not None and y_train_res is not None:
        trained_models = train_models(X_train_res, y_train_res)
        print("Trained models:", trained_models.keys())
