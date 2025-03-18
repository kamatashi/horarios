import pandas as pd
from datetime import datetime, timedelta



def converter_tempo(tempo_str):
    return pd.to_datetime(tempo_str, format='%H:%M:%S').time()


df = pd.read_csv("horarios.csv")
df.columns = df.columns.str.strip()
print("Colunas encontradas:", df.columns.tolist())

df['saida_casa'] = df['saida_casa'].apply(converter_tempo)
df['chegada_uni'] = df['chegada_uni'].apply(converter_tempo)
df['saida_uni']   = df['saida_uni'].apply(converter_tempo)
df['chegada_casa'] = df['chegada_casa'].apply(converter_tempo)

def tempo_datetime(tempo):
    return datetime.combine(datetime.min, tempo)

def calcular_diferenca(inicio, fim):
    dt_inicio = tempo_datetime(inicio)
    dt_fim = tempo_datetime(fim)
    if dt_fim < dt_inicio:
        dt_fim += timedelta(days=1)
    return dt_fim - dt_inicio

def calcular_tempo(linha, inicio, fim):
    return calcular_diferenca(linha[inicio], linha[fim])

tempos_ida = df.apply(calcular_tempo, args=('saida_casa', 'chegada_uni'), axis=1)
tempos_volta = df.apply(calcular_tempo, args=('saida_uni', 'chegada_casa'), axis=1)
tempos_uni = df.apply(calcular_tempo, args=('chegada_uni', 'saida_uni'), axis=1)

tempos_deslocamento = tempos_ida + tempos_volta

df['Tempo de Ida'] = tempos_ida
df['Tempo de Volta'] = tempos_volta
df['Tempo na Universidade'] = tempos_uni
df['Tempo no Ônibus'] = tempos_deslocamento

print("Resumo dos tempos calculados:")
print(df[['Tempo no Ônibus', 'Tempo na Universidade']])
