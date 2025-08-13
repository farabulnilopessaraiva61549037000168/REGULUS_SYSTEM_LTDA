import imaplib
import email
from email.header import decode_header

# Configurações
username = "SEU_EMAIL"
password = "SUA_SENHA"
imap_server = "imap.gmail.com"  # ou o servidor que usar (Yahoo, Outlook etc.)

# Conectar ao servidor
mail = imaplib.IMAP4_SSL(imap_server)
mail.login(username, password)
mail.select("inbox")

# Buscar mensagens com palavra-chave relevante
status, messages = mail.search(None, 'SUBJECT "chave"')  # Pode ser outra keyword
email_ids = messages[0].split()

for e_id in email_ids[-5:]:  # Últimas 5 mensagens com esse assunto
    status, msg_data = mail.fetch(e_id, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    subject, encoding = decode_header(msg["Subject"])[0]
    print("Assunto:", subject)

    # Se houver anexos ou corpo com código:
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            print("Conteúdo:", part.get_payload(decode=True).decode())

mail.logout() 