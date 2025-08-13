import os

pasta_base = os.path.join(os.path.expanduser("~"), "Documents", "OMEGA_BASE")

assinaturas = {
    "INTERFACE_COMANDO_OMEGA_V1": "Interface principal de comandos do sistema.",
    "RECEPTOR_NUCLEO_ANALITICO": "Módulo responsável pela recepção de dados e integração com o núcleo de inteligência.",
    "PROTOCOLO_EXECUTOR_SIGMA": "Executa comandos operacionais com base em sinais estratégicos.",
    "MODULO_OBSERVADOR_GHOST": "Observador silencioso de arquivos e eventos.",
    "NUCLEO_MOTOR_DIMENSIONAL": "Gerador de respostas e adaptação dinâmica de comportamento.",
}

print(f"\n📂 Vasculhando a pasta {pasta_base}...\n")

for raiz, _, arquivos in os.walk(pasta_base):
    for arquivo in arquivos:
        if arquivo.endswith(".py"):
            caminho = os.path.join(raiz, arquivo)
            try:
                with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                    conteudo = f.read()
                    for chave, descricao in assinaturas.items():
                        if chave in conteudo:
                            print(f"✅ [{chave}] encontrado em → {caminho}")
                            break
            except Exception as e:
                print(f"⚠️ Erro ao ler {caminho}: {e}")

print("\n✅ Varredura concluída.")
