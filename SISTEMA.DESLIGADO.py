def desligar_sistema(chave_autenticacao):
    if chave_autenticacao == "SUA_SENHA_MESTRE_AQUI":
        print(">>> ⚠️ SISTEMA DESLIGADO PELO USUÁRIO. TODOS OS PROCESSOS ENCERRADOS. ⚠️")
        exit()
    else:
        print(">>> 🚫 ACESSO NEGADO. CHAVE INVÁLIDA.") 