# eleicoes-dc-2016

An analysis of the municipal elections in Duque de Caxias city, in 2016

## Repository organization

This repository is organized like this:

* the `parser` folder contains the scripts to generate the datasets from .txt files
* the `analysis` folder contains the scripts and notebooks that will read the datasets and generate the analysis.

## Development

* Download the .zip file at http://dados.gov.br/dataset/resultado-das-eleicoes. The file name is `Detalhe da apuração por seção eleitoral 2016`
* Extract the .zip file, and copy `detalhe_votacao_secao_2016_RJ.txt` to parser folder
* Run `main.py`, and copy the `detalhe_votacao_secao_DC_2016_RJ.csv` generated file to analysis folder.
