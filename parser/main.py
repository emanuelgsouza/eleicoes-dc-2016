# -*- coding: utf-8 -*-

# import libraries
import pandas as pd

# helper functions
removeSpaces = lambda string : string.strip()

removeQuotes = lambda line : str(line).replace('"', '')

# define constants
DC_CODE = '58335'

TURNO = '2'

LABELS = [
    'data',
    'hora',
    'ano',
    'turno',
    'descricao',
    'uf',
    'ue',
    'codigo_municipio',
    'nome_municipio',
    'zona',
    'secao',
    'codigo_cargo',
    'cargo',
    'aptos',
    'comparecimento',
    'abstencoes',
    'votos_nominais',
    'votos_brancos',
    'votos_nulos',
    'votos_legenda',
    'votos_anulados'
]

with open('detalhe_votacao_secao_2016_RJ.txt', mode = 'r') as file:
    print('Init parse file')
    dataLines = []

    print('Work in each line')
    for line in file:
        _line = removeQuotes(line)
        dataColumns = list(map(removeSpaces, _line.split(';')))
        dataColumns[0] = dataColumns[0].replace("b'", '')
        dataColumns[-1] = dataColumns[-1].replace("\\n'", '')
        dataLines.append(dataColumns)

    print('Generate the DataFrame')
    df = pd.DataFrame.from_records(dataLines, columns=LABELS)

    print('Generate the DC city DataFrame')
    duqueCaxiasdf = df[(df['codigo_municipio'] == DC_CODE) & (df['turno'] == TURNO)]

    print('Generate .csv file')
    duqueCaxiasdf.to_csv('detalhe_votacao_secao_DC_2016_RJ.csv', index=False)
