def gerar_relatorio(tipo, dados):
    data_hoje = datetime.now().strftime('%d/%m/%Y')

    if tipo == "licitacao":
        relatorio = f"""
        COMPLEXO DIGITAL - RELATÓRIO TÉCNICO
        Data: {data_hoje}

        Análise de Viabilidade de Licitação
        ------------------------------------------
        Cliente: {dados['nome']}
        Órgão: {dados['orgao']}
       
        Descrição da Demanda:
        {dados['descricao_demanda']}
       
        Parecer Técnico:
        ✓ A demanda apresentada corresponde a uma necessidade compatível com processos licitatórios.
        ✓ É necessário verificar o cabimento orçamentário, compatibilidade legal e diretrizes da legislação vigente (Lei 14.133/2021).

        Recomendações:
        - Avaliar rubricas disponíveis.
        - Analisar os prazos e conformidades do edital.
        - Validar exigências jurídicas e técnicas.

        Gerado automaticamente por IA - Complexo Digital.
        """
    else:
        relatorio = f"""
        Relatório padrão para tipo: {tipo}
        Cliente: {dados['nome']}
        Órgão: {dados['orgao']}
        Descrição: {dados['descricao_demanda']}
        """

    return relatorio 