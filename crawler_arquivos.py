import os
import pandas as pd
from pathlib import PurePath

def crawler_arquivos_tipo(extension, dir_ = os.getcwd()):
    '''Percorre uma árvore de diretórios e obtém os 
    paths absolutos de todos os arquivos de uma determinada extensão'''
    
    paths = [(tupla[0], tupla[2]) for tupla in list(os.walk(dir_))]
    path_files = [os.path.abspath(os.path.join(tupla[0], file)) for tupla in paths for file in tupla[1]]
    files = [path for path in path_files if os.path.isfile(path) and extension == PurePath(path).suffix]
    
    return files

def tipos_arquivos(dir_ = os.getcwd()):
    '''Percorre uma árvore de diretórios e obtém o 
    conjunto de extensões de arquivo únicas presentes nessa árvore'''
    
    paths = [(tupla[0], tupla[2]) for tupla in list(os.walk(dir_))]
    path_files = [os.path.abspath(os.path.join(tupla[0], file)) for tupla in paths for file in tupla[1]]
    file_types = set(PurePath(path).suffix for path in path_files if os.path.isfile(path))
    
    return file_types

def contar_arquivos_tipo(dir_ = os.getcwd()):
    '''Percorre uma árvore de diretórios e retorna um dicionário contendo
    a contagem de arquivos presentes nesta árvore por extensão de arquivo'''
    
    result = {}
    file_types = tipos_arquivos(dir_)
    for type_ in file_types:
        if type_ not in result.keys():
            result[type_] = len(crawler_arquivos_tipo(type_, dir_))
    return result

def todos_os_paths(dir_ = os.getcwd(), tipos_indesejados = []):
    '''Obtém todos os paths absolutos dos arquivos contidos em uma determinada árvore de diretórios,
    retornando um dicionário que contém como chave a extensão do arquivo e como valor a lista de arquivos
    desta extensão contidos na árvore de diretórios.
    Opcionalmente, pode-se passar uma lista de extensões indesejadas, que serão ignoradas e não estarão presentes
    no dicionário de retorno.'''
    
    result = {}
    file_types = tipos_arquivos(dir_)
    for type_ in file_types:
        if type_ not in tipos_indesejados:
            result[type_] = crawler_arquivos_tipo(type_, dir_)
    return result

def remover_extensoes_erradas(paths, lista_extensoes):
    '''Remove as extensões de arquivo indesejadas de um dicionário do tipo retornado pela função "todos os paths".
    Essa função tem por objetivo evitar ter que rodar novamente a função anterior, otimizando o trabalho'''
    
    for extensao in lista_extensoes:
        del paths[extensao]
    
    return paths

def diretorio_pai(path):
    '''Obtém o diretorio pai de um path de arquivo, retornando
    apenas o nome do diretorio pai, não o path inteiro'''
    
    return os.path.split(os.path.split(path)[-2])[-1]

def nome_arquivo(path):
    '''Retorna apenas o nome do arquivo - seu basename'''
    
    return os.path.basename(path)

def data_criacao(file_path):
    '''Retorna uma tupla com o ano, o mês e o dia de criação do arquivo'''
    
    time_ = os.path.getctime(file_path)
    dtime = datetime.fromtimestamp(time_)
    
    return dtime.day, dtime.month, dtime.year

def gerar_df(paths):
    '''Retorna um dataframe com as colunas abaixo, a partir da chamada das funções anteriories'''
    cols = [
            'nome_pasta',
            'nome_arquivo',
            'extensao',
            'dia_criacao',
            'mes_criacao',
            'ano_criacao',
            'path'
           ]
    result = {col:[] for col in cols}
    for tipo in paths.keys():
        for path in paths[tipo]:
            result['nome_pasta'].append(diretorio_pai(path))
            result['nome_arquivo'].append(nome_arquivo(path))
            result['extensao'].append(tipo)
            dia, mes, ano = data_criacao(path)
            result['dia_criacao'].append(dia)
            result['mes_criacao'].append(mes)
            result['ano_criacao'].append(ano)
            result['path'].append(path)
            
    return pd.DataFrame(result)
