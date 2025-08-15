import shutil
import platform

def verificar_ambiente():
    ambiente = {
        "Python": shutil.which("python") is not None,
        "Anaconda": shutil.which("conda") is not None,
        "Jupyter": shutil.which("jupyter") is not None,
        "Sistema": platform.system(),
        "Versão": platform.version()
    }
    for item, status in ambiente.items():
        print(f"🔎 {item}: {'✅ OK' if status else '❌ Não encontrado'}")
    return ambiente
