# -*- coding: utf-8 -*-

# imports
import pandas as pd

df = pd.read_csv('detalhe_votacao_secao_DC_2016_RJ.csv')

# constants
APTOS = 'aptos'
ABSTENCOES = 'abstencoes'
BRANCOS = 'votos_brancos'
NULOS = 'votos_nulos'
ANULADOS = 'votos_anulados'
NOMINAIS = 'votos_nominais'

# helpers
getSum = lambda df, prop : df[prop].sum()

def factoryData (df):
    return {
        'abstencoes': getSum(df, ABSTENCOES),
        'aptos': getSum(df, APTOS),
        'brancos': getSum(df, BRANCOS),
        'nulos': getSum(df, NULOS),
        'anulados': getSum(df, ANULADOS),
        'validos': getSum(df, NOMINAIS),
        'nao_considerados': getSum(df, APTOS) - getSum(df, NOMINAIS)
    }

def getConsolidateNumbers (df):
    return factoryData(df)

def getConsolidateNumbersByZona (df):
    zonas = df[['zona', APTOS, NOMINAIS, ABSTENCOES, BRANCOS, NULOS, ANULADOS]].groupby(['zona']).sum()
    return zonas
