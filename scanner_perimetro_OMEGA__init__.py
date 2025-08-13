import winshell

for item in winshell.recycle_bin():
    print(f"🗂️ {item.original_filename} | De: {item.source_path}")
    item.restore()  # Restaura para a pasta de origem
