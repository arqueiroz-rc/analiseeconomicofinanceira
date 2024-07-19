import pandas as pd
import matplotlib.pyplot as plt
from math import pi

balanco_df = pd.read_csv('balanco.csv')

balanco_df['liquidez_corrente'] = balanco_df['ativo_total'] / balanco_df['passivo_total']
balanco_df['margem_bruta'] = balanco_df['lucro_bruto'] / balanco_df['receita_liquida']
balanco_df['despesa_sobre_receita'] = balanco_df['despesa_operacional'] / balanco_df['receita_liquida']
balanco_df['rentabilidade'] = balanco_df['lucro_bruto'] / balanco_df['ativo_total']
balanco_df['endividamento'] = balanco_df['passivo_total'] / balanco_df['ativo_total']
balanco_df['retorno_sobre_capital_proprio'] = balanco_df['lucro_bruto'] / (balanco_df['ativo_total'] - balanco_df['passivo_total'])

def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

balanco_df['liquidez_corrente'] = normalize(balanco_df['liquidez_corrente'])
balanco_df['margem_bruta'] = normalize(balanco_df['margem_bruta'])
balanco_df['despesa_sobre_receita'] = normalize(balanco_df['despesa_sobre_receita'])
balanco_df['rentabilidade'] = normalize(balanco_df['rentabilidade'])
balanco_df['endividamento'] = normalize(balanco_df['endividamento'])
balanco_df['retorno_sobre_capital_proprio'] = normalize(balanco_df['retorno_sobre_capital_proprio'])

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

company_names = balanco_df['empresa'].unique()

make_radar_chart(balanco_df, company_names)
