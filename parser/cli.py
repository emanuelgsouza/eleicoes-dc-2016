# -*- coding: utf-8 -*-

import sys
sys.path.append('./build_dataset')

import os
from shutil import copy2
import pandas as pd
import click

from build_dataset.main import FactoryDataframe
from build_dataset.detalhe_votacao import addPercentualColumns
from build_dataset.votacao_munzona import buildVotacaoZonaDataframe
from build_dataset.boletim_urna import getConsolidateCandidates, insertCandidateInformation
from build_dataset.locais_votacao import runProcess

# define constants
DETALHE_FILE_NAME = 'detalhe_votacao_secao'
MUNZONA_FILE_NAME = 'detalhe_votacao_zona'
LOCAL_VOTACAO_SECAO = 'detalhe_secao_localizacao'
LOCAL_VOTACAO_CONSOLIDADO = 'detalhe_votacao_localizacao_consolidado'
DC_CODE = '58335'
TURNO = '2'

class Cli():
    def __init__(self, municipio=DC_CODE, turno=TURNO):
        self.csv_name = None
        self.municipio = municipio
        self.turno = turno
        
    def getCSVName(self, prop):
        return "{}_{}.csv".format(prop, self.getDistrictName())
    
    def getDistrictName (self):
        return 'duque_de_caxias'
    
    def getDataframeSecao(self):
        df_secao = None

        with open('data/detalhe_votacao_secao_2016_RJ.txt', mode='rb') as file:
            _FactoryDataframe = FactoryDataframe(file=file, codMun=self.municipio, turno=self.turno)
            df_secao = _FactoryDataframe.buildSecaoDataframe()
        
        df = addPercentualColumns(df_secao)

        return df
    
    def getDataframeBoletimUrna (self):
        df = None

        with open('data/bweb_2t_RJ_31102016134235.txt', mode='rb') as file:
            _FactoryDataframe = FactoryDataframe(file=file, codMun=self.municipio, turno=self.turno)
            df = _FactoryDataframe.buildBoletimUrnaDataframe()
        
        return df

    def getDataframeByZona (self, df):
        return buildVotacaoZonaDataframe(df_detalhe_secao=df)

    def saveDataframe(self, df, prop, use_index = False):
        csv_name = self.getCSVName(prop)
        df.to_csv('temp/{}'.format(csv_name), index = use_index)
        return df
    
    def getCandidateSecoesinformation (self):
        df_secoes = self.getDataframeSecao()
        _boletimUrna = self.getDataframeBoletimUrna()
        _candidates = getConsolidateCandidates(_boletimUrna)
        df_candidates = pd.DataFrame(_candidates)
        
        consolidatedInformation = insertCandidateInformation(df_secoes=df_secoes, df_candidates=df_candidates)
        
        return pd.DataFrame(consolidatedInformation)

    def copyFiles(self, prop):
        src = 'temp/{}'.format(self.getCSVName(prop))
        dst = os.path.abspath('../analysis/dataset')
        copy2(src=src, dst=dst)
    
    def run (self):
        print('Generate initial informations')
        df = self.getCandidateSecoesinformation()
        df_zona = self.getDataframeByZona(df=df)

        print('Save detalhe_votacao_secao')
        self.saveDataframe(df, DETALHE_FILE_NAME)

        print('Save votacao_by_zona')
        self.saveDataframe(df_zona, MUNZONA_FILE_NAME, use_index=True)
        
        df_secoes = pd.read_csv('temp/detalhe_votacao_secao_duque_de_caxias.csv')
        
        df_location = pd.read_excel('data/secao_local_votacao_29_09_2016.xls')
        ( secoes_location, locations, locations_with_coordinates ) = runProcess(df_location=df_location, df_secoes=df_secoes)
        
        print('Save detalhe votacao secao with localization information')
        self.saveDataframe(pd.DataFrame(secoes_location), LOCAL_VOTACAO_SECAO)
        
        print('Save detalhe localizacao consolidado')
        self.saveDataframe(pd.DataFrame(locations_with_coordinates), LOCAL_VOTACAO_CONSOLIDADO)

        print('Copy detalhe_votacao_secao files')
        self.copyFiles(DETALHE_FILE_NAME)

        print('Copy votacao_by_zona files')
        self.copyFiles(MUNZONA_FILE_NAME)
        
        print('Copy detalhe votacao secao with localization information')
        self.copyFiles(LOCAL_VOTACAO_SECAO)

        print('Copy detalhe localizacao consolidado')
        self.copyFiles(LOCAL_VOTACAO_CONSOLIDADO)

@click.command()
@click.option('--municipio', default=DC_CODE, help='A municipio para uso (somente Rio de Janeiro)')
@click.option('--turno', default=TURNO, help='Turno que será analisado')
def main(municipio, turno):
   cli = Cli(municipio=municipio, turno=turno)

   cli.run()

if __name__ == '__main__':
   main()
