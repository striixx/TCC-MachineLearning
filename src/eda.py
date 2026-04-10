
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure the reports directory exists for saving plots
if not os.path.exists("../reports/figures"):
    os.makedirs("../reports/figures")

def perform_eda(df):
    """
    Performs exploratory data analysis on the credit card fraud dataset.

    Args:
        df (pandas.DataFrame): The input DataFrame containing credit card transactions.
    """
    print("\n--- Performing Exploratory Data Analysis (EDA) ---")

    # Display basic information
    print("\nInformações do dataset:")
    df.info()

    # Check for missing values
    print("\nMissing values per column:")
    print(df.isnull().sum())

    # Distribution of classes (Fraud vs. Non-Fraud)
    print("\nDistribuição das classes:")
    print(df["Class"].value_counts())
    print(df["Class"].value_counts(normalize=True) * 100)

    # Visualize class distribution
    plt.figure(figsize=(6, 4))
    sns.countplot(x="Class", data=df)
    plt.title("Distribuição das Classes (0: Não Fraude, 1: Fraude)")
    plt.xlabel("Classe")
    plt.ylabel("Número de Transações")
    plt.xticks(ticks=[0, 1], labels=["Não Fraude", "Fraude"])
    plt.savefig("../reports/figures/class_distribution.png")
    plt.close()
    print("Saved: ../reports/figures/class_distribution.png")

    # Visualize distribution of Time variable
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Time"], bins=50, kde=True)
    plt.title("Distribuição da Variável Time")
    plt.xlabel("Tempo (segundos)")
    plt.ylabel("Número de Transações")
    plt.savefig("../reports/figures/time_distribution.png")
    plt.close()
    print("Saved: ../reports/figures/time_distribution.png")

    # Visualize distribution of Amount variable
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Amount"], bins=50, kde=True)
    plt.title("Distribuição da Variável Amount")
    plt.xlabel("Valor da Transação")
    plt.ylabel("Número de Transações")
    plt.savefig("../reports/figures/amount_distribution.png")
    plt.close()
    print("Saved: ../reports/figures/amount_distribution.png")

    # Visualize distribution of some PCA features for both classes (V1 and V2 as examples)
    # V1
    plt.figure(figsize=(12, 8))
    sns.kdeplot(df[df["Class"] == 0]["V1"], label="Não Fraude", fill=True)
    sns.kdeplot(df[df["Class"] == 1]["V1"], label="Fraude", fill=True)
    plt.title("Distribuição da Feature V1 por Classe")
    plt.xlabel("V1")
    plt.ylabel("Densidade")
    plt.legend()
    plt.savefig("../reports/figures/pca_v1_distribution.png")
    plt.close()
    print("Saved: ../reports/figures/pca_v1_distribution.png")

    # V2
    plt.figure(figsize=(12, 8))
    sns.kdeplot(df[df["Class"] == 0]["V2"], label="Não Fraude", fill=True)
    sns.kdeplot(df[df["Class"] == 1]["V2"], label="Fraude", fill=True)
    plt.title("Distribuição da Feature V2 por Classe")
    plt.xlabel("V2")
    plt.ylabel("Densidade")
    plt.legend()
    plt.savefig("../reports/figures/pca_v2_distribution.png")
    plt.close()
    print("Saved: ../reports/figures/pca_v2_distribution.png")

    print("\nEDA concluída e gráficos salvos em ../reports/figures/.")

if __name__ == "__main__":
    # Example usage: Assumes data_loader.py is in the same directory and creditcard.csv in ../data/
    from data_loader import load_data
    data_path = "../data/creditcard.csv"
    credit_card_df = load_data(data_path)
    if credit_card_df is not None:
        perform_eda(credit_card_df)
