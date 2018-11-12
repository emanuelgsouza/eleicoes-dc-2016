# -*- coding: utf-8 -*-

import sys
sys.path.append('./build_dataset')
import os
from shutil import copy2

from build_dataset.main import FactoryDataframe
from build_dataset.detalhe_votacao import addPercentualColumns

# define constants
DETALHE_FILE_NAME = 'detalhe_votacao_secao'
MUNZONA_FILE_NAME = 'detalhe_votacao_zona'
DC_CODE = '58335'
TURNO = '2'

class Cli():
    def __init__(self):
        self.csv_name = self.getCSVName()
        
    def getCSVName(self):
        return "{}_{}.csv".format(DETALHE_FILE_NAME, 'duque_de_caxias')
    
    def generateDataframeSecao(self):
        df_secao = None

        with open('data/detalhe_votacao_secao_2016_RJ.txt') as file:
            _FactoryDataframe = FactoryDataframe(file=file, codMun=DC_CODE, turno=TURNO)
            df_secao = _FactoryDataframe.buildSecaoDataframe()
        
        return df_secao

    def saveDataframe(self, df):
        df.to_csv('temp/{}'.format(self.csv_name), index=False)
        return df

    def copyFiles(self):
        src = 'temp/{}'.format(self.csv_name)
        dst = os.path.abspath('../analysis/dataset')
        copy2(src=src, dst=dst)
    
    def run (self):
        df = addPercentualColumns(self.generateDataframeSecao())

        self.saveDataframe(df)

        self.copyFiles()

def main():
    cli = Cli()

    cli.run()

if __name__ == '__main__':
    main()
