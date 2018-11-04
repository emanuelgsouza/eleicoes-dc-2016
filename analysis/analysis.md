
# Eleições para segundo turno em Duque de Caxias - RJ

Antes de qualquer código e gráfico, vamos a alguns conceitos que serão colocados nas análises a seguir:

As eleições para os cargos executivos (prefeito, governador e presidente) são eleições majoritárias, isto é, o candidato eleito será o que tiver mais votos. A questão levantada e analisada a seguir, é que o cálculo da eleição, é feita em cima dos votos válidos.

Este trabalho, porém, traz para análise, os votos ou eleitores que não são considerados. Então, será mostrado no cálculo, os votos brancos e nulos, como também as abstenções.


```python
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
py.init_notebook_mode(connected=True)
from eleicoes_analysis import *

df = pd.read_csv('detalhe_votacao_secao_DC_2016_RJ.csv')

numeros_consolidados = getConsolidateNumbers(df)
total_votos_validos = numeros_consolidados.get('validos')
total_votos_nao_considerados = numeros_consolidados.get('nao_considerados')
total_abstencoes = numeros_consolidados.get('abstencoes')
total_brancos = numeros_consolidados.get('brancos')
total_nulos = numeros_consolidados.get('nulos')
```


<script>requirejs.config({paths: { 'plotly': ['https://cdn.plot.ly/plotly-latest.min']},});if(!window.Plotly) {{require(['plotly'],function(plotly) {window.Plotly=plotly;});}}</script>


## Visualizando os dados

### Visualizando os dados em geral

#### Proporção de eleitores considerados (votos válidos) em relação aos não considerados


```python
values = [total_votos_validos, total_votos_nao_considerados]
labels = [ 'Computados', 'Não Computados' ]

title = 'O eleitorado divido em: eleitores (votos) computados e não computados'
fig = generatePieChart(go=go, labels=labels, values=values, title=title)
py.iplot(fig)
```


<div id="9a9f1f4b-32ae-42ca-ac4f-bbaff3116795" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("9a9f1f4b-32ae-42ca-ac4f-bbaff3116795", [{"labels": ["Computados", "N\u00e3o Computados"], "textinfo": "percent+value", "values": [402030, 226134], "type": "pie", "uid": "e47c6f70-e058-11e8-b858-5cc9d399d62a"}], {"title": "O eleitorado divido em: eleitores (votos) computados e n\u00e3o computados"}, {"showLink": true, "linkText": "Export to plot.ly"})});</script>


#### Visualizando a divisão entre os não considerados


```python
values = [total_votos_validos, total_abstencoes, total_brancos, total_nulos]
labels = [ 'Válidos', 'Abstenções', 'Brancos', 'Nulos' ]

title = 'Proporcao de eleitores em votos válidos e não computados'
fig = generatePieChart(go=go, labels=labels, values=values, title=title)
py.iplot(fig)
```


<div id="c8aeff2f-112d-46b6-81ed-6e5f6281e9ca" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("c8aeff2f-112d-46b6-81ed-6e5f6281e9ca", [{"labels": ["V\u00e1lidos", "Absten\u00e7\u00f5es", "Brancos", "Nulos"], "textinfo": "percent+value", "values": [402030, 149714, 18337, 58083], "type": "pie", "uid": "e58d920e-e058-11e8-b858-5cc9d399d62a"}], {"title": "Proporcao de eleitores em votos v\u00e1lidos e n\u00e3o computados"}, {"showLink": true, "linkText": "Export to plot.ly"})});</script>


### Visualizando os dados por zona

#### Proporção de eleitores considerados (votos válidos) em relação aos não considerados


```python
agrupado_por_zona = getConsolidateNumbersByZona(df)
zonas = agrupado_por_zona.index.values

_zonas = list(map(lambda z : 'Z-{}'.format(z), zonas))

props = ['votos_nominais', 'nao_considerados']
labels = { 'votos_nominais': 'Válidos', 'nao_considerados': 'Não Considerados' }
title = 'Proporção de eleitores em votos válidos e não considerados'
traces = generateDataToStackedBar(go=go, x=_zonas, props=props, labels=labels, df=agrupado_por_zona)
fig = generatedStackedBar(go=go, data=traces, title=title, x='Zonas', y='% de registros')
py.iplot(fig)
```


<div id="594fe400-6e2b-479b-86e0-771678684ad4" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("594fe400-6e2b-479b-86e0-771678684ad4", [{"name": "V\u00e1lidos", "x": ["Z-66", "Z-77", "Z-78", "Z-79", "Z-103", "Z-126", "Z-127", "Z-128", "Z-194", "Z-200"], "y": [61.326262788579996, 63.59515715393332, 64.35028172249321, 65.52715476257062, 62.75046396778963, 63.20511559272012, 62.72070488603809, 69.05735574423844, 63.1549623926862, 63.208795219196205], "type": "bar", "uid": "ed8f2774-e058-11e8-b858-5cc9d399d62a"}, {"name": "N\u00e3o Considerados", "x": ["Z-66", "Z-77", "Z-78", "Z-79", "Z-103", "Z-126", "Z-127", "Z-128", "Z-194", "Z-200"], "y": [38.673737211420004, 36.40484284606668, 35.64971827750679, 34.47284523742938, 37.24953603221037, 36.79488440727988, 37.2792951139619, 30.942644255761564, 36.8450376073138, 36.791204780803795], "type": "bar", "uid": "ed8f2775-e058-11e8-b858-5cc9d399d62a"}], {"barmode": "stack", "title": "Propor\u00e7\u00e3o de eleitores em votos v\u00e1lidos e n\u00e3o considerados", "xaxis": {"title": "Zonas"}, "yaxis": {"title": "% de registros"}}, {"showLink": true, "linkText": "Export to plot.ly"})});</script>


#### Visualizando a divisão entre os não considerados


```python
title = 'Proporção de eleitores em votos válidos e não considerados'
props = ['votos_nominais', 'abstencoes', 'votos_brancos', 'votos_nulos']
labels = { 'votos_nominais': 'Nominais', 'abstencoes' : 'Abstencoes', 'votos_brancos': 'Brancos', 'votos_nulos': 'Nulos' }
traces = generateDataToStackedBar(go=go, x=_zonas, props=props, labels=labels, df=agrupado_por_zona)
fig = generatedStackedBar(go=go, data=traces, title=title, x='Zonas', y='% de registros')
py.iplot(fig)
```


<div id="3ef9b72d-b4a5-474e-b77c-4ae1b908f7ee" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("3ef9b72d-b4a5-474e-b77c-4ae1b908f7ee", [{"name": "Nominais", "x": ["Z-66", "Z-77", "Z-78", "Z-79", "Z-103", "Z-126", "Z-127", "Z-128", "Z-194", "Z-200"], "y": [61.326262788579996, 63.59515715393332, 64.35028172249321, 65.52715476257062, 62.75046396778963, 63.20511559272012, 62.72070488603809, 69.05735574423844, 63.1549623926862, 63.208795219196205], "type": "bar", "uid": "b19b319c-e05b-11e8-b858-5cc9d399d62a"}, {"name": "Abstencoes", "x": ["Z-66", "Z-77", "Z-78", "Z-79", "Z-103", "Z-126", "Z-127", "Z-128", "Z-194", "Z-200"], "y": [27.312657346403128, 25.41599570585078, 23.960599386561093, 22.920745008110075, 26.661633795728353, 22.653221839645845, 23.28885946791148, 20.965170680991164, 23.395041406032366, 25.201861228958535], "type": "bar", "uid": "b19b319d-e05b-11e8-b858-5cc9d399d62a"}, {"name": "Brancos", "x": ["Z-66", "Z-77", "Z-78", "Z-79", "Z-103", "Z-126", "Z-127", "Z-128", "Z-194", "Z-200"], "y": [2.4130912207402644, 2.78821494602493, 2.7185882798038077, 3.0113541025784443, 2.2443458840552357, 3.3999016232169206, 3.7572617186162507, 2.207589672500433, 3.087091954314078, 2.575156242872132], "type": "bar", "uid": "b19b319e-e05b-11e8-b858-5cc9d399d62a"}, {"name": "Nulos", "x": ["Z-66", "Z-77", "Z-78", "Z-79", "Z-103", "Z-126", "Z-127", "Z-128", "Z-194", "Z-200"], "y": [8.947988644276608, 8.200632194190971, 8.97053061114189, 8.540746126740869, 8.343556352426788, 10.741760944417116, 10.233173927434173, 7.769883902269971, 10.362904246967357, 9.01418730897313], "type": "bar", "uid": "b19b319f-e05b-11e8-b858-5cc9d399d62a"}], {"barmode": "stack", "title": "Propor\u00e7\u00e3o de eleitores em votos v\u00e1lidos e n\u00e3o considerados", "xaxis": {"title": "Zonas"}, "yaxis": {"title": "% de registros"}}, {"showLink": true, "linkText": "Export to plot.ly"})});</script>


### Visualizando os dados por seção

O objetivo aqui é trazer as dez seções com mais eleitores aptos

#### Proporção de eleitores considerados (votos válidos) em relação aos não considerados


```python
# ordenando por quantidade de aptos
sorted = df.sort_values(by='aptos', ascending=False)
items_grouped = getConsolidateNumbersByZonaSecao(sorted.iloc[:10])
zonas_secao = list(map(lambda x : '(z, s) - {}'.format(x), items_grouped.index.values))
props = ['votos_nominais', 'nao_considerados']
labels = { 'votos_nominais': 'Válidos', 'nao_considerados': 'Não Considerados' }
title = 'Proporção de eleitores em votos válidos e não considerados'
traces = generateDataToStackedBar(go=go, x=zonas_secao, props=props, labels=labels, df=items_grouped)
fig = generatedStackedBar(go=go, data=traces, title=title, x='Zonas', y='% de registros')
py.iplot(fig)
```


<div id="ab45fb15-b7ab-44d4-a121-cbe60cccb39d" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("ab45fb15-b7ab-44d4-a121-cbe60cccb39d", [{"name": "V\u00e1lidos", "x": ["(z, s) - (66, 9)", "(z, s) - (66, 170)", "(z, s) - (79, 25)", "(z, s) - (79, 26)", "(z, s) - (79, 27)", "(z, s) - (79, 28)", "(z, s) - (79, 29)", "(z, s) - (79, 562)", "(z, s) - (79, 599)", "(z, s) - (200, 48)"], "y": [54.32900432900433, 61.5546218487395, 62.98701298701299, 62.10762331838565, 65.05494505494505, 59.1703056768559, 61.30434782608696, 71.70626349892008, 68.12227074235808, 57.7922077922078], "type": "bar", "uid": "c498dd7a-e05c-11e8-b858-5cc9d399d62a"}, {"name": "N\u00e3o Considerados", "x": ["(z, s) - (66, 9)", "(z, s) - (66, 170)", "(z, s) - (79, 25)", "(z, s) - (79, 26)", "(z, s) - (79, 27)", "(z, s) - (79, 28)", "(z, s) - (79, 29)", "(z, s) - (79, 562)", "(z, s) - (79, 599)", "(z, s) - (200, 48)"], "y": [45.67099567099567, 38.445378151260506, 37.01298701298701, 37.89237668161435, 34.94505494505494, 40.8296943231441, 38.69565217391304, 28.293736501079913, 31.877729257641924, 42.2077922077922], "type": "bar", "uid": "c498dd7b-e05c-11e8-b858-5cc9d399d62a"}], {"barmode": "stack", "title": "Propor\u00e7\u00e3o de eleitores em votos v\u00e1lidos e n\u00e3o considerados", "xaxis": {"title": "Zonas"}, "yaxis": {"title": "% de registros"}}, {"showLink": true, "linkText": "Export to plot.ly"})});</script>


#### Visualizando a divisão entre os não considerados


```python
title = 'Proporção de eleitores em votos válidos e não considerados'
props = ['votos_nominais', 'abstencoes', 'votos_brancos', 'votos_nulos']
labels = { 'votos_nominais': 'Nominais', 'abstencoes' : 'Abstencoes', 'votos_brancos': 'Brancos', 'votos_nulos': 'Nulos' }
traces = generateDataToStackedBar(go=go, x=zonas_secao, props=props, labels=labels, df=agrupado_por_zona)
fig = generatedStackedBar(go=go, data=traces, title=title, x='Zonas', y='% de registros')
py.iplot(fig)
```


<div id="5828ab22-d75d-44ab-bda0-96c4c4a61790" style="height: 525px; width: 100%;" class="plotly-graph-div"></div><script type="text/javascript">require(["plotly"], function(Plotly) { window.PLOTLYENV=window.PLOTLYENV || {};window.PLOTLYENV.BASE_URL="https://plot.ly";Plotly.newPlot("5828ab22-d75d-44ab-bda0-96c4c4a61790", [{"name": "Nominais", "x": ["(z, s) - (66, 9)", "(z, s) - (66, 170)", "(z, s) - (79, 25)", "(z, s) - (79, 26)", "(z, s) - (79, 27)", "(z, s) - (79, 28)", "(z, s) - (79, 29)", "(z, s) - (79, 562)", "(z, s) - (79, 599)", "(z, s) - (200, 48)"], "y": [61.326262788579996, 63.59515715393332, 64.35028172249321, 65.52715476257062, 62.75046396778963, 63.20511559272012, 62.72070488603809, 69.05735574423844, 63.1549623926862, 63.208795219196205], "type": "bar", "uid": "c6aa7632-e05c-11e8-b858-5cc9d399d62a"}, {"name": "Abstencoes", "x": ["(z, s) - (66, 9)", "(z, s) - (66, 170)", "(z, s) - (79, 25)", "(z, s) - (79, 26)", "(z, s) - (79, 27)", "(z, s) - (79, 28)", "(z, s) - (79, 29)", "(z, s) - (79, 562)", "(z, s) - (79, 599)", "(z, s) - (200, 48)"], "y": [27.312657346403128, 25.41599570585078, 23.960599386561093, 22.920745008110075, 26.661633795728353, 22.653221839645845, 23.28885946791148, 20.965170680991164, 23.395041406032366, 25.201861228958535], "type": "bar", "uid": "c6aa7633-e05c-11e8-b858-5cc9d399d62a"}, {"name": "Brancos", "x": ["(z, s) - (66, 9)", "(z, s) - (66, 170)", "(z, s) - (79, 25)", "(z, s) - (79, 26)", "(z, s) - (79, 27)", "(z, s) - (79, 28)", "(z, s) - (79, 29)", "(z, s) - (79, 562)", "(z, s) - (79, 599)", "(z, s) - (200, 48)"], "y": [2.4130912207402644, 2.78821494602493, 2.7185882798038077, 3.0113541025784443, 2.2443458840552357, 3.3999016232169206, 3.7572617186162507, 2.207589672500433, 3.087091954314078, 2.575156242872132], "type": "bar", "uid": "c6aa7634-e05c-11e8-b858-5cc9d399d62a"}, {"name": "Nulos", "x": ["(z, s) - (66, 9)", "(z, s) - (66, 170)", "(z, s) - (79, 25)", "(z, s) - (79, 26)", "(z, s) - (79, 27)", "(z, s) - (79, 28)", "(z, s) - (79, 29)", "(z, s) - (79, 562)", "(z, s) - (79, 599)", "(z, s) - (200, 48)"], "y": [8.947988644276608, 8.200632194190971, 8.97053061114189, 8.540746126740869, 8.343556352426788, 10.741760944417116, 10.233173927434173, 7.769883902269971, 10.362904246967357, 9.01418730897313], "type": "bar", "uid": "c6aa7635-e05c-11e8-b858-5cc9d399d62a"}], {"barmode": "stack", "title": "Propor\u00e7\u00e3o de eleitores em votos v\u00e1lidos e n\u00e3o considerados", "xaxis": {"title": "Zonas"}, "yaxis": {"title": "% de registros"}}, {"showLink": true, "linkText": "Export to plot.ly"})});</script>

