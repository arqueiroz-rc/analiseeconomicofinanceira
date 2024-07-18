import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

# Carregar os dados
balanco_df = pd.read_csv('balanco.csv')
saude_df = pd.read_csv('saude_financeira.csv')

# Juntar os dados
df = pd.merge(balanco_df, saude_df, on='empresa')

# Criar novas colunas de indicadores financeiros
df['liquidez_corrente'] = df['ativo_total'] / df['passivo_total']
df['margem_bruta'] = df['lucro_bruto'] / df['receita_liquida']
df['despesa_sobre_receita'] = df['despesa_operacional'] / df['receita_liquida']

# Preparar os dados para o modelo
X = df[['ativo_total', 'passivo_total', 'receita_liquida', 'lucro_bruto', 'despesa_operacional', 'liquidez_corrente', 'margem_bruta', 'despesa_sobre_receita']]
y = df['saude_financeira']

# Codificar as etiquetas
le = LabelEncoder()
y = le.fit_transform(y)

# Dividir os dados em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Fazer previsões
y_pred = model.predict(X_test)

# Avaliar o modelo
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

# Visualização
plt.figure(figsize=(10, 6))
plt.barh(df['empresa'], df['liquidez_corrente'], color='blue', alpha=0.6, label='Liquidez Corrente')
plt.barh(df['empresa'], df['margem_bruta'], color='green', alpha=0.6, label='Margem Bruta')
plt.xlabel('Indicadores Financeiros')
plt.ylabel('Empresas')
plt.title('Indicadores Financeiros das Empresas')
plt.legend()
plt.show()
