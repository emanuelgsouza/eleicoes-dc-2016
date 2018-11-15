# -*- coding: utf-8 -*-

import requests

def factoryData (row):
    return {
        'zona': int(row['zona']),
        'secao': int(row['secao']),
        'codigo_municipio': int(row['munic']),
        'nome_munic': row['nome_munic'],
        'bairro': row['bairro'],
        'endereco': row['endereco'],
        'cep': int(row['cep']),
        'num_local': int(row['num_local']),
        'nome_local': row['nome_local'],
        'location': '{}, {}, {}, Rio de Janeiro'.format(row['endereco'], row['bairro'], row['nome_munic'])
    }

def processIntern (item):
    (key, value) = item
    _key = key.lower().replace(' ', '_')
    return (_key, value)

def processKeys (row):
    return dict(list(map(processIntern, row.items())))


def computeAddressFromRow (row):
    return factoryData(processKeys(row=row))

def processLocations (df_location):
    values = df_location.to_dict(orient='index').values()
    return list(map(computeAddressFromRow, values))

def insertLocationAtSecoesDataset (df_location, df_secoes):
    locations = processLocations(df_location)
    secoes = df_secoes.to_dict(orient='index').values()
    _secoes = []
    
    for secao in secoes:
        _secao = secao['secao']
        _zona = secao['zona']
        _codigo_municipio = secao['codigo_municipio']
        location = list(
            filter(
                lambda l : l['secao'] == _secao and l['zona'] == _zona and l['codigo_municipio'] == _codigo_municipio,
                locations
            )
        )[0]
        
        s = secao.copy()
        s.update(location)
        _secoes.append(s)
        
    return _secoes

def factoryConsolidatedLocation (data):
    return {
        'zona': data['zona'],
        'nome_munic': data['nome_munic'],
        'bairro': data['bairro'],
        'endereco': data['endereco'],
        'cep': data['cep'],
        'num_local': data['num_local'],
        'nome_local': data['nome_local'],
        'location': data['location'],
        'secoes': [ data['secao'] ],
        'aptos': [ data['aptos'] ],
        'abstencoes': [ data['abstencoes'] ],
        'DICA': [ data['DICA'] ],
        'WASHINGTON REIS': [ data['WASHINGTON REIS'] ],
        'nao_considerados': [ data['nao_considerados'] ],
        'votos_anulados': [ data['votos_anulados'] ],
        'votos_brancos': [ data['votos_brancos'] ],
        'votos_legenda': [ data['votos_legenda'] ],
        'votos_nominais': [ data['votos_nominais'] ],
        'votos_nulos': [ data['votos_nulos'] ]
    }

def computedConsolidateLocation (data, row):
    data['secoes'].append(row['secao'])
    data['aptos'].append(row['aptos'])
    data['abstencoes'].append(row['abstencoes'])
    data['DICA'].append(row['DICA'])
    data['WASHINGTON REIS'].append(row['WASHINGTON REIS'])
    data['nao_considerados'].append(row['nao_considerados'])
    data['votos_anulados'].append(row['votos_anulados'])
    data['votos_brancos'].append(row['votos_brancos'])
    data['votos_legenda'].append(row['votos_legenda'])
    data['votos_nominais'].append(row['votos_nominais'])
    data['votos_nulos'].append(row['votos_nulos'])
    return data

def consolidateLocation (data):
    _data = data.copy()
    _data['secoes'] = len(data['secoes'])
    _data['aptos'] = sum(data['aptos'])
    _data['abstencoes'] = sum(data['abstencoes'])
    _data['DICA'] = sum(data['DICA'])
    _data['WASHINGTON REIS'] = sum(data['WASHINGTON REIS'])
    _data['nao_considerados'] = sum(data['nao_considerados'])
    _data['votos_anulados'] = sum(data['votos_anulados'])
    _data['votos_brancos'] = sum(data['votos_brancos'])
    _data['votos_legenda'] = sum(data['votos_legenda'])
    _data['votos_nominais'] = sum(data['votos_nominais'])
    _data['votos_nulos'] = sum(data['votos_nulos'])
    return _data

def processSecoesLocations (secoes_locations):
    data = dict()
    
    for s in secoes_locations:
        _location = s['location']
        if _location in data:
            _data = computedConsolidateLocation(data[_location], s)
            data[_location] = _data
        else:
            data[_location] = factoryConsolidatedLocation(s)
        
    _data = list(
        map(consolidateLocation, data.values())
    )   
    return _data

URL_HERE = 'https://geocoder.api.here.com/6.2/geocode.json'
APP_ID = ''
APP_CODE = ''

def factoryUrl (address):
    return '{}?app_id={}&app_code={}&searchtext={}'.format(URL_HERE, APP_ID, APP_CODE, address)

'''
- Pegarás a lista de localizacoes já processadas e filtradas por municípo para fazer a requisição
na api do HERE Maps
'''
def loadCoordinates (locations):
    _locations = []
    count = 1
    total = len(locations)

    for location in locations:
        print('Process {}/{}'.format(count, total))
        _location = location.copy()
        
        locationAddress = _location['location']
        print('Process lat and lon to {}'.format(locationAddress))

        try:
            url = factoryUrl(locationAddress)
            r = requests.get(url)
            coordinates = getCoordinates(r.json())
            print('url')
            print(url)
            print('Coordinates found')
            print(coordinates)
            print('')
            _location['lat'] = coordinates.get('lat')
            _location['lon'] = coordinates.get('lon')
        except Exception as e:
            print(e)
            lat = None
            lon = None
            _location['lat'] = lat
            _location['lon'] = lon
        finally:
            _locations.append(_location)
        
        count += 1
    return _locations

def getCoordinates (response):
    _response = response.get('Response')
    view = _response.get('View')[0]
    result = view.get('Result')[0]
    location_position = result.get('Location').get('DisplayPosition')
    return {
        'lat': location_position.get('Latitude'),
        'lon': location_position.get('Longitude')
    }

'''
- Rodar o processo de consolidaçao das informaçoes por secao juntamente com localizacao
- Retornar uma tupla com tres arrays de dicionarios:
    (
         secoes_location = informacoes de secoes com suas respectivas informacoes de secao
         locations = localizacoes consolidadas
         locations_with_coordinates = localizacoes consolidadas, com os dados de latitude e longitude     
    )
'''
def runProcess (df_location, df_secoes):
    secoes_location = insertLocationAtSecoesDataset(df_location, df_secoes)
    locations = processSecoesLocations(secoes_locations=secoes_location)
    locations_with_coordinates = loadCoordinates(locations=locations)
    
    return ( secoes_location, locations, locations_with_coordinates )
