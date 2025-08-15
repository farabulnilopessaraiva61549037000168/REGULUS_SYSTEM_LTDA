import os
import traceback

# Caminho raiz
CAMINHO_RAIZ = r'C:\Users\Bruno Lopes\Documents\OMEGA_BASE'

# Contadores
total_arquivos = 0
total_pastas = 0
arquivos_com_erro = []
arquivos_ok = []

# Função de varredura
def escanear(caminho):
    global total_arquivos, total_pastas
    for raiz, pastas, arquivos in os.walk(caminho):
        total_pastas += 1
        for nome in arquivos:
            total_arquivos += 1
            caminho_completo = os.path.join(raiz, nome)
            try:
                with open(caminho_completo, 'rb') as f:
                    f.read(512)  # Tenta ler os primeiros 512 bytes
                arquivos_ok.append(caminho_completo)
            except Exception as e:
                arquivos_com_erro.append((caminho_completo, str(e)))

# Rodando a função
print("🔍 Escaneando todas as pastas e arquivos dentro de OMEGA_BASE...\n")
escanear(CAMINHO_RAIZ)

# Resultado
print("\n✅ ESCANEAMENTO FINALIZADO")
print(f"Pastas analisadas: {total_pastas}")
print(f"Arquivos analisados: {total_arquivos}")
print(f"Arquivos OK: {len(arquivos_ok)}")
print(f"Arquivos com erro: {len(arquivos_com_erro)}")

# Relatório de erros
if arquivos_com_erro:
    print("\n⚠️ Arquivos com erro de leitura:")
    for caminho, erro in arquivos_com_erro:
        print(f" - {caminho}\n   └─ Erro: {erro}")
else:
    print("\n🟢 Nenhum erro encontrado durante o escaneamento!")
