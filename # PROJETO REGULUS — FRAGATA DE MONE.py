# PROJETO REGULUS — FRAGATA DE MONETIZAÇÃO DIGITAL
# Protótipo: "O Código que Abre Portas"

import random
import time
from datetime import datetime

class ContainerDado:
    def __init__(self, tipo, valor_bruto):
        self.tipo = tipo
        self.valor_bruto = valor_bruto
        self.timestamp = datetime.now()
        self.valor_liquido = self.apurar_liquido()

    def apurar_liquido(self):
        impostos = 0.06  # Taxa simbólica para simulação tributária otimizável
        return round(self.valor_bruto * (1 - impostos), 2)

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] Pacote: {self.tipo} | Bruto: R${self.valor_bruto} | Líquido: R${self.valor_liquido}"


class FragataRegulus:
    def __init__(self, nome):
        self.nome = nome
        self.tanque_financeiro = 0.0
        self.log_transacoes = []
        self.containers_vendidos = 0

    def gerar_container(self):
        tipo = random.choice(["Dados de Tráfego", "Metrica Comercial", "Padrão de Consumo", "API de Tendência"])
        valor = round(random.uniform(50, 500), 2)
        return ContainerDado(tipo, valor)

    def vender_container(self, container):
        self.tanque_financeiro += container.valor_liquido
        self.containers_vendidos += 1
        log = f"VENDA: {container}"
        self.log_transacoes.append(log)
        print(log)

    def simular_voo_comercial(self, ciclos=5):
        print(f"Iniciando voo da Fragata: {self.nome}")
        for _ in range(ciclos):
            time.sleep(1)  # Simula tempo de operação
            container = self.gerar_container()
            self.vender_container(container)
        print(f"\n>>> FIM DO VOO: Tanque Acumulado = R${round(self.tanque_financeiro, 2)} | Containers vendidos: {self.containers_vendidos}\n")

        if self.tanque_financeiro >= 1000:
            print("\u2705 Missão comercial bem-sucedida. Abriu portas para expansão.")
        else:
            print("\u26a0️ Captação abaixo do ideal. Replanejamento necessário.")


# Iniciar a Fragata
if __name__ == "__main__":
    regulus = FragataRegulus("Regulus I — Aurora")
    regulus.simular_voo_comercial(ciclos=10)
