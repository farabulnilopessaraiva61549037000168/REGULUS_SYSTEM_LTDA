# Documentação da Funcionalidade VER NO RELATÓRIO

## Resumo / Summary
Foi adicionado o método `ver()` às classes de Relatório para permitir a visualização formatada dos relatórios gerados.

The `ver()` method has been added to the Report classes to allow formatted viewing of generated reports.

## Mudanças Implementadas / Changes Implemented

### 1. Classe `Relatorio` em `# modulo_relatorios.py`

**Novo Método / New Method:**
```python
def ver(self):
    """Visualiza o conteúdo do relatório."""
    print("[Relatorio] Visualizando relatório:")
    print("=" * 50)
    if self.itens:
        for i, item in enumerate(self.itens, 1):
            print(f"{i}. {item}")
    else:
        print("Nenhum item no relatório.")
    print("=" * 50)
```

**Funcionalidade / Functionality:**
- Exibe o conteúdo do relatório de forma formatada e numerada
- Displays the report content in a formatted and numbered way
- Mostra uma mensagem quando o relatório está vazio
- Shows a message when the report is empty

### 2. Classe `RelatorioXGeradorZ` em `Scanner.Executor.Relatório.Firewall.py`

**Mudanças / Changes:**

1. **Adicionado método `__init__`:**
```python
def __init__(self):
    self.relatorios = []
```

2. **Modificado método `gerar_relatorio`:**
```python
def gerar_relatorio(self, resultado):
    # ... código existente ...
    self.relatorios.append(relatorio_gerado)  # Nova linha / New line
    # ... resto do código ...
```

3. **Novo método `ver()`:**
```python
def ver(self):
    """Visualiza todos os relatórios gerados."""
    print("[Relatorio] Visualizando relatórios:")
    print("=" * 50)
    if self.relatorios:
        for i, relatorio in enumerate(self.relatorios, 1):
            print(f"{i}. {relatorio}")
    else:
        print("Nenhum relatório gerado ainda.")
    print("=" * 50)
```

## Uso / Usage

### Exemplo Básico / Basic Example

```python
# Importar a classe
from modulo_relatorios import Relatorio

# Criar instância
relatorio = Relatorio()

# Adicionar itens
relatorio.adicionar_item("Item 1")
relatorio.adicionar_item("Item 2")

# Visualizar relatório
relatorio.ver()

# Saída / Output:
# [Relatorio] Visualizando relatório:
# ==================================================
# 1. Item 1
# 2. Item 2
# ==================================================
```

### Exemplo com Scanner / Example with Scanner

```python
# No contexto do Scanner system
relatorio = RelatorioXGeradorZ()

# Relatórios são adicionados automaticamente via gerar_relatorio()
# Reports are added automatically via gerar_relatorio()

# Visualizar todos os relatórios gerados
# View all generated reports
relatorio.ver()
```

## Compatibilidade / Compatibility

- ✅ Mantém compatibilidade total com código existente
- ✅ Maintains full compatibility with existing code
- ✅ Método `gerar()` continua funcionando como antes
- ✅ The `gerar()` method continues to work as before
- ✅ Não quebra nenhuma funcionalidade existente
- ✅ Does not break any existing functionality

## Testes / Tests

Todos os testes foram executados com sucesso:
All tests were executed successfully:

1. ✅ Visualização de relatório vazio / Empty report view
2. ✅ Visualização de relatório com itens / Report view with items
3. ✅ Compatibilidade com método `gerar()` / Compatibility with `gerar()` method
4. ✅ Funcionamento em ambas as classes / Functionality in both classes

## Arquivos Modificados / Modified Files

1. `# modulo_relatorios.py` - Adicionado método `ver()`
2. `Scanner.Executor.Relatório.Firewall.py` - Adicionados `__init__()` e `ver()`, modificado `gerar_relatorio()`
3. `.gitignore` - Criado para excluir arquivos de cache Python
