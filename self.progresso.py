import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class SistemaExpansaoGlobal:
    def __init__(self):
        """Inicializa o sistema com o plano de ação estruturado."""
        self.plano_expansao = {
            "2025 - 1º trimestre": {"Ação": "Infraestrutura técnica e materiais de marketing", "Países": "Global"},
            "2025 - 2º trimestre": {"Ação": "Abertura de redes sociais e networking", "Países": "Global"},
            "2025 - 3º trimestre": {"Ação": "Contato com parceiros na África e América Central", "Países": "Nigéria, Quênia, México, Guatemala, Costa Rica"},
            "2025 - 4º trimestre": {"Ação": "Lançamento de projetos-piloto e consultorias iniciais", "Países": "África e América Central"},
            "2026 - 1º trimestre": {"Ação": "Expansão para Sudeste Asiático", "Países": "Filipinas, Vietnã, Indonésia"},
            "2026 - 2º trimestre": {"Ação": "Formalização de parcerias e certificações", "Países": "Global"},
            "2026 - 3º trimestre": {"Ação": "Lançamento de serviços premium", "Países": "Oriente Médio"},
            "2026 - 4º trimestre": {"Ação": "Consolidação do portfólio internacional", "Países": "Global"}
        }
        self.progresso = pd.DataFrame(columns=["Trimestre", "Status"])

    def visualizar_plano(self):
        """Exibe o plano estratégico formatado."""
        return json.dumps(self.plano_expansao, indent=4)

    def atualizar_status(self, trimestre, status):
        """Atualiza o status de implementação de cada fase."""
        self.progresso.loc[len(self.progresso)] = [trimestre, status]
        return f"Status atualizado: {trimestre} -> {status}"

    def gerar_dashboard(self):
        """Gera gráficos mostrando progresso e implementação global."""
        if self.progresso.empty:
            return "Nenhum progresso registrado ainda."
        
        plt.figure(figsize=(10, 5))
        self.progresso.groupby("Status")["Trimestre"].count().plot(kind='bar', color='green')
        plt.xlabel("Status de Implementação")
        plt.ylabel("Número de Trimestres")
        plt.title("Progresso do Plano de Expansão")
        plt.grid(True)
        plt.show()

# Exemplo de uso
sistema = SistemaExpansaoGlobal()
print(sistema.visualizar_plano())
print(sistema.atualizar_status("2025 - 1º trimestre", "Concluído"))
print(sistema.atualizar_status("2025 - 2º trimestre", "Em andamento"))
sistema.gerar_dashboard()
