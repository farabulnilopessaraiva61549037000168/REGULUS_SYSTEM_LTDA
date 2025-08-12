# scanner_inteligente.py
import os

pasta_base = r"C:\Users\Bruno Lopes\Documents\OMEGA_BASE"
chaves_busca = [
    "INTERFACE_COMANDO_OMEGA_V1",
    "RECEPTOR_NUCLEO_ANALITICO",
    "PROTOCOLO_SIGMA_ENCERRAMENTO"
]

print("🔎 Iniciando busca inteligente por palavras-chave...\n")
for raiz, _, arquivos in os.walk(pasta_base):
    for arquivo in arquivos:
        if arquivo.endswith(".py"):
            caminho = os.path.join(raiz, arquivo)
            try:
                with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
                    conteudo = f.read()
                    for chave in chaves_busca:
                        if chave in conteudo:
                            print(f"✅ [{chave}] encontrado em → {caminho}")
            except Exception as e:
                print(f"⚠️ Erro ao ler {caminho}: {e}")
