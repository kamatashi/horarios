import pandas as pd
from datetime import datetime, timedelta



def converterTempo(tempo_str):
    return pd.to_datetime(tempo_str, format='%H:%M:%S').time()


def tempoDatetime(tempo):
    return datetime.combine(datetime.min, tempo)


def calcularDiferenca(inicio, fim):
    dtInicio = tempoDatetime(inicio)
    dtFim = tempoDatetime(fim)
    if dtFim < dtInicio:
        dtFim += timedelta(days=1)
    return dtFim - dtInicio


def formatarTimedelta(dado):
    totalSegundos = int(dado.total_seconds())
    horas = totalSegundos // 3600
    minutos = (totalSegundos % 3600) // 60
    segundos = totalSegundos % 60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


def calcularTempo(linha, inicio, fim):
    return calcularDiferenca(linha[inicio], linha[fim])




df = pd.read_csv("horarios.csv")
df.columns = df.columns.str.strip()
#print("Colunas encontradas:", df.columns.tolist())

df['saida_casa'] = df['saida_casa'].apply(converterTempo)
df['chegada_uni'] = df['chegada_uni'].apply(converterTempo)
df['saida_uni']   = df['saida_uni'].apply(converterTempo)
df['chegada_casa'] = df['chegada_casa'].apply(converterTempo)


temposIda = df.apply(calcularTempo, args=('saida_casa', 'chegada_uni'), axis=1)
temposVolta = df.apply(calcularTempo, args=('saida_uni', 'chegada_casa'), axis=1)
temposUni = df.apply(calcularTempo, args=('chegada_uni', 'saida_uni'), axis=1)

temposDeslocamento = temposIda + temposVolta

df['Tempo de Ida'] = temposIda
df['Tempo de Volta'] = temposVolta
df['Tempo na Universidade'] = temposUni
df['Tempo no Ônibus'] = temposDeslocamento

mediaTempoUni = df['Tempo na Universidade'].mean()
mediaTempoOnibus = df['Tempo no Ônibus'].mean()

# print("Resumo dos tempos calculados:")
# print(df[['Tempo no Ônibus', 'Tempo na Universidade']])
print('\n\nMédia de tempo em ônibus: ' + formatarTimedelta(mediaTempoOnibus))
print('Média de tempo na Universidade: ' + formatarTimedelta(mediaTempoUni))
