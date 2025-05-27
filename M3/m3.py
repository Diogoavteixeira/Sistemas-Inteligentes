import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report
import seaborn as sns
import time
import psutil

# Carregar o dataset Diabetes (regressão) e Iris (classificação) já em formato DataFrame
diabetes = datasets.load_diabetes(as_frame=True)
iris = datasets.load_iris(as_frame=True)

# Análise estatística básica dos dados do Diabetes
print("Estatísticas Diabetes:")
print(diabetes['data'].describe().round(0).astype(int))  # Mostra valores arredondados para inteiros

# Análise estatística básica dos dados do Iris
print("\nEstatísticas Iris:")
print(iris['data'].describe())  # Mostra média, desvio padrão, min, max, etc. para cada coluna

# --- Modelo de Regressão para o dataset Diabetes ---
# Separar variáveis independentes (X_d) e variável dependente (y_d)
X_d, y_d = diabetes['data'], diabetes['target']

# Dividir o dataset em treino (80%) e teste (20%)
X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(X_d, y_d, test_size=0.2, random_state=42)

# Instanciar o modelo de Regressão Linear
reg = LinearRegression()

# Treinar o modelo com os dados de treino
process = psutil.Process()
start_mem = process.memory_info().rss / (1024 * 1024)  # Memória inicial em MB
start_time = time.time()
reg.fit(X_train_d, y_train_d)
train_time_d = time.time() - start_time
end_mem = process.memory_info().rss / (1024 * 1024)  # Memória final em MB
mem_used_d = end_mem - start_mem

# Fazer previsões com os dados de teste
y_pred_d = reg.predict(X_test_d)

# Avaliar o desempenho do modelo de regressão
print("\nPerformance Regressão Diabetes:")
print("MSE:", mean_squared_error(y_test_d, y_pred_d))  # Erro quadrático médio
print("R2:", r2_score(y_test_d, y_pred_d))             # Coeficiente de determinação (R²)
print("Primeiros 5 valores reais (Diabetes):", y_test_d.values[:5])
print("Primeiros 5 valores previstos (Diabetes):", y_pred_d[:5])
print(f"\nCusto Computacional Diabetes (Regressão Linear):")
print(f"- Tempo de treino: {train_time_d:.4f} segundos")
print(f"- Memória utilizada: {mem_used_d:.2f} MB")

# --- Modelo de Classificação para o dataset Iris ---
# Separar variáveis independentes (X_i) e variável dependente (y_i)
X_i, y_i = iris['data'], iris['target']

# Dividir o dataset em treino (80%) e teste (20%)
X_train_i, X_test_i, y_train_i, y_test_i = train_test_split(X_i, y_i, test_size=0.2, random_state=42)

# Instanciar o modelo de Random Forest para classificação
clf = RandomForestClassifier(random_state=42)

# Treinar o modelo com os dados de treino
process = psutil.Process()
start_mem = process.memory_info().rss / (1024 * 1024)
start_time = time.time()
clf.fit(X_train_i, y_train_i)
train_time_i = time.time() - start_time
end_mem = process.memory_info().rss / (1024 * 1024)
mem_used_i = end_mem - start_mem

# Fazer previsões com os dados de teste
y_pred_i = clf.predict(X_test_i)

# Avaliar o desempenho do modelo de classificação
print("\nPerformance Classificação Iris:")
print("Acurácia:", accuracy_score(y_test_i, y_pred_i))      # Percentagem de acertos
print(classification_report(y_test_i, y_pred_i))            # Relatório detalhado (precision, recall, f1-score)
print("Primeiras 10 classes reais (Iris):", y_test_i.values[:10])
print("Primeiras 10 classes previstas (Iris):", y_pred_i[:10])
print(f"\nCusto Computacional Iris (Random Forest):")
print(f"- Tempo de treino: {train_time_i:.4f} segundos")
print(f"- Memória utilizada: {mem_used_i:.2f} MB")

# Visualização dos dados do Diabetes (histograma das features)
print("\nA mostrar histograma das features do Diabetes...")
diabetes['data'].hist(figsize=(10, 8))
plt.suptitle('Distribuição das Features do Diabetes')
plt.tight_layout()
plt.show()

# Gráfico de dispersão: valores reais vs previstos (Diabetes)
print("A mostrar gráfico de dispersão: valores reais vs previstos (Diabetes)...")
plt.figure(figsize=(6, 6))
plt.scatter(y_test_d, y_pred_d, alpha=0.7)
plt.xlabel('Valores Reais')
plt.ylabel('Valores Previstos')
plt.title('Regressão Diabetes: Valores Reais vs Previstos')
plt.plot([y_test_d.min(), y_test_d.max()], [y_test_d.min(), y_test_d.max()], 'r--')
plt.tight_layout()
plt.show()

# Gráfico de barras: classes reais vs previstas (Iris)
print("A mostrar gráfico de barras: classes reais vs previstas (Iris)...")
plt.figure(figsize=(6, 4))
sns.countplot(x=y_test_i, label='Reais', color='blue', alpha=0.6)
sns.countplot(x=y_pred_i, label='Previstos', color='orange', alpha=0.6)
plt.title('Classificação Iris: Classes Reais vs Previstos')
plt.xlabel('Classe')
plt.ylabel('Contagem')
plt.legend(['Reais', 'Previstos'])
plt.tight_layout()
plt.show()

# Gráfico de dispersão: classes reais vs previstas (Iris)
print("A mostrar gráfico de dispersão: classes reais vs previstas (Iris)...")
plt.figure(figsize=(6, 6))
# Adiciona jitter para melhor visualização dos pontos sobrepostos
jitter = np.random.normal(0, 0.05, size=len(y_test_i))
plt.scatter(y_test_i + jitter, y_pred_i + jitter, alpha=0.7)
plt.xlabel('Classes Reais')
plt.ylabel('Classes Previstas')
plt.title('Classificação Iris: Classes Reais vs Previstos')
plt.xticks([0, 1, 2], iris['target_names'])
plt.yticks([0, 1, 2], iris['target_names'])
plt.plot([-.5, 2.5], [-.5, 2.5], 'r--')
plt.tight_layout()
plt.show()
