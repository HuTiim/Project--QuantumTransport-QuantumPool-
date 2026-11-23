---
name: maintain-research-documentation
description: Mantém a teoria e os resultados reproduzíveis de projetos de transporte quantico. Use ao criar, alterar ou revisar DOCS/Problem.md, DOCS/Report.md, DOCS/Results.md, cálculos numericos ou notebooks de plotagem.
---

# Documentacao teorica e de resultados

## Objetivo

Mantenha dois documentos na pasta `DOCS/`:

- `DOCS/Report.md`: teoria, premissas, definicoes, equacoes e metodologia.
- `DOCS/Results.md`: resultados, ilustracoes, interpretacao e rastreabilidade dos dados.

Esta skill complementa as regras gerais do repositório. Ela nao substitui o codigo, os testes ou a reproducibilidade dos experimentos.

## Fluxo de trabalho

1. Identifique as equacoes relevantes no `DOCS/Report.md`.
2. Numere as equacoes ou seções de forma estável; nao renomeie referencias existentes sem atualizar todos os usos.
3. Implemente o calculo em um `*.py` separado da plotagem.
4. Faça o script salvar os dados gerados em arquivos `.npz`, incluindo parametros e metadados minimamente necessarios para reproducao.
5. Leia os `.npz` em notebooks Jupyter para gerar e documentar graficos.
6. Atualize `DOCS/Results.md` com a figura, o arquivo gerador, o `.npz` usado e uma leitura objetiva do resultado.
7. Verifique se cada equacao usada no codigo possui referencia no `DOCS/Report.md` e docstring correspondente.

## Convencoes do Report.md

- Escreva o contexto cientifico antes das formulas.
- Defina todas as variaveis e unidades na primeira aparicao.
- Use identificadores estaveis para equacoes, por exemplo `(R1)`, `(R2)` ou referencias numeradas consistentes.
- Separe teoria, aproximacoes e limite de validade.
- Inclua premissas que afetam a interpretacao dos resultados.
- Atualize a metodologia quando parametros, modelos ou convencoes forem alterados.

Modelo recomendado:

```markdown
# Report

## 1. Modelo

Descrição do sistema e das premissas.

## 2. Formalismo

Defina o modelo e as equacoes.

## Equacao R1

$$
...
$$

Descrição das variaveis, unidades e validade.
```

## Convencoes do Results.md

- Relacione cada resultado a uma equacao e a um script de calculo.
- Indique os parametros, o intervalo varrido e o arquivo `.npz` usado.
- Inclua o notebook ou arquivo de plotagem que produziu a ilustracao.
- Descreva o que a figura demonstra sem afirmar causalidade nao suportada pelo modelo.
- Preserve os dados usados em uma execucao e evite substituir resultados sem registrar a mudanca.

Modelo recomendado:

```markdown
# Results

## Resultado R1

- Equacao: [Report.md](./Report.md), equacao R1
- Calculo: `script/calculo.py`
- Dados: `data/resultado.npz`
- Plotagem: `notebooks/resultado.ipynb`

### Ilustracao

![Descrição alternativa](./figures/resultado.png)

### Leitura

Resumo objetivo do resultado e dos parametros relevantes.
```

## Referencias em codigo Python

Adicione referencias a equacoes do `DOCS/Report.md` nas docstrings das funcoes de calculo e plotagem quando o comportamento depender de uma formula.

Exemplo:

```python
def observable(parameter):
    """Calcula o observavel definido pela Eq. R1 do DOCS/Report.md."""
    ...
```

## Nao misture responsabilidades

- Scripts `.py`: calculo numerico, leitura de entradas e escrita de `.npz`.
- Notebooks Jupyter: leitura dos `.npz`, plotagem e apresentacao visual.
- `DOCS/Report.md`: teoria e equacoes.
- `DOCS/Results.md`: resultados e sua interpretacao.

Nao incorpore plotagem em scripts numericos nem realize calculos cientificos principais em notebooks.
