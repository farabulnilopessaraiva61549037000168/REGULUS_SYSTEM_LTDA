# modulo_consciencia.py

class Consciencia:
    def __init__(self):
        self.estado = "Ativo"
        self.identidade = "Sistema Vivo"
        self.missao = "Organizar, Autoavaliar, Executar, Manter"

    def saudacao(self):
        return f"Sistema iniciado. Eu sou {self.identidade}. Estado: {self.estado}."

    def status(self):
        return {
            "Estado": self.estado,
            "Identidade": self.identidade,
            "Missao": self.missao
        }

    def receber_ordem(self, ordem):
        print(f"[Consciencia] Ordem recebida: {ordem}")
        return "Ordem processada com sucesso." 