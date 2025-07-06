# Segunda avaliação da disciplina de Programação Orientadas a Objetos II (INE5404) - UFSC 

# Sistema de Controle Financeiro Residencial

## Objetivo
Desenvolver um sistema de controle financeiro orientado a objetos em Python que permita a uma residência gerenciar suas despesas mensais em categorias específicas e exportar relatórios em formato PDF.

## Requisitos do Sistema

### Cadastro de Despesas
Permitir ao usuário cadastrar despesas em diferentes categorias:
- Educação
- Energia
- Água
- Internet
- Alimentação
- Transporte
- Residência
- Entretenimento

### Visualização de Gastos
- Gerar relatórios mensais com as despesas categorizadas.

### Análise de Dados
- Comparar os gastos mensais com os meses anteriores (opcional).
- Identificar categorias com aumento significativo de gastos.

### Notificações
- Enviar alertas quando os gastos em uma categoria ultrapassarem um limite pré-definido.

### Exportação de Dados
- Exportar o relatório de despesas para um arquivo PDF.

## Estrutura do Sistema

### Classe `Despesa`
**Atributos:**
- `valor`: `float` — O valor da despesa.
- `categoria`: `str` — A categoria da despesa (Educação, Energia, etc.).
- `data`: `str` — A data em que a despesa foi registrada (formato sugerido: "DD/MM/AAAA").
- `descricao`: `str` — Uma descrição breve da despesa.

### Classe `Categoria`
**Atributos:**
- `nome`: `str` — O nome da categoria da despesa (ex: "Educação", "Energia").
- `limite`: `float` (opcional) — Um valor que define um limite para gastos nesta categoria.
- `despesas`: `list` — Uma lista que armazena as despesas associadas a esta categoria.

### Classe `ControleFinanceiro`
**Atributos:**
- `categorias`: `dict` — Um dicionário onde a chave é o nome da categoria e o valor é uma instância da classe `Categoria`.

### Classe `Usuario` (opcional)
**Atributos:**
- `nome`: `str` — O nome do usuário.
- `email`: `str` — O e-mail do usuário (para contato ou notificações).

## Tecnologias Sugeridas
- **Biblioteca para PDF:** `fpdf` (instalável via `pip install fpdf`)

## Resultados Esperados
Um sistema funcional que permite ao usuário gerenciar suas finanças de forma simples e exportar relatórios de despesas em PDF, ajudando a manter o controle financeiro da residência.
