import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


def analise_por_mes_e_tipo_evento(tipo_evento):
    """
    Analisa a frequência de consultas por usuário, separada por mês e tipo de evento.

    Parâmetros:
        tipo_evento (str): Tipo de evento a ser filtrado.

    Retorna:
        DataFrame: DataFrame contendo a análise por usuário, mês e tipo de evento.
    """
    df_filtrado = df[df['TIPO EVENTO'] == tipo_evento]
    agrupado = df_filtrado.groupby(['USUARIO', 'MÊS', 'ANO'])['ID'].count().reset_index()
    agrupado['PCT_CONSULTAS'] = agrupado['ID'] / agrupado['ID'].sum() * 100
    agrupado = agrupado.sort_values(by='PCT_CONSULTAS', ascending=False)

    return agrupado



df = pd.read_csv('input\Dados Tratados Humanittare.csv')
df['DATA'] = pd.to_datetime(df['DATA'])
df['ANO'] = df['DATA'].dt.year
df['MÊS'] = df['DATA'].dt.month_name()

st.title('Análise de Frequência de Consultas por Usuário')
tipo_evento = st.selectbox('Tipo de Evento:', df['TIPO EVENTO'].unique())
dados_analise = analise_por_mes_e_tipo_evento(tipo_evento)

st.header('Distribuição Mensal de Consultas por Usuário (%)')
consultas_por_mes = dados_analise.groupby(['MÊS', 'ANO'])['PCT_CONSULTAS'].sum().reset_index()

plt.figure(figsize=(12, 6))
consultas_por_mes.plot.bar(x='MÊS', y='PCT_CONSULTAS', color='skyblue')
plt.xlabel('Mês')
plt.ylabel('Percentual de Consultas')
plt.title(f'Distribuição Mensal de Consultas por Usuário ({tipo_evento})')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

# Ranking dos Maiores Usuários
st.header('Ranking dos Maiores Usuários (%)')

# Filtre os 10 maiores usuários
maiores_usuarios = dados_analise.head(10)

# Crie a tabela de ranking
colunas = ['USUARIO', 'MÊS', 'PCT_CONSULTAS']
st.table(maiores_usuarios[colunas])
