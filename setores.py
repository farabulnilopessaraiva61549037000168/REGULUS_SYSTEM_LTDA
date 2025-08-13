import json

# Núcleo Central de Processamento da NeoCompleX
class NeoCompleX:
    def __init__(self):
        self.setores = {
            "Registro_Legal": [],
            "Modelagem_Financeira": [],
            "Organizacao_Tecnica": [],
            "Expansao_Clientes": [],
        }
        self.progresso = {}

    def adicionar_tarefa(self, setor, tarefa, status="Pendente"):
        if setor in self.setores:
            self.setores[setor].append({"tarefa": tarefa, "status": status})
            print(f"Tarefa adicionada ao setor {setor}: {tarefa}")
        else:
            print("Setor inválido.")

    def atualizar_status(self, setor, tarefa, novo_status):
        for item in self.setores.get(setor, []):
            if item["tarefa"] == tarefa:
                item["status"] = novo_status
                print(f"Status atualizado: {tarefa} agora está {novo_status}")
                return
        print("Tarefa não encontrada.")

    def visualizar_progresso(self):
        print("\n📊 Progresso da NeoCompleX\n")
        for setor, tarefas in self.setores.items():
            print(f"🔹 {setor}:")
            for item in tarefas:
                print(f"   ✅ {item['tarefa']} - {item['status']}")
            print("\n")

# Inicializando o sistema
sistema = NeoCompleX()

# Adicionando tarefas conforme os processos do projeto
sistema.adicionar_tarefa("Registro_Legal", "Solicitar CNPJ e identidade fiscal")
sistema.adicionar_tarefa("Registro_Legal", "Criar contratos e estrutura jurídica")
sistema.adicionar_tarefa("Modelagem_Financeira", "Gerar planilha automática de fluxo de caixa")
sistema.adicionar_tarefa("Modelagem_Financeira", "Implementar tabela de recebimentos multimoeda")
sistema.adicionar_tarefa("Organizacao_Tecnica", "Configurar núcleo central de processamento")
sistema.adicionar_tarefa("Expansao_Clientes", "Criar material de apresentação e proposta oficial")
sistema.adicionar_tarefa("Expansao_Clientes", "Divulgar em plataformas estratégicas")

# Atualizando status de tarefas
sistema.atualizar_status("Registro_Legal", "Solicitar CNPJ e identidade fiscal", "Concluído")

# Visualizando progresso
sistema.visualizar_progresso()
