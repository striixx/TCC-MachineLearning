import os
import sys

# --- SUPRIME WARNING DO JOBLIB (LOKY) NO WINDOWS ---
os.environ["LOKY_MAX_CPU_COUNT"] = str(os.cpu_count())

import pandas as pd
import matplotlib

matplotlib.use('Agg')

# --- CONFIGURAÇÃO DE CAMINHOS (IMPORTANTE) ---
current_file_path = os.path.abspath(__file__)
src_dir = os.path.dirname(current_file_path)
project_root = os.path.dirname(src_dir)

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# --- IMPORTAÇÃO DOS SEUS SCRIPTS ---
try:
    import data_loader
    import eda
    import preprocessing
    import train
    import evaluate
    import xai

    print("Scripts carregados com sucesso!")
except ImportError as e:
    print(f"\nERRO DE IMPORTAÇÃO: {e}")
    print(f"Verifique se os arquivos .py estão na pasta: {src_dir}")
    sys.exit(1)


def run_pipeline():
    print("\n" + "=" * 50)
    print("INICIANDO PIPELINE DE DETECÇÃO DE FRAUDES - TCC VITOR")
    print("=" * 50)

    data_path = os.path.join(project_root, "data", "creditcard.csv")

    if not os.path.exists(data_path):
        print(f"\nERRO: Arquivo não encontrado em: {data_path}")
        print("Por favor, coloque o arquivo 'creditcard.csv' dentro da pasta 'data'.")
        return

    print("\n[1/5] Carregando dados...")
    df = data_loader.load_data(data_path)

    print("\n[2/5] Realizando Análise Exploratória (EDA)...")
    eda.perform_eda(df)

    print("\n[3/5] Preparando dados e aplicando SMOTE...")
    X_train_res, y_train_res, X_test, y_test = preprocessing.preprocess_data(df)

    print("\n[4/5] Treinando modelos (Regressão Logística, Random Forest, Rede Neural)...")
    trained_models = train.train_models(X_train_res, y_train_res)

    print("\n[5/5] Avaliando modelos e gerando gráficos...")
    evaluate.evaluate_models(trained_models, X_test, y_test)

    print("\n[EXTRA] Gerando explicabilidade com SHAP (Random Forest)...")
    rf_model_path = os.path.join(project_root, "models", "random_forest.pkl")
    X_test_path = os.path.join(project_root, "data", "processed", "X_test.csv")

    if os.path.exists(rf_model_path) and os.path.exists(X_test_path):
        xai.perform_xai_shap(rf_model_path, X_test_path)
    else:
        print("Aviso: Não foi possível rodar o SHAP. Verifique se o modelo foi salvo.")

    print("\n" + "=" * 50)
    print("PIPELINE CONCLUÍDO COM SUCESSO!")
    print("Verifique as pastas 'models' e 'reports' para ver os resultados.")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()