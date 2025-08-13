import deepl

# Substitua por sua chave de API do DeepL (Cadastre-se no site do DeepL para obter uma chave gratuita)
auth_key = "SUA_CHAVE_DE_API"

# Criar um tradutor
translator = deepl.Translator(auth_key)

# Texto para traduzir
texto_original = "Olá, como você está?"

# Traduzir para árabe ('AR')
texto_traduzido = translator.translate_text(texto_original, target_lang="AR")

# Exibir resultado
print(f"Texto original: {texto_original}")
print(f"Texto traduzido: {texto_traduzido.text}")
