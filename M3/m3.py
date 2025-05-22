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

# Carregar o dataset Diabetes (regressão) e Iris (classificação) já em formato DataFrame
diabetes = datasets.load_diabetes(as_frame=True)
iris = datasets.load_iris(as_frame=True)

# Análise estatística básica dos dados do Diabetes
print("Estatísticas Diabetes:")
print(diabetes['data'].describe())  # Mostra média, desvio padrão, min, max, etc. para cada coluna

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
reg.fit(X_train_d, y_train_d)

# Fazer previsões com os dados de teste
y_pred_d = reg.predict(X_test_d)

# Avaliar o desempenho do modelo de regressão
print("\nPerformance Regressão Diabetes:")
print("MSE:", mean_squared_error(y_test_d, y_pred_d))  # Erro quadrático médio
print("R2:", r2_score(y_test_d, y_pred_d))             # Coeficiente de determinação (R²)

# --- Modelo de Classificação para o dataset Iris ---
# Separar variáveis independentes (X_i) e variável dependente (y_i)
X_i, y_i = iris['data'], iris['target']

# Dividir o dataset em treino (80%) e teste (20%)
X_train_i, X_test_i, y_train_i, y_test_i = train_test_split(X_i, y_i, test_size=0.2, random_state=42)

# Instanciar o modelo de Random Forest para classificação
clf = RandomForestClassifier(random_state=42)

# Treinar o modelo com os dados de treino
clf.fit(X_train_i, y_train_i)

# Fazer previsões com os dados de teste
y_pred_i = clf.predict(X_test_i)

# Avaliar o desempenho do modelo de classificação
print("\nPerformance Classificação Iris:")
print("Acurácia:", accuracy_score(y_test_i, y_pred_i))      # Percentagem de acertos
print(classification_report(y_test_i, y_pred_i))            # Relatório detalhado (precision, recall, f1-score)

# Visualização dos dados do Diabetes (histograma das features)
diabetes['data'].hist(figsize=(10, 8))
plt.suptitle('Distribuição das Features do Diabetes')
plt.tight_layout()
plt.show()

# Gráfico de dispersão: valores reais vs previstos (Diabetes)
plt.figure(figsize=(6, 6))
plt.scatter(y_test_d, y_pred_d, alpha=0.7)
plt.xlabel('Valores Reais')
plt.ylabel('Valores Previstos')
plt.title('Regressão Diabetes: Valores Reais vs Previstos')
plt.plot([y_test_d.min(), y_test_d.max()], [y_test_d.min(), y_test_d.max()], 'r--')
plt.tight_layout()
plt.show()

# Gráfico de barras: classes reais vs previstas (Iris)
plt.figure(figsize=(6, 4))
sns.countplot(x=y_test_i, label='Reais', color='blue', alpha=0.6)
sns.countplot(x=y_pred_i, label='Previstos', color='orange', alpha=0.6)
plt.title('Classificação Iris: Classes Reais vs Previstos')
plt.xlabel('Classe')
plt.ylabel('Contagem')
plt.legend(['Reais', 'Previstos'])
plt.tight_layout()
plt.show()
