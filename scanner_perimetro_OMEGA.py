import os
import hashlib
from datetime import datetime

def hash_arquivo(caminho):
    try:
        with open(caminho, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None

def formatar_tamanho(tamanho_bytes):
    for unidade in ['B', 'KB', 'MB', 'GB']:
        if tamanho_bytes < 1024:
            return f"{tamanho_bytes:.2f} {unidade}"
        tamanho_bytes /= 1024
    return f"{tamanho_bytes:.2f} TB"

def escanear_pasta(base_path):
    print(f"\n🔎 Iniciando varredura em: {base_path}\n")
    arquivos_info = []
    duplicados = {}
    for raiz, dirs, arquivos in os.walk(base_path):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            try:
                tamanho = os.path.getsize(caminho_completo)
                modificado = os.path.getmtime(caminho_completo)
                hash_arq = hash_arquivo(caminho_completo)
                extensao = os.path.splitext(arquivo)[1].lower()

                info = {
                    "nome": arquivo,
                    "caminho": caminho_completo,
                    "tamanho": formatar_tamanho(tamanho),
                    "modificado": datetime.fromtimestamp(modificado).strftime("%d/%m/%Y %H:%M:%S"),
                    "extensao": extensao,
                    "hash": hash_arq
                }

                if hash_arq:
                    if hash_arq in duplicados:
                        duplicados[hash_arq].append(caminho_completo)
                    else:
                        duplicados[hash_arq] = [caminho_completo]

                arquivos_info.append(info)

                print(f"📄 {arquivo} | {info['tamanho']} | {info['extensao']} | Última modificação: {info['modificado']}")

            except Exception as e:
                print(f"⚠️ Erro ao ler {caminho_completo}: {e}")

    print("\n📦 Total de arquivos encontrados:", len(arquivos_info))
    py_files = [f for f in arquivos_info if f['extensao'] == '.py']
    print(f"🐍 Arquivos Python (.py): {len(py_files)}")

    arquivos_duplicados = [v for v in duplicados.values() if len(v) > 1]
    print(f"📑 Arquivos duplicados por conteúdo: {len(arquivos_duplicados)}")

    if arquivos_duplicados:
        print("\n🔁 Lista de arquivos duplicados:")
        for grupo in arquivos_duplicados:
            print(" - " + "\n   ".join(grupo))
    
    print("\n✅ Varredura finalizada.\n")

# Caminho da pasta principal
caminho_omega_base = r"C:\Users\Bruno Lopes\Documents\OMEGA_BASE"

# Executa a varredura
escanear_pasta(caminho_omega_base)


 

     