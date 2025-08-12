# main.py

from modulo_consciencia import Consciencia
from modulo_varredura import Varredura
from modulo_acao import Executor
from modulo_relatorios import Relatorio

# Inicializando o sistema
cons = Consciencia()
print(cons.saudacao())

# Fazendo varredura
scanner = Varredura("./")
arquivos = scanner.diagnostico()

# Executando ações
executor = Executor()
acao = executor.executar("Organizar pastas internas")

# Gerando relatório
relatorio = Relatorio()
relatorio.adicionar_item(f"Arquivos encontrados: {len(arquivos)}")
relatorio.adicionar_item(acao)
print(relatorio.gerar())

print("[Sistema Vivo] Ciclo concluído.") 