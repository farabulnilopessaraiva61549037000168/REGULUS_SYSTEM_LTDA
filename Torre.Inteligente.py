# 🚀 Núcleo de Dados Digital - Torre Inteligente
# Código aberto para expansão e integração de sistemas globais

from flask import Flask, request, jsonify
import os
import shutil
from datetime import datetime

app = Flask(__name__)

# 🔐 Diretório principal do Núcleo de Dados
BASE_DIR = os.path.expanduser("~/NucleoDeDadosDigital")

# 🌐 Estrutura de diretórios
folders = [
    "Entrada",
    "Processando",
    "Organizado/Documentos",
    "Organizado/Imagens",
    "Organizado/Audios",
    "Organizado/Projetos",
    "Organizado/Licitações",
    "Organizado/Consultoria",
    "Organizado/ForenseDigital",
    "Organizado/Agronegócio",
    "Organizado/Tecnologia",
    "Organizado/Jurídico",
    "Organizado/SaúdePsicologia",
    "Logs"
]

# 🏗️ Função para criar estrutura de pastas
def criar_pastas():
    for folder in folders:
        caminho = os.path.join(BASE_DIR, folder)
        os.makedirs(caminho, exist_ok=True)

# 📥 Upload de arquivos para Entrada
@app.route('/upload', methods=['POST'])
def upload_arquivo():
    if 'arquivo' not in request.files:
        return "Nenhum arquivo encontrado", 400
    arquivo = request.files['arquivo']
    caminho = os.path.join(BASE_DIR, "Entrada", arquivo.filename)
    arquivo.save(caminho)
    log_evento(f"Arquivo {arquivo.filename} recebido em Entrada")
    return f"Arquivo {arquivo.filename} salvo com sucesso", 200

# 🧠 Processamento dos Arquivos
@app.route('/processar', methods=['POST'])
def processar_arquivos():
    entrada_dir = os.path.join(BASE_DIR, "Entrada")
    processado = 0
    for filename in os.listdir(entrada_dir):
        origem = os.path.join(entrada_dir, filename)
        destino = classificar_arquivo(filename)
        shutil.move(origem, destino)
        processado += 1
        log_evento(f"Arquivo {filename} movido para {destino}")
    return jsonify({"arquivos_processados": processado})

# 🗂️ Classificação de arquivos
def classificar_arquivo(nome_arquivo):
    extensao = nome_arquivo.lower().split('.')[-1]
    if extensao in ['pdf', 'doc', 'docx', 'txt']:
        return os.path.join(BASE_DIR, "Organizado", "Documentos", nome_arquivo)
    elif extensao in ['jpg', 'jpeg', 'png', 'svg']:
        return os.path.join(BASE_DIR, "Organizado", "Imagens", nome_arquivo)
    elif extensao in ['mp3', 'wav', 'm4a']:
        return os.path.join(BASE_DIR, "Organizado", "Audios", nome_arquivo)
    elif 'licitacao' in nome_arquivo.lower():
        return os.path.join(BASE_DIR, "Organizado", "Licitações", nome_arquivo)
    elif 'forense' in nome_arquivo.lower():
        return os.path.join(BASE_DIR, "Organizado", "ForenseDigital", nome_arquivo)
    elif 'consultoria' in nome_arquivo.lower():
        return os.path.join(BASE_DIR, "Organizado", "Consultoria", nome_arquivo)
    elif 'psicologia' in nome_arquivo.lower():
        return os.path.join(BASE_DIR, "Organizado", "SaúdePsicologia", nome_arquivo)
    elif 'agronegocio' in nome_arquivo.lower():
        return os.path.join(BASE_DIR, "Organizado", "Agronegócio", nome_arquivo)
    elif 'tecnologia' in nome_arquivo.lower():
        return os.path.join(BASE_DIR, "Organizado", "Tecnologia", nome_arquivo)
    elif 'juridico' in nome_arquivo.lower():
        return os.path.join(BASE_DIR, "Organizado", "Jurídico", nome_arquivo)
    else:
        return os.path.join(BASE_DIR, "Organizado", "Projetos", nome_arquivo)

# 🗒️ Logs dos eventos
def log_evento(mensagem):
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log = f"[{agora}] {mensagem}\n"
    with open(os.path.join(BASE_DIR, "Logs", "log_eventos.txt"), "a") as log_file:
        log_file.write(log)

# 🔎 Status do Sistema
@app.route('/status', methods=['GET'])
def status():
    total_arquivos = {}
    for folder in folders:
        caminho = os.path.join(BASE_DIR, folder)
        total_arquivos[folder] = len(os.listdir(caminho)) if os.path.exists(caminho) else 0
    return jsonify(total_arquivos)

# 🚀 Inicialização
if __name__ == '__main__':
    criar_pastas()
    app.run(host='0.0.0.0', port=5000) 