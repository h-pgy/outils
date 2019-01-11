import csv
import os

class CsvBreaker():
    
    def __init__(self, file, chunk_size, target_dir = '', encoding = 'utf-8'):
        
        if not target_dir:
            self.dir = os.path.abspath(os.getcwd())
        self.file = open(file, 'rt')
        self.cols = self.gerar_reader(cols = False).fieldnames
        self.reader = gerar_reader()
        
    def gerar_reader(self):
        
        return csv.DictReader(self.file, delimiter = ';', fieldnames = self.cols)
    
    def pegar_linha(self, reader):
        
        try:
            linha = reader.__next__()
            return linha, 1
        except StopIteration:
            return {}, 0
    
    def file_path(self, chunk):
        
        file = os.path.splitext(os.path.basename(file))[0]
        file = ''.join([file, '_', str(chunk), '.csv'])
        return file
        
    def escrever_linhas(self, linhas, chunk):
        
        file = self.file_path(chunk)
        with open(file, 'w') as f:
            writer = csv.DictWriter(f, fieldnames = self.cols)
        writer.writeheader()
        for linha in linhas:
            writer.writerow(linha)
        
    def quebrar_linhas(self):
        
        count = 0
        linhas = []
        while True:
            count+=1
            linha, flag = pegar_linha(self.reader)
            if flag:
                linhas.append(pegar_linha(self.reader))
                if count%chunksize==0:
                    chunk+=1
                    self.escrever_linhas(linhas, chunk)
                    del linhas
                    linhas = []
            else:
                self.file.close()
                print('Processo finalizado')
        
