def caminho_do_vortice():
    ambiente = ler_ambiente_digital()
    entidade = invocar_entidade_responsiva(ambiente)
    dados = entidade.executar_missao()
    if dados:
        abrir_portal_envio(dados)
        selar_pergaminho() 