# 💳 Detecção de Fraudes em Cartões de Crédito com Machine Learning

Este projeto faz parte do meu **Trabalho de Conclusão de Curso (TCC II )**. O objetivo é desenvolver e avaliar modelos de Machine Learning para identificar transações fraudulentas, utilizando técnicas avançadas de balanceamento de dados e explicabilidade de modelos (XAI).

## 🚀 Visão Geral
O projeto utiliza o dataset de cartões de crédito do Kaggle e implementa um pipeline completo de Ciência de Dados:
1. **Análise Exploratória (EDA):** Visualização de distribuições e correlações.
2. **Pré-processamento:** Escalonamento de variáveis e tratamento de desbalanceamento com **SMOTE**.
3. **Modelagem:** Comparação entre **Regressão Logística**, **Random Forest** e **Redes Neurais (MLP)**.
4. **Avaliação:** Uso de métricas robustas como Precision-Recall, F1-Score e ROC AUC.
5. **Explicabilidade (XAI):** Uso de **SHAP** para entender as decisões do modelo Random Forest.

## 📊 Resultados Obtidos
O modelo **Random Forest** apresentou o melhor desempenho para a detecção de fraudes:
- **Precision (Fraude):** ~0.85
- **Recall (Fraude):** ~0.84
- **F1-Score:** ~0.84
- **ROC AUC:** ~0.98

## 📁 Estrutura do Projeto
- `src/`: Scripts de código (carregamento, treino, avaliação, XAI).
- `data/`: Pasta para o dataset (não incluído no GitHub por tamanho).
- `models/`: Modelos treinados salvos em formato `.pkl`.
- `reports/figures/`: Gráficos gerados automaticamente pelo pipeline.
- `requirements.txt`: Lista de bibliotecas necessárias.

## 🛠️ Como Rodar
1. Clone o repositório: `git clone https://github.com/SEU_USUARIO/deteccao-fraude-cartao-credito.git`
2. Instale as dependências: `pip install -r requirements.txt`
3. Coloque o `creditcard.csv` na pasta `data/`.
4. Execute o pipeline: `python src/main.py`

## 👨‍🎓 Autor
**Vitor** - Aluno de Engenharia/Ciência da Computação.
Orientador: Prof. Flavio.
