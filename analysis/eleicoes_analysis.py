# -*- coding: utf-8 -*-

# imports
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
        'nao_considerados': getSum(df, NAO_CONSIDERADOS)
    }

def getConsolidateNumbers (df):
    return factoryData(df)

def getConsolidateNumbersByZona (df):
    zonas = df[['zona', APTOS, NOMINAIS, ABSTENCOES, BRANCOS, NULOS, ANULADOS, NAO_CONSIDERADOS]].groupby(['zona']).sum()
    return zonas

def getConsolidateNumbersByZonaSecao (df):
    items = df[['zona', 'secao', APTOS, NOMINAIS, ABSTENCOES, BRANCOS, NULOS, ANULADOS, NAO_CONSIDERADOS]].groupby(['zona', 'secao']).sum()
    return items

def getStatisticAnalysisByProp (df, prop):
    return {
        'mean': round(df[prop].mean()),
        'median': round(df[prop].median()),
        'std': round(df.loc[:,prop].std()),
        'var': round(df.loc[:,prop].var())
    }

def generatePieChart (go, labels, values, title, marker = dict()):
    textfont = {
        'size': 15
    }
    trace = go.Pie(
        labels=labels,
        values=values,
        textinfo='percent+value+label',
        textfont=textfont,
        marker=marker
    )
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
        proportion_texts = list(
            map(lambda x : '{}%'.format(round(x, 2)), proportion)
        )
        traces.append(
            go.Bar(
                x = x,
                y = proportion,
                hoverinfo = 'text',
                hovertext = proportion_texts,
                name = labels.get(prop)
            )
        )
    
    return traces

def generatedStackedBar (go, data, title, x, y):
    layout = go.Layout(title = title, xaxis = { 'title': x }, yaxis = { 'title': y }, barmode='stack')
    fig = go.Figure(data=data, layout=layout)
    return fig

def getConsolidateNumbersByCandidate (df):
    props = [ 'DICA', 'WASHINGTON REIS' ]
    return df[props].sum()

def factoryNameVote (name, votes):
    return {
        'name': name,
        'votes': votes
    }

def getNameVotesByCandidate (df):
    indexes = list(df.index)
    return {
        'cand1': factoryNameVote(name=indexes[0], votes=df[indexes[0]]),
        'cand2': factoryNameVote(name=indexes[1], votes=df[indexes[1]])
    }

def generateScatterTrace (df, go, prop):
    _count = len(df)
    return go.Scatter(x = list(range(_count)), y = df[prop], mode = 'markers')

def generateScatterLayout (df, go, prop, title):
    _count = len(df)
    _mean = df[prop].mean()
    return go.Layout(title=title, yaxis={'title':'Numeros absolutos'}, xaxis={'title': 'Seção'}, shapes= [
        # Line Horizontal
        {
            'type': 'line',
            'x0': _mean,
            'y0': _mean,
            'x1': _count,
            'y1': _mean,
        }
    ])

def generateScatterFigure (df, go, prop, title):
    data = [ generateScatterTrace(df, go, prop) ]
    layout = generateScatterLayout(df, go, prop, title)
    return go.Figure(data=data, layout=layout)
