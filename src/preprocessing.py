import os
os.environ["LOKY_MAX_CPU_COUNT"] = str(os.cpu_count())

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

# Ensure the processed data directory exists
if not os.path.exists("../data/processed"):
    os.makedirs("../data/processed")

def preprocess_data(df):
    """
    Performs data preprocessing including feature scaling, train-test split,
    and SMOTE balancing on the training set.

    Args:
        df (pandas.DataFrame): The input DataFrame containing credit card transactions.

    Returns:
        tuple: X_train_res, y_train_res, X_test, y_test (processed dataframes).
    """
    print("\n--- Performing Data Preprocessing and SMOTE Balancing ---")

    X = df.drop("Class", axis=1)
    y = df["Class"]

    scaler = StandardScaler()
    X["Amount"] = scaler.fit_transform(X[["Amount"]])
    X["Time"] = scaler.fit_transform(X[["Time"]])

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.2, random_state=42, stratify=y)

    print("Formato dos dados de treino antes do SMOTE:", X_train.shape, y_train.shape)
    print("Distribuição das classes no treino antes do SMOTE:")
    print(y_train.value_counts())

    sm = SMOTE(random_state=42)
    X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

    print("\nFormato dos dados de treino após o SMOTE:", X_train_res.shape, y_train_res.shape)
    print("Distribuição das classes no treino após o SMOTE:")
    print(y_train_res.value_counts())

    X_train_res.to_csv("../data/processed/X_train_res.csv", index=False)
    y_train_res.to_csv("../data/processed/y_train_res.csv", index=False)
    X_test.to_csv("../data/processed/X_test.csv", index=False)
    y_test.to_csv("../data/processed/y_test.csv", index=False)

    print("\nPré-processamento e balanceamento concluídos e dados salvos em ../data/processed/.")

    return X_train_res, y_train_res, X_test, y_test

if __name__ == "__main__":
    from data_loader import load_data
    data_path = "../data/creditcard.csv"
    credit_card_df = load_data(data_path)
    if credit_card_df is not None:
        X_train_res, y_train_res, X_test, y_test = preprocess_data(credit_card_df)
        print("\nShape of X_train_res:", X_train_res.shape)
        print("Shape of y_train_res:", y_train_res.shape)
        print("Shape of X_test:", X_test.shape)
        print("Shape of y_test:", y_test.shape)