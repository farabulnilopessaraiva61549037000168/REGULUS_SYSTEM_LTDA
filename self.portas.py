
# estrutura_nucleo.py
class NúcleoOmega:
    def __init__(self):
        self.guardioes = []
        self.portas_seguras = 3

    def adicionar_guardiao(self, nome):
        self.guardioes.append(nome)

    def status(self):
        return f"Núcleo com {len(self.guardioes)} guardiões e {self.portas_seguras} portas de verificação" 