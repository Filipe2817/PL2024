# TP2

## Autor: [Filipe Simões Pereira](https://github.com/Filipe2817), A100552

## Tabela de Conteúdos

- [Objetivos do Trabalho](#objetivos-do-trabalho)
- [Requisitos para Utilização](#requisitos-para-utilização)
- [Solução](#solução)
- [Resultados](#resultados)
- [Trabalho Futuro](#trabalho-futuro)

---

## Objetivos do Trabalho

## Requisitos para Utilização

## Solução

### Failed Attempts

#### Headers

- ^\s*(#{1,6})\s+(.*)$ does not match empty headers

#### Bold

- ([*|_]{1,2})(.+?)\1
- (\*\*|__)([^*_]+?)\1 does not match * inside
- generic hard

#### Italic

- \*(.+?)\*
- (\*|_)([^*_]+?)\1 matches lists with asterisk bullets, does not match italic in different lines, matches escaped asterisks

#### Full Blockquotes

- ^(>[^\n]*(?:\n>[^\n]+)*)
- ^(>.*(?:\n>.*)*)

#### List

- (?:^|\n)(?:\d+\.|[+*-])[ ]+(?:.*(?:\n[ ]{0,4}\S.*)*)
- (?:\d+\.|[+*-])(?:[ ]+(?:.*(?:\n[ ]*\S.*)*))?
- (?:^|\n)(?:\d+\.|[+*-])(?:[ ]*(?:.*(?:\n[ ]*\S.*)*)*)?
- (?<=^|\n)[ ]*(?:\d+\.|[+*-])[ ]+(?:.*(?:\n[ ]*\S.*)*)*
- (?<=\A|\n{2})[ ]*(?:\d+\.|[+*-])[ ]*(?:.*(?:\n[ ]*\S.*)*)*
- (?<=\A|\n{2})[ ]*(?:\d+\.|[+*-])(?:.*(?:\n[ ]*\S.*)*)*

#### Code

- `(.+?)`

## Resultados

## Trabalho Futuro

- combinações tipo listas dentro de blockquotes
- tornar os regex mais genéricos para cobrir mais casos e até juntar varias funções numa só
- cobrir mais casos do commonmark (novas bullets começam novas listas, por exemplo)

## Referências

- [Markdown to HTML Converter](https://codebeautify.org/markdown-to-html)
- [Markdown Spec](https://spec.commonmark.org/0.28/#list-items)
- [Markdown Basic Syntax](https://www.markdownguide.org/basic-syntax)

---
