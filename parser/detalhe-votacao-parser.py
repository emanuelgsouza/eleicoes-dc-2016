# -*- coding: utf-8 -*-

# import libraries

from parser_utils import parserFile, generateRegionDataset

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
    dataLines = parserFile(file)
    print('Generate the DC city DataFrame')
    duqueCaxiasdf = generateRegionDataset(dataLines=dataLines, columns=LABELS, codMun=DC_CODE, turn=TURNO)

    print('Generate .csv file')
    duqueCaxiasdf.to_csv('detalhe_votacao_secao_DC_2016_RJ.csv', index=False)
