# TP5 - Máquina de Vending

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

Construção de um programa que simule uma máquina de vending.
Os dados da máquina persistem num ficheiro json.

## Requisitos para Utilização

`python3 tp5.py <ficheiro>`: o ficheiro é opcional, se for passado deverá ter conteúdo. Caso o ficheiro passado como argumento não exista, será utilizado o ficheiro `initial.json` como base. Os dados serão sempre guardados no ficheiro `updated.json`.

Comandos:

- `listar`: Mostra todos os produtos disponíveis (código, nome, quantidade e preço)
- `moeda <valor> .`: Adiciona moedas ao saldo, onde `<valor>` é um tipo de moeda (2e, 1e, 50c, 20c, 10c, 5c, 2c, 1c) que pode pode ser separado por espaços e virgulas opcionalmente e termina a inserção de moedas com um ponto final
- `selecionar <código>`: Seleciona um produto para compra, onde `<código>` é o código do produto (letra e 2 números)
- `saldo`: Mostra o saldo atual
- `sair`: Devolve o troco e termina o programa
- `novo <código> "<nome>" <quantidade> <preço>`: Adiciona um novo produto, com código não existente, nome (entre aspas), quantidade e preço
- `reabastece <código> <quantidade>`: Adiciona quantidade ao produto com o código especificado (o produto tem de existir)

## Solução

## Resultados

## Trabalho Futuro

- Resolver bug de adicionar produtos com nome com espaços (split() rebenta o programa)

## Referências

---
