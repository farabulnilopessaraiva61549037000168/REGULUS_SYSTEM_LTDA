class ComplexoDigital:
    def __init__(self):
        self.nome = "Complexo IO Ômega"
        self.estagios = ["superfície", "subsolo", "mares de dados", "céus digitais"]
        self.mineracao = {
            "tipo": "multi-dimensional",
            "camadas": self.estagios,
            "metodo": "captura inteligente de dados em tempo real",
            "automacao": True
        }
        self.fiscalizacao = {
            "modo": "transparente",
            "imposto_percentual": 25,
            "relatorio_mensal": True
        }
        self.economia = {
            "ganhos_brutos": 0,
            "imposto_pago": 0,
            "lucro_liquido": 0
        }

    def processar_fluxo(self, ganho_bruto_dia):
        imposto = ganho_bruto_dia * (self.fiscalizacao["imposto_percentual"] / 100)
        liquido = ganho_bruto_dia - imposto
        self.economia["ganhos_brutos"] += ganho_bruto_dia
        self.economia["imposto_pago"] += imposto
        self.economia["lucro_liquido"] += liquido

    def relatorio_desenvolvimento_autonomia(self):
        print("\n📊 RELATÓRIO DE DESENVOLVIMENTO E AUTONOMIA:")
        print(f"🔹 Nome do Complexo: {self.nome}")
        print(f"🔹 Estágios Operacionais: {', '.join(self.estagios)}")
        print(f"⚙️ Tipo de Mineração: {self.mineracao['tipo']}")
        print(f"⚙️ Método de Mineração: {self.mineracao['metodo']}")
        print(f"🔄 Automação: {'Ativada' if self.mineracao['automacao'] else 'Desativada'}")
        print(f"📈 Modo de Fiscalização: {self.fiscalizacao['modo']}")
        print(f"💰 Imposto Percentual: {self.fiscalizacao['imposto_percentual']}%")
        print(f"📊 Economia Atual:")
        for chave, valor in self.economia.items():
            print(f"   - {chave.replace('_', ' ').title()}: R$ {valor:,.2f}")

if __name__ == "__main__":
    IO_OMEGA = ComplexoDigital()

    # Exemplo de captação de R$180.000 em um dia típico
    IO_OMEGA.processar_fluxo(180_000)
    IO_OMEGA.relatorio_desenvolvimento_autonomia()
