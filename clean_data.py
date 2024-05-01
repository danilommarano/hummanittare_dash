from pandas import read_csv, to_datetime
from pathlib import Path

output_path = 'input'
input_path = Path(output_path, 'raw')
df_file = 'BASE BRADESCO E CNU.csv'
subtitle_file = 'LEGENDA PREVENTIVOS.csv'

columns_df = {
    'Operadora': 'operadora',
    'REDE/REEMBOLSO': 'rede_reembolso',
    'Titular': 'titular',
    'Usuário': 'usuario',
    'Idade': 'idade',
    'Tipo de Associado': 'tipo_associado',
    'Sexo': 'sexo',
    'PLANO': 'plano',
    'Grupo Tipo de Atendimento': 'tipo_atendimento',
    ' Valor': 'valor',
    'Competência': 'competencia',
    'Competência (mês)': 'competencia_mes',
    'Nome do Prestador Local': 'nome_prestador',
    'AMB - Código do Procedimento': 'codigo_procedimento',
    'Nome do Procedimento': 'nome_procedimento',
    'Qtd Procedimentos': 'qtd_procedimento'
}
columns_sub = {
    'AMB - Código do Procedimento': 'codigo_procedimento',
    'PADRAO_HUMANITTARE': 'padrao_humanittare'
}

df = read_csv(Path(input_path, df_file))
df = df.rename(columns=columns_df)

df.operadora = df.operadora.str.title()
df.rede_reembolso = df.rede_reembolso.str.capitalize()
df.titular = df.titular.str.replace('TITULAR ', '').astype(int)
df.usuario = df.usuario.str.replace('USUARIO ', '').astype(int)
sexo_replace = {'M': 'Masculino', 'F': 'Feminino'}
df.sexo = df.sexo.replace(sexo_replace)
df.tipo_associado = df.tipo_associado.str.capitalize()
df.plano = df.plano.str.strip()
df.tipo_atendimento = df.tipo_atendimento.str.capitalize()
df.valor = df.valor.str.replace('R$', '').str.replace(',', '').str.strip()
df.valor = df.valor.replace({'-': None}).astype(float)
df.competencia = to_datetime(df.competencia, format="%d/%m/%Y")
df.competencia_mes = to_datetime(df.competencia_mes, format="%m/%Y")
df.nome_prestador = df.nome_prestador.str.title()
df.nome_procedimento = df.nome_procedimento.str.capitalize()
dsc_re = r"\(([^)]+)\)"
descricao = df.nome_procedimento.str.extract(dsc_re, expand=False)
df['descricao_procedimento'] = descricao.str.capitalize()
df.nome_procedimento = df.nome_procedimento.str.replace(dsc_re, "", regex=True)

sub = read_csv(Path(input_path, subtitle_file))
sub = sub.rename(columns=columns_sub)
sub.padrao_humanittare = sub.padrao_humanittare.str.capitalize()

df_sub = df.join(other=sub, on='codigo_procedimento', rsuffix='_remove')
df_sub = df_sub.drop(columns='codigo_procedimento_remove')

df_sub.to_csv(Path(output_path, 'Dados Tratados Humanittare.csv'))


