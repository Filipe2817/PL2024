# TP6 - Parser Top-Down Recursivo Descendente

## Autor: [Filipe Simões Pereira](https://github.com/Filipe2817), A100552

## Tabela de Conteúdos

- [Objetivos do Trabalho](#objetivos-do-trabalho)
- [Requisitos para Utilização](#requisitos-para-utilização)
- [Solução](#solução)
- [Resultados](#resultados)
- [Trabalho Futuro](#trabalho-futuro)
- [Referências](#referências)

---

## Objetivos do Trabalho

Este trabalho prático tem como objetivo a implementação de um parser top-down recursivo descendente para a seguinte linguagem:

```
? a
b = a * 2 / (27 - 3)
! a + b
c = a * b / (a / b)
```

É uma linguagem simples que permite input (`?`), output (`!`), atribuições (`=`) a variáveis e operações aritméticas (`+`, `-`, `*`, `/`) com prioridade de operadores.

Para a realização deste trabalho, é necessário:

- Definir uma gramática independente do contexto (GIC) LL(1) para a linguagem apresentada
- Garantir que a gramática não é ambígua, calculando os Lookaheads (LA) para todas as produções e garantindo que a gramática respeita a condição LL(1)
- Garantir prioridade de operadores

## Requisitos para Utilização

`python3 tp6.py < input.txt`

## Solução

Para garantir prioridade de operadores é necessário perceber como funciona a prioridade numa gramática LL(1). A prioridade aumenta de acordo com a profundidade da árvore, logo, operadores com maior prioridade têm de aparecer depois de operadores com menor prioridade.

Foi criado um ficheiro de logs para facilitar a visualização das produções reconhecidas pelo parser.
Nas logs, os diversos statements são separados por `|`.

## Resultados

## Trabalho Futuro

- Gerar Árvore de Sintaxe Abstrata (AST)
- Adicionar modo de execução de código
- Handling de erros com mensagens descritivas e localização do erro

## Referências

---
