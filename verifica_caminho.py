import os

# Caminho automático para a pasta Documentos > OMEGA_NOVA
caminho = os.path.join(os.path.expanduser("~"), "Documents", "OMEGA_NOVA")
print("🧭 Caminho detectado:", caminho)

# Verifica se a pasta existe
if os.path.exists(caminho):
    print("✅ A pasta foi localizada com sucesso.")
else:
    print("❌ A pasta NÃO foi encontrada. Verifique o nome.")
