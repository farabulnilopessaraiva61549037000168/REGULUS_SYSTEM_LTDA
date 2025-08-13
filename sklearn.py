import pandas as pd
from sklearn.ensemble import IsolationForest

# Dados de um órgão (ex: contratos, despesas, atividades)
df = pd.read_csv("dados_governo.csv")

# Preparar modelo de detecção de anomalias (modo sábio ativado)
modelo = IsolationForest(n_estimators=100, contamination=0.05)
df['anomaly'] = modelo.fit_predict(df[['valor', 'prazo', 'quantidade']])

# Exibir contratos considerados suspeitos pelo sábio
anomalias = df[df['anomaly'] == -1]
print("⚠️ ALERTA DO SÁBIO DOS SEIS CAMINHOS:")
print(anomalias[['nome_contrato', 'valor', 'responsável']]) 