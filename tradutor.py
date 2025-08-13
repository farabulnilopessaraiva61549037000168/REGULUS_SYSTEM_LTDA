from googletrans import Translator

# Criar um objeto tradutor
translator = Translator()

# Texto para traduzir
texto_original = "Olá, como você está?"

# Traduzir para árabe ('ar')
texto_traduzido = translator.translate(texto_original, dest="ar")

# Exibir resultado
print(f"Texto original: {texto_original}")
print(f"Texto traduzido: {texto_traduzido.text}")
