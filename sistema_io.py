import datetime

class SistemaIO:
    def __init__(self):
        self.interface = None
        self.avatar = None
        self.tema = "claro"
        self.acessibilidade = False
        self.sensores = {"voz": False, "toque": False, "teclado": False, "visual": False}
    
    def carregar_interface_visual(self, layout):
        self.interface = layout
        print(f"Interface visual '{layout}' carregada.")
    
    def carregar_avatar_virtual(self, avatar):
        self.avatar = avatar
        print(f"Avatar virtual '{avatar}' carregado.")
    
    def verificar_horario_do_dia(self):
        hora = datetime.datetime.now().hour
        if 18 <= hora or hora < 6:
            self.tema = "escuro"
        else:
            self.tema = "claro"
        print(f"Tema ajustado para: {self.tema}")
    
    def definir_modo_acessibilidade(self, ativado):
        self.acessibilidade = ativado
        status = "ativado" if ativado else "desativado"
        print(f"Modo acessibilidade {status}.")
    
    def sincronizar_sensores(self):
        for sensor in self.sensores:
            self.sensores[sensor] = True
        print("Sensores sincronizados: voz, toque, teclado, visual.")
    
    def exibir_tela_inicial(self):
        print("Exibindo tela inicial...")
        print(f"Tema atual: {self.tema}")
        print(f"Acessibilidade: {'Sim' if self.acessibilidade else 'Não'}")
        print(f"Interface: {self.interface}")
        print(f"Avatar: {self.avatar}")

def iniciar_sistema():
    sistema = SistemaIO()
    sistema.carregar_interface_visual("Figma_layout")
    sistema.carregar_avatar_virtual("IO_Ω")
    sistema.verificar_horario_do_dia()
    sistema.definir_modo_acessibilidade(True)
    sistema.sincronizar_sensores()
    sistema.exibir_tela_inicial()

if __name__ == "__main__":
    iniciar_sistema()
