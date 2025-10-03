# modulo_relatorios.py

class Relatorio:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, item):
        self.itens.append(item)

    def gerar(self):
        print("[Relatorio] Gerando relatório...")
        return "\n".join(self.itens)
    
    def ver(self):
        """Visualiza o conteúdo do relatório."""
        print("[Relatorio] Visualizando relatório:")
        print("=" * 50)
        if self.itens:
            for i, item in enumerate(self.itens, 1):
                print(f"{i}. {item}")
        else:
            print("Nenhum item no relatório.")
        print("=" * 50)