# -*- coding: utf-8 -*-

# imports
import pandas as pd
import numpy as np

# constants
APTOS = 'aptos'
ABSTENCOES = 'abstencoes'
BRANCOS = 'votos_brancos'
NULOS = 'votos_nulos'
ANULADOS = 'votos_anulados'
NOMINAIS = 'votos_nominais'
NAO_CONSIDERADOS = 'nao_considerados'

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
    zonas[NAO_CONSIDERADOS] = zonas[APTOS] - zonas[NOMINAIS]
    return zonas

def getConsolidateNumbersByZonaSecao (df):
    items = df[['zona', 'secao', APTOS, NOMINAIS, ABSTENCOES, BRANCOS, NULOS, ANULADOS]].groupby(['zona', 'secao']).sum()
    items[NAO_CONSIDERADOS] = items[APTOS] - items[NOMINAIS]
    return items

def generatePieChart (go, labels, values, title):
    trace = go.Pie(labels=labels, values=values, textinfo='percent+value+label')
    layout = go.Layout(title=title)
    fig = go.Figure(data=[trace], layout=layout)
    return fig

def getProportion (value, total):
    return np.true_divide(value, total) * 100

def generateDataToStackedBar (go, x, props, labels, df):
    traces = []
    total = df['aptos']
    for prop in props:
        values = df[prop].values
        proportion = getProportion(values, total)
        traces.append(go.Bar(x = x, y = proportion, name = labels.get(prop)))
    
    return traces

def generatedStackedBar (go, data, title, x, y):
    layout = go.Layout(title = title, xaxis = { 'title': x }, yaxis = { 'title': y }, barmode='stack')
    fig = go.Figure(data=data, layout=layout)
    return fig

def getConsolidateNumbersByCandidate (df):
    props = [ 'nome_urna_candidato', 'votos' ]
    return df[props].groupby('nome_urna_candidato').sum()

def factoryNameVote (name, votes):
    return {
        'name': name,
        'votes': votes
    }

def getNameVotesByCandidate (df):
    values = df.index.values
    return {
        'cand1': factoryNameVote(name=values[0], votes=df.iloc[0].values[0]),
        'cand2': factoryNameVote(name=values[1], votes=df.iloc[1].values[0])
    }