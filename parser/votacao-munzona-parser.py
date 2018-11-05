# -*- coding: utf-8 -*-

# import libraries
from parser_utils import parserFile, generateRegionDataset

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
    'codigo_cargo',
    'numero_candidato',
    'sq_candidato',
    'nome_candidato',
    'nome_urna_candidato',
    'cargo',
    'cod_sit_cand_superior',
    'desc_sit_cand_superior',
    'cod_sit_candidato',
    'desc_sit_candidato',
    'cod_sit_candidato_tot',
    'desc_sit_candidato_tot',
    'numero_partido',
    'sigla_partido',
    'nome_partido',
    'sequencial_legenda',
    'nome_coligacao',
    'composicao_legenda',
    'votos',
    'transito'
]

with open('votacao_candidato_munzona_2016_RJ.txt', mode = 'rb') as file:
    dataLines = parserFile(file)
    print(dataLines)
    print('Generate the DC city DataFrame')
    duqueCaxiasdf = generateRegionDataset(dataLines=dataLines, columns=LABELS, codMun=DC_CODE, turn=TURNO)

    print('Generate .csv file')
    duqueCaxiasdf.to_csv('votacao_munzona_DC_2016_RJ.csv', index=False)