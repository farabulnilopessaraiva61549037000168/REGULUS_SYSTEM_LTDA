import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime

# Configurações do e-mail
EMAIL_USER = "seusistema@gmail.com"
EMAIL_PASS = "SENHA_DE_APP"  # Use senha de app do Google
IMAP_SERVER = "imap.gmail.com"
PASTA_DESTINO = "cartas_matriz"

# Garante a pasta
os.makedirs(PASTA_DESTINO, exist_ok=True)

# Conecta e autentica
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_USER, EMAIL_PASS)
mail.select("inbox", readonly=True)

# Pesquisa por mensagens com palavras-chave
STATUS, MENSAGENS = mail.search(None, '(OR SUBJECT "matriz" BODY "omega")')

# Processamento
for num in MENSAGENS[0].split():
    STATUS, dados = mail.fetch(num, "(RFC822)")
    raw_email = dados[0][1]
    msg = email.message_from_bytes(raw_email)

    assunto, encoding = decode_header(msg["Subject"])[0]
    if isinstance(assunto, bytes):
        assunto = assunto.decode(encoding if encoding else "utf-8")

    remetente = msg.get("From")
    data = msg.get("Date")
    corpo = ""

    if msg.is_multipart():
        for parte in msg.walk():
            tipo = parte.get_content_type()
            if tipo == "text/plain":
                corpo += parte.get_payload(decode=True).decode(errors="ignore")
    else:
        corpo = msg.get_payload(decode=True).decode(errors="ignore")

    nome_arquivo = f"{PASTA_DESTINO}/matriz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(f"Assunto: {assunto}\nRemetente: {remetente}\nData: {data}\n\n{corpo}")

mail.logout()
print("🛡️ Relatório de cartas-matriz extraído com sucesso.") 