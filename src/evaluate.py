import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score, precision_recall_curve, auc
import joblib
import os

# Garante que a pasta de figuras existe
if not os.path.exists("../reports/figures"):
    os.makedirs("../reports/figures")

def evaluate_models(trained_models, X_test, y_test):
    print("\n--- Avaliando Modelos de Machine Learning ---")
    results = {}

    for name, model in trained_models.items():
        print(f"\nAvaliando {name}...")
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        # Relatório de Classificação
        print(f"\nRelatorio de Classificacao para {name}:")
        print(classification_report(y_test, y_pred))

        # Matriz de Confusão
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Nao Fraude", "Fraude"], yticklabels=["Nao Fraude", "Fraude"])
        plt.title(f"Matriz de Confusao - {name}")
        plt.xlabel("Previsto")
        plt.ylabel("Real")
        plt.savefig(f"../reports/figures/confusion_matrix_{name.replace(' ', '_').lower()}.png")
        plt.close()

        # Curva ROC
        roc_auc = roc_auc_score(y_test, y_prob)
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'Curva ROC (area = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Taxa de Falsos Positivos')
        plt.ylabel('Taxa de Verdadeiros Positivos')
        plt.title(f'Curva ROC - {name}')
        plt.legend(loc="lower right")
        plt.savefig(f"../reports/figures/roc_curve_{name.replace(' ', '_').lower()}.png")
        plt.close()

        # Curva Precision-Recall
        precision, recall, _ = precision_recall_curve(y_test, y_prob)
        auprc = auc(recall, precision)
        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, color='blue', lw=2, label=f'Curva PR (area = {auprc:.2f})')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title(f'Curva Precision-Recall - {name}')
        plt.legend(loc="lower left")
        plt.savefig(f"../reports/figures/precision_recall_curve_{name.replace(' ', '_').lower()}.png")
        plt.close()

        results[name] = {"ROC AUC": roc_auc, "AUPRC": auprc}

    return results

if __name__ == "__main__":
    print("Script de avaliacao pronto.")
