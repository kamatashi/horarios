import pandas as pd

# Função para converter string de tempo para objeto datetime.time
def converter_tempo(tempo_str):
    return pd.to_datetime(tempo_str, format='%H:%M:%S').time()

# Ler a planilha (aqui, utilizando um CSV)
df = pd.read_csv("horarios.csv")

# Converter os horários para o formato de tempo
df['saida_casa'] = df['saida_casa'].apply(converter_tempo)
df['chegada_uni'] = df['chegada_uni'].apply(converter_tempo)
df['saida_uni']   = df['saida_uni'].apply(converter_tempo)
df['chegada_casa'] = df['chegada_casa'].apply(converter_tempo)

# Para calcular as diferenças, é mais simples trabalhar com objetos datetime.
# Vamos considerar uma data fixa (por exemplo, 1900-01-01) para todos os horários.
from datetime import datetime, timedelta

def tempo_datetime(tempo):
    return datetime.combine(datetime.min, tempo)

def calcular_diferenca(inicio, fim):
    # Se o fim for menor que o início, assumimos que o horário passou da meia-noite
    dt_inicio = tempo_datetime(inicio)
    dt_fim = tempo_datetime(fim)
    if dt_fim < dt_inicio:
        dt_fim += timedelta(days=1)
    return dt_fim - dt_inicio

# Calcular os tempos para cada linha
tempos_ida = df.apply(lambda linha: calcular_diferenca(linha['saida_casa'], linha['chegada_uni']), axis=1)
tempos_volta = df.apply(lambda linha: calcular_diferenca(linha['saida_uni'], linha['chegada_casa']), axis=1)
tempos_uni = df.apply(lambda linha: calcular_diferenca(linha['chegada_uni'], linha['saida_uni']), axis=1)

# Tempo total de deslocamento (ida + volta)
tempos_deslocamento = tempos_ida + tempos_volta

# Exibir os resultados
df['tempo_ida'] = tempos_ida
df['tempo_volta'] = tempos_volta
df['tempo_uni'] = tempos_uni
df['tempo_deslocamento'] = tempos_deslocamento

print("Resumo dos tempos calculados:")
print(df[['tempo_deslocamento', 'tempo_uni']])
