# bootloader.py
def verificar_integridade():
    print("[BOOTLOADER] Verificando módulos...")
    from modulo_consciencia import Consciencia
    from modulo_varredura import Varredura
    from modulo_acao import Executor
    from modulo_relatorios import Relatorio
    print("[✓] Todos os módulos OK.")
