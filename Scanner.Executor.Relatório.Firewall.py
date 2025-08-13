import threading
import time
import queue
import random

# --- Fila central para comunicação entre módulos ---
comunicacao_fila = queue.Queue()

# --- Módulo Scanner (Varredura) ---
class ScannerAlphaBeta:
    def varrer(self):
        while True:
            dados_coletados = f"dado_{random.randint(1000,9999)}"
            print(f"[Scanner] Varredura detectou: {dados_coletados}")
            comunicacao_fila.put(('dados_varredura', dados_coletados))
            time.sleep(3)

# --- Módulo Executor (Ação) ---
class ExecutorPrimeOmega:
    def executar_acao(self, dados):
        print(f"[Executor] Recebendo dados para ação: {dados}")
        # Simula ação
        time.sleep(2)
        resultado_acao = f"ação_executada_com_{dados}"
        print(f"[Executor] Ação concluída: {resultado_acao}")
        comunicacao_fila.put(('resultado_acao', resultado_acao))

    def monitorar(self):
        while True:
            try:
                tipo, dados = comunicacao_fila.get(timeout=1)
                if tipo == 'dados_varredura':
                    self.executar_acao(dados)
                else:
                    comunicacao_fila.put((tipo, dados))  # reenvia para outros módulos
            except queue.Empty:
                pass

# --- Módulo Relatorio (Relatórios) ---
class RelatorioXGeradorZ:
    def gerar_relatorio(self, resultado):
        print(f"[Relatorio] Gerando relatório para: {resultado}")
        # Simula geração de relatório
        time.sleep(1)
        relatorio_gerado = f"relatorio_{resultado}"
        print(f"[Relatorio] Relatório gerado: {relatorio_gerado}")
        comunicacao_fila.put(('relatorio_pronto', relatorio_gerado))

    def monitorar(self):
        while True:
            try:
                tipo, dados = comunicacao_fila.get(timeout=1)
                if tipo == 'resultado_acao':
                    self.gerar_relatorio(dados)
                else:
                    comunicacao_fila.put((tipo, dados))
            except queue.Empty:
                pass

# --- Módulo Firewall (Segurança) ---
class FirewallX:
    def monitorar_sistema(self):
        while True:
            # Simula monitoramento e bloqueio aleatório
            ameaça_detectada = random.choice([False, False, False, True])  # baixa chance
            if ameaça_detectada:
                print("[Firewall] ALERTA: Ameaça detectada! Bloqueando ataque.")
            else:
                print("[Firewall] Sistema seguro.")
            time.sleep(5)

# --- Inicialização e execução ---
def iniciar_sistema():
    scanner = ScannerAlphaBeta()
    executor = ExecutorPrimeOmega()
    relatorio = RelatorioXGeradorZ()
    firewall = FirewallX()

    # Threads para módulos
    t_scanner = threading.Thread(target=scanner.varrer, daemon=True)
    t_executor = threading.Thread(target=executor.monitorar, daemon=True)
    t_relatorio = threading.Thread(target=relatorio.monitorar, daemon=True)
    t_firewall = threading.Thread(target=firewall.monitorar_sistema, daemon=True)

    # Start threads
    t_scanner.start()
    t_executor.start()
    t_relatorio.start()
    t_firewall.start()

    print("[FARABULINI] Sistema iniciado. Pressione Ctrl+C para encerrar.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[FARABULINI] Sistema encerrado pelo usuário.")

if __name__ == "__main__":
    iniciar_sistema()
