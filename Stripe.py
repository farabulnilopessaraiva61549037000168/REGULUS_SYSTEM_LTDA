# Conecta na API do Stripe ou do PayPal
def gerar_cobranca(cliente, valor):
    print(f"💳 Cobrança gerada para {cliente} no valor de R${valor}")
    # Integração real: stripe.Charge.create(...)

gerar_cobranca('Empresa XYZ', 199.90) 