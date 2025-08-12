# modulo_acao.py

class Executor:
    def __init__(self):
        self.log = []

    def executar(self, tarefa):
        print(f"[Executor] Executando: {tarefa}")
        self.log.append(tarefa)
        return f"Tarefa '{tarefa}' concluída." 