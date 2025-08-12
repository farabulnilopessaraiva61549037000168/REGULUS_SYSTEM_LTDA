# modulo_relatorios.py

class Relatorio:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, item):
        self.itens.append(item)

    def gerar(self):
        print("[Relatorio] Gerando relatório...")
        return "\n".join(self.itens) 