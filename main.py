'''
A proposta do programa é calcular a média de tempo em que o usuário passa no ônibus e na universidade. 
Esse programa pode ser expandido para outras atividades.
Consideramos que o aluno anota chegadas e saidas em uma planilha.
'''
import pandas as pd
from datetime import datetime, timedelta



# Funções para manipulação da informações
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



# Manipulação das células
df = pd.read_csv("horarios.csv")
df.columns = df.columns.str.strip()

df['saida casa'] = df['saida casa'].apply(converterTempo)
df['chegada universidade'] = df['chegada universidade'].apply(converterTempo)
df['saida universidade']   = df['saida universidade'].apply(converterTempo)
df['chegada casa'] = df['chegada casa'].apply(converterTempo)


# Descobrindo o tempo nas atividades e cálculo da média
temposIda = df.apply(calcularTempo, args=('saida casa', 'chegada universidade'), axis=1)
temposVolta = df.apply(calcularTempo, args=('saida universidade', 'chegada casa'), axis=1)
temposUni = df.apply(calcularTempo, args=('chegada universidade', 'saida universidade'), axis=1)

temposDeslocamento = temposIda + temposVolta

df['Tempo de Ida'] = temposIda
df['Tempo de Volta'] = temposVolta
df['Tempo na Universidade'] = temposUni
df['Tempo no Ônibus'] = temposDeslocamento

mediaTempoUni = df['Tempo na Universidade'].mean()
mediaTempoOnibus = df['Tempo no Ônibus'].mean()
maxTempoUni = df['Tempo na Universidade'].max()
maxTempoOnibus = df['Tempo no Ônibus'].max()
minTempoUni = df['Tempo na Universidade'].min()
minTempoOnibus = df['Tempo no Ônibus'].min()


# Apresentação das informações descobertas
print('\n\nMédia de tempo em ônibus: ' + formatarTimedelta(mediaTempoOnibus))
print('Média de tempo na Universidade: ' + formatarTimedelta(mediaTempoUni))
print('Maxímo de tempo na universidade: ' + formatarTimedelta(maxTempoUni))
print('Máximo de tempo em ônibus: ' + formatarTimedelta(maxTempoOnibus))
print('Menor tempo na universidade: ' + formatarTimedelta(minTempoUni))
print('Menor tempo em ônibus: ' + formatarTimedelta(minTempoOnibus))
