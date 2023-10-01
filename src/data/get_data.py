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
base_url = 'https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_PNAD_COVID19/Microdados/Dados/'

def _create_dir(new_dir = 'raw'):
    if not os.path.isdir(new_dir):
        print(f'-- Creating directory {new_dir}')
        os.makedirs(new_dir)

def _download(output_dir = f'{base_dir}raw/'):    
    _create_dir(output_dir)
    for sufix in sufix_files:
        filename = f'{prefix_file}{sufix}.zip'
        output_file = f'{output_dir}{filename}'
        print(f'-- Downloading {base_url}{filename} to {output_file}')
        res = r.get(f'{base_url}{filename}')
        with open(output_file, 'wb') as file:
            file.write(res.content)
        _unzip(output_dir, filename, sufix)
        

def _unzip(output_dir, filename, sufix):
    filename = f'{prefix_file}{sufix}.zip'
    print(f'-- Unzipping {filename} to {output_dir}')
    file_path = f'{output_dir}{filename}'
    zip_ref = zipfile.ZipFile(file_path)
    zip_ref.extractall(output_dir)
    zip_ref.close()
    os.remove(file_path)

def _download_docs():
    prefix_file = 'Dicionario_PNAD_COVID_'
    fixed_sufix_file = '_20220621.xls'
    base_url = 'https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_PNAD_COVID19/Microdados/Documentacao/'
    output_dir = f'{base_dir}raw/dimensoes/'
    _create_dir(output_dir)
    for sufix in sufix_files:
        filename = f'{prefix_file}{sufix}{fixed_sufix_file}'
        output_file = f'{output_dir}{filename}'
        print(f'-- Downloading{base_url}{filename} to {output_file}')
        res = r.get(f'{base_url}{filename}')
        with open(output_file, 'wb') as file:
            file.write(res.content)

def get():
    _download()
    _download_docs()

if __name__ == '__main__':
    get()
