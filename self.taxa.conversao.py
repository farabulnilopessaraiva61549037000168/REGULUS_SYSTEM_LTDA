import json
import requests
import pandas as pd
import matplotlib.pyplot as plt

class SistemaPagamentoInteligente:
    def __init__(self):
        """Inicializa o sistema com métodos de pagamento."""
        self.pagamentos = {
            "Brasil": ["PagSeguro", "Mercado Pago", "Pix via Gerencianet", "Juno"],
            "Internacional": ["PayPal", "Stripe", "Wise"]
        }
        self.taxa_conversao = 5.50  # Simulação de taxa de câmbio do dólar para reais
        self.transacoes = pd.DataFrame(columns=["Cliente", "Valor", "Método", "Origem"])

    def selecionar_metodo(self, origem, valor):
        """Sugere o melhor método de pagamento baseado na origem e no valor."""
        if origem.lower() == "brasil":
            metodo = "Pix via Gerencianet" if valor < 1000 else "PagSeguro"
        else:
            metodo = "Wise" if valor > 5000 else "PayPal"
        return f"Método sugerido: {metodo} para pagamento de R$ {valor:.2f}"

    def calcular_taxa(self, metodo, valor):
        """Calcula a taxa de processamento para cada método."""
        taxas = {
            "PagSeguro": 2.99,
            "Mercado Pago": 3.49,
            "Pix via Gerencianet": 1.00,
            "Juno": 2.50,
            "PayPal": 4.50,
            "Stripe": 3.90,
            "Wise": 2.00
        }
        taxa_aplicada = (taxas.get(metodo, 3.00) / 100) * valor
        return f"Taxa aplicada para {metodo}: R$ {taxa_aplicada:.2f}"

    def gerar_link_pagamento(self, cliente, valor, origem):
        """Cria um link de pagamento simulado baseado na escolha do método."""
        metodo = self.selecionar_metodo(origem, valor).split(":")[1].strip()
        self.transacoes.loc[len(self.transacoes)] = [cliente, valor, metodo, origem]
        return f"Link de pagamento gerado para {cliente} via {metodo}. Valor: R$ {valor:.2f}"

    def visualizar_transacoes(self):
        """Gera gráficos interativos com informações sobre pagamentos."""
        if self.transacoes.empty:
            return "Nenhuma transação registrada ainda."
        
        plt.figure(figsize=(10, 5))
        self.transacoes.groupby("Método")["Valor"].sum().plot(kind='bar', color='steelblue')
        plt.xlabel("Método de Pagamento")
        plt.ylabel("Valor Total (R$)")
        plt.title("Fluxo de Pagamentos por Método")
        plt.grid(True)
        plt.show()

# Exemplo de uso
sistema = SistemaPagamentoInteligente()
print(sistema.selecionar_metodo("Brasil", 800))
print(sistema.calcular_taxa("PayPal", 1500))
print(sistema.gerar_link_pagamento("Cliente XYZ", 2500, "Internacional"))
sistema.visualizar_transacoes()
