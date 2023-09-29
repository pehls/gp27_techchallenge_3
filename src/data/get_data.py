import os
import requests as r
import zipfile

base_dir = 'data/'
sufix_files = [
        '052020',
        '062020',
        '072020',
        '082020',
        '092020',
        '102020',
        '112020',
    ]
prefix_file = 'PNAD_COVID_'
output_dir = f'{base_dir}raw/'
base_url = 'https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_PNAD_COVID19/Microdados/Dados/'

def _create_dir(dir = 'raw'):
    new_dir = f'{base_dir}{dir}'
    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)

def _download():    
    for sufix in sufix_files:
        filename = f'{prefix_file}{sufix}.zip'
        output_file = f'{output_dir}{filename}'
        print(f'{base_url}{filename}')
        res = r.get(f'{base_url}{filename}')
        with open(output_file, 'wb') as file:
            file.write(res.content)

def _unzip():
    for sufix in sufix_files:
        filename = f'{prefix_file}{sufix}.zip'
        print(filename)
        file_path = f'{output_dir}{filename}'
        zip_ref = zipfile.ZipFile(file_path)
        zip_ref.extractall(output_dir)
        zip_ref.close()
        os.remove(file_path)

def get():
    _create_dir()
    _download()
    _unzip()

get()
