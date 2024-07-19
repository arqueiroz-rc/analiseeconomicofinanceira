import pandas as pd
import matplotlib.pyplot as plt
from math import pi

balanco_df = pd.read_csv('balanco.csv')
saude_df = pd.read_csv('saude_financeira.csv')

df = pd.merge(balanco_df, saude_df, on='empresa')

df['liquidez_corrente'] = df['ativo_total'] / df['passivo_total']
df['margem_bruta'] = df['lucro_bruto'] / df['receita_liquida']
df['despesa_sobre_receita'] = df['despesa_operacional'] / df['receita_liquida']
df['rentabilidade'] = df['lucro_bruto'] / df['ativo_total']
df['endividamento'] = df['passivo_total'] / df['ativo_total']
df['retorno_sobre_capital_proprio'] = df['lucro_bruto'] / (df['ativo_total'] - df['passivo_total'])

def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

df['liquidez_corrente'] = normalize(df['liquidez_corrente'])
df['margem_bruta'] = normalize(df['margem_bruta'])
df['despesa_sobre_receita'] = normalize(df['despesa_sobre_receita'])
df['rentabilidade'] = normalize(df['rentabilidade'])
df['endividamento'] = normalize(df['endividamento'])
df['retorno_sobre_capital_proprio'] = normalize(df['retorno_sobre_capital_proprio'])

def make_radar_chart(df, company_names):
    categories = ['liquidez_corrente', 'margem_bruta', 'despesa_sobre_receita', 'rentabilidade', 'endividamento', 'retorno_sobre_capital_proprio']
    N = len(categories)

    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    plt.figure(figsize=(10, 6))
    ax = plt.subplot(111, polar=True)

    for i, company in enumerate(company_names):
        values = df.loc[df['empresa'] == company, categories].values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=company)
        ax.fill(angles, values, alpha=0.25)

    plt.xticks(angles[:-1], categories)
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], ["0.2", "0.4", "0.6", "0.8", "1.0"], color="grey", size=7)
    plt.ylim(0, 1)

    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.title('Indicadores Financeiros das Empresas')
    plt.show()

company_names = df['empresa'].unique()
make_radar_chart(df, company_names)
