import os
import streamlit as st

senha = st.text_input("🔑 Insira sua Chave do Absorvedor", type="password")

if senha == os.getenv("CHAVE_ABSORVEDOR"):
    st.success("🔓 Acesso concedido. O sistema foi ativado.")
    # Chamar a função principal do absorvedor
    rodar_absorvedor()
else:
    st.warning("🔒 Aguardando autenticação.")
