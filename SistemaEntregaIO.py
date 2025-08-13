import time
import random

class SistemaEntregaIO:
    def __init__(self, banco_de_dados):
        self.banco = banco_de_dados

    def localizar_destinatario(self, nome):
        print(f"🔎 Procurando {nome} no banco de dados...")
        dados = self.banco.get(nome.lower())
        if dados:
            print("✅ Destinatário localizado.")
        else:
            print("❌ Destinatário não encontrado.")
        return dados

    def escolher_modo_de_envio(self, dados):
        meios = []
        if dados.get("telefone"):
            meios.append("ligação telefônica")
        if dados.get("email"):
            meios.append("envio por email")
        if dados.get("caixa_postal"):
            meios.append("envio por correspondência")
        return random.choice(meios) if meios else None

    def executar_entrega(self, nome):
        dados = self.localizar_destinatario(nome)
        if not dados:
            print("Encerrando operação.")
            return
        meio = self.escolher_modo_de_envio(dados)
        if not meio:
            print("⚠️ Nenhum meio de contato disponível.")
            return
        print(f"🚀 Executando entrega para {nome} via {meio}...")
        time.sleep(2)
        print(f"📦 Conteúdo entregue com sucesso para {nome} por {meio}.")

# 🔧 SIMULAÇÃO DE BANCO DE DADOS
banco_simulado = {
    "marina": {
        "telefone": "+55 85 90000-0000",
        "email": "marina@exemplo.com",
        "caixa_postal": "CP 12345 - Fortaleza/CE"
    },
    "joão": {
        "email": "joao@empresa.com"
    },
    "lucas": {
        "telefone": "+55 11 91111-1111"
    }
}

# 📡 EXECUÇÃO
entrega_io = SistemaEntregaIO(banco_simulado)
entrega_io.executar_entrega("Marina") 