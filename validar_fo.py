def validar_formulario(dados):
    campos_obrigatorios = ["nome", "orgao", "descricao_demanda"]
    faltando = [campo for campo in campos_obrigatorios if campo not in dados or not dados[campo]]

    if faltando:
        return False, f"Faltam os seguintes dados: {', '.join(faltando)}"
    else:
        return True, "Formulário completo." 