# ler_arquivo.py
import os

caminho = r"C:\Users\Bruno Lopes\Documents\OMEGA_NOVA"
arquivo = os.path.join(caminho, "script.py")

if os.path.exists(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    print("📄 Conteúdo do script.py:")
    print("-" * 40)
    print(conteudo)
else:
    print("❌ Arquivo script.py não encontrado na pasta.")
