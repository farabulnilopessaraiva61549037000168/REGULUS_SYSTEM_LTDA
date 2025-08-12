# modulo_varredura.py

import os

class Varredura:
    def __init__(self, diretorio):
        self.diretorio = diretorio

    def listar_arquivos(self):
        arquivos = []
        for raiz, dirs, files in os.walk(self.diretorio):
            for file in files:
                arquivos.append(os.path.join(raiz, file))
        return arquivos

    def diagnostico(self):
        arquivos = self.listar_arquivos()
        print(f"[Varredura] {len(arquivos)} arquivos encontrados.")
        return arquivos 