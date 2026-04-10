import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

def preprocess_data(df):
    print("\n--- Pré-processamento e Balanceamento de Dados ---")

    # Separar features (X) e target (y)
    X = df.drop("Class", axis=1)
    y = df["Class"]

    # Dividir os dados em conjuntos de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Escalonamento das features (StandardScaler)
    # Excluir 'Time' e 'Amount' do escalonamento inicial se necessário, ou escalar tudo
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)

    print("Dados escalonados.")

    # Balanceamento da classe minoritária com SMOTE no conjunto de treinamento
    print("Aplicando SMOTE para balanceamento de classes...")
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train_scaled, y_train)

    print(f"Shape de X_train antes do SMOTE: {X_train_scaled.shape}")
    print(f"Shape de X_train depois do SMOTE: {X_train_res.shape}")
    print(f"Distribuição de classes em y_train antes do SMOTE:\n{y_train.value_counts()}")
    print(f"Distribuição de classes em y_train depois do SMOTE:\n{y_train_res.value_counts()}")

    # Salvar os datasets pré-processados
    X_train_res.to_csv("X_train_res.csv", index=False)
    y_train_res.to_csv("y_train_res.csv", index=False)
    X_test_scaled.to_csv("X_test.csv", index=False)
    y_test.to_csv("y_test.csv", index=False)

    print("Dados pré-processados e balanceados salvos como X_train_res.csv, y_train_res.csv, X_test.csv e y_test.csv")

    return X_train_res, y_train_res, X_test_scaled, y_test

if __name__ == "__main__":
    df = pd.read_csv("credit_card_fraud_detection/data/creditcard.csv")
    X_train_res, y_train_res, X_test_scaled, y_test = preprocess_data(df)
