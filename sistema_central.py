class SistemaCentral:
    def __init__(self):
        self.assinatura_valida = False
        self.espaco_disponivel = False
        self.area_alocada = False

    def detectar(self):
        print("[Sistema] Núcleo detectado.")
        self.validar_assinatura()

    def validar_assinatura(self):
        # Aqui você pode usar uma verificação real com chave digital
        self.assinatura_valida = True
        print("[Sistema] Assinatura digital validada com sucesso.")

    def verificar_espaco(self):
        # Simulação da checagem de espaço disponível
        self.espaco_disponivel = True  # ou False, se quiser testar o outro caminho
        print(f"[Sistema] Espaço disponível: {self.espaco_disponivel}")

    def alocar_area(self):
        if self.espaco_disponivel:
            print("[Sistema] Alocando área otimizada...")
            self.area_alocada = True
            self.executar_configuracao()
        else:
            print("[Sistema] Espaço insuficiente. Otimizando recursos...")
            self.otimizar_recursos()
            print("[Sistema] Criando área virtual temporária...")
            self.area_alocada = True
            self.executar_configuracao()

    def otimizar_recursos(self):
        print("[Sistema] Otimizando memória e processamento...")

    def executar_configuracao(self):
        if self.area_alocada:
            print("[Sistema] Executando configuração autônoma...")

# Execução
omega = SistemaCentral()
omega.detectar()
omega.verificar_espaco()
omega.alocar_area()
