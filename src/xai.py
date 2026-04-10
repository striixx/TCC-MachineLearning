import joblib
import pandas as pd
import shap
import matplotlib.pyplot as plt
import os
import numpy as np

# Garante que a pasta de figuras existe
if not os.path.exists("../reports/figures/shap_plots"):
    os.makedirs("../reports/figures/shap_plots")


def perform_xai_shap(model_path, X_test_path):
    print("\n--- Iniciando Explicabilidade com SHAP ---")

    try:
        # 1. Carregar o modelo e os dados
        model = joblib.load(model_path)
        X_test = pd.read_csv(X_test_path)

        # 2. Limpeza automática de colunas que não são do modelo
        # Removemos 'Class' ou índices numéricos se existirem
        if 'Class' in X_test.columns:
            X_test = X_test.drop('Class', axis=1)

        # Se houver colunas sem nome (índices), removemos
        X_test = X_test.loc[:, ~X_test.columns.str.contains('^Unnamed')]

        # 3. Alinhamento Dinâmico
        # Em vez de adivinhar os nomes, vamos pegar o que está no arquivo
        # O Random Forest espera exatamente 30 colunas.
        if len(X_test.columns) > 30:
            X_test = X_test.iloc[:, :30]

        print(f"Modelo e dados carregados. Colunas detectadas: {len(X_test.columns)}")
    except Exception as e:
        print(f"Erro ao carregar ou alinhar dados para SHAP: {e}")
        return

    # 4. Amostra para o SHAP (50 amostras)
    X_sample = X_test.sample(n=50, random_state=42)

    print("Calculando valores SHAP (isso pode levar um minuto)...")
    explainer = shap.TreeExplainer(model)

    # Calculamos os valores SHAP
    shap_values = explainer.shap_values(X_sample)

    # 5. AJUSTE DE FORMATO (O ponto crítico)
    # Se o SHAP retornar uma lista (comum em Random Forest), pegamos a classe 1 (Fraude)
    if isinstance(shap_values, list):
        values_to_plot = shap_values[1]
    elif isinstance(shap_values, np.ndarray) and len(shap_values.shape) == 3:
        values_to_plot = shap_values[:, :, 1]
    else:
        values_to_plot = shap_values

    print("Gerando gráfico de resumo SHAP...")
    plt.figure(figsize=(10, 6))

    # Criamos o gráfico de resumo
    # Forçamos o uso dos valores e dos nomes das colunas do X_sample
    shap.summary_plot(values_to_plot, X_sample, show=False)

    plt.title("Importância das Variáveis (SHAP) - Classe Fraude")
    plt.tight_layout()

    # Salvamos o gráfico
    save_path = "../reports/figures/shap_plots/shap_summary_plot_fraud.png"
    plt.savefig(save_path)
    plt.close()

    print(f"Sucesso! Gráfico SHAP salvo em: {save_path}")


if __name__ == "__main__":
    print("Script SHAP pronto.")
