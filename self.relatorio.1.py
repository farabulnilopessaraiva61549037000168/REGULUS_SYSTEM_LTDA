class Torre:
    def __init__(self, nome):
        self.nome = nome
        self.relatorio = None

    def gerar_relatorio(self):
        self.relatorio = f"Relatório gerado por {self.nome}"
        return self.relatorio

    def enviar_para_ioop(self, ioop):
        if self.relatorio:
            ioop.receber_relatorio(self.nome, self.relatorio)


class IOOP:
    def __init__(self):
        self.relatorios = {}

    def receber_relatorio(self, torre, relatorio):
        print(f"[IOOP] Relatório recebido de {torre}: {relatorio}")
        self.relatorios[torre] = relatorio

    def listar_relatorios(self):
        return self.relatorios


# Exemplo de funcionamento
ioop = IOOP()
torre_import = Torre("Importação")
torre_urban = Torre("Urbanização")

torre_import.gerar_relatorio()
torre_import.enviar_para_ioop(ioop)

torre_urban.gerar_relatorio()
torre_urban.enviar_para_ioop(ioop)

print(ioop.listar_relatorios()) 