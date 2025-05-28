import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report
import seaborn as sns
import time
import psutil

# Carregar os datasets Diabetes (regressão) e Iris (classificação)
diabetes = datasets.load_diabetes(as_frame=True)
iris = datasets.load_iris(as_frame=True)

# Análise estatística básica
print("Estatísticas Diabetes:")
print(diabetes['data'].describe().round(0).astype(int))

print("\nEstatísticas Iris:")
print(iris['data'].describe())

# -------------------------------
# MODELO DE REGRESSÃO – DIABETES
# -------------------------------
X_d, y_d = diabetes['data'], diabetes['target']
X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(X_d, y_d, test_size=0.2, random_state=42)

reg = LinearRegression()

process = psutil.Process()
start_mem = process.memory_info().rss / (1024 * 1024)
start_time = time.time()
reg.fit(X_train_d, y_train_d)
train_time_d = time.time() - start_time
end_mem = process.memory_info().rss / (1024 * 1024)
mem_used_d = end_mem - start_mem

y_pred_d = reg.predict(X_test_d)

print("\nPerformance Regressão Diabetes:")
print("MSE:", mean_squared_error(y_test_d, y_pred_d))
print("R2:", r2_score(y_test_d, y_pred_d))
print("Primeiros 5 valores reais (Diabetes):", y_test_d.values[:5])
print("Primeiros 5 valores previstos (Diabetes):", y_pred_d[:5])
print(f"\nCusto Computacional Diabetes (Regressão Linear):")
print(f"- Tempo de treino: {train_time_d:.4f} segundos")
print(f"- Memória utilizada: {mem_used_d:.2f} MB")

# -------------------------------
# MODELO DE CLASSIFICAÇÃO – IRIS
# -------------------------------
X_i, y_i = iris['data'], iris['target']
X_train_i, X_test_i, y_train_i, y_test_i = train_test_split(X_i, y_i, test_size=0.2, random_state=42)

clf = RandomForestClassifier(random_state=42)

process = psutil.Process()
start_mem = process.memory_info().rss / (1024 * 1024)
start_time = time.time()
clf.fit(X_train_i, y_train_i)
train_time_i = time.time() - start_time
end_mem = process.memory_info().rss / (1024 * 1024)
mem_used_i = end_mem - start_mem

y_pred_i = clf.predict(X_test_i)

print("\nPerformance Classificação Iris:")
print("Acurácia:", accuracy_score(y_test_i, y_pred_i))
print(classification_report(y_test_i, y_pred_i))
print("Primeiras 10 classes reais (Iris):", y_test_i.values[:10])
print("Primeiras 10 classes previstas (Iris):", y_pred_i[:10])
print(f"\nCusto Computacional Iris (Random Forest):")
print(f"- Tempo de treino: {train_time_i:.4f} segundos")
print(f"- Memória utilizada: {mem_used_i:.2f} MB")

# Validação cruzada (5-fold) para o dataset Iris
scores = cross_val_score(clf, X_i, y_i, cv=5)
print(f"\nValidação Cruzada (5-fold) – Iris:")
print("Acurácia média:", scores.mean())
print("Acurácia por fold:", scores)

# -------------------
# VISUALIZAÇÕES
# -------------------

# Histogramas do Diabetes
print("\nA mostrar histograma das features do Diabetes...")
diabetes['data'].hist(figsize=(10, 8))
plt.suptitle('Distribuição das Features do Diabetes')
plt.tight_layout()
plt.show()

# Dispersão: Reais vs Previstos (Diabetes)
print("A mostrar gráfico de dispersão: valores reais vs previstos (Diabetes)...")
plt.figure(figsize=(6, 6))
plt.scatter(y_test_d, y_pred_d, alpha=0.7)
plt.xlabel('Valores Reais')
plt.ylabel('Valores Previstos')
plt.title('Regressão Diabetes: Valores Reais vs Previstos')
plt.plot([y_test_d.min(), y_test_d.max()], [y_test_d.min(), y_test_d.max()], 'r--')
plt.tight_layout()
plt.show()

# Barras: Classes reais vs previstas (Iris)
print("A mostrar gráfico de barras: classes reais vs previstas (Iris)...")
plt.figure(figsize=(6, 4))
ax = sns.countplot(x=y_test_i, label='Reais', color='blue', alpha=0.6)
sns.countplot(x=y_pred_i, label='Previstos', color='orange', alpha=0.6)

for p in ax.patches[:len(np.unique(y_test_i))]:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', fontsize=10, color='blue')

for p in ax.patches[len(np.unique(y_test_i)):]:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', fontsize=10, color='orange')

plt.title('Classificação Iris: Classes Reais vs Previstos')
plt.xlabel('Classe')
plt.ylabel('Contagem')
plt.legend(['Reais', 'Previstos'])
plt.tight_layout()
plt.show()

# Dispersão: Classes reais vs previstas (Iris)
print("A mostrar gráfico de dispersão: classes reais vs previstas (Iris)...")
plt.figure(figsize=(6, 6))
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
