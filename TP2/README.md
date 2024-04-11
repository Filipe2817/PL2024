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

Criar um conversor de Markdown para HTML, com suporte para os elementos descritos na *"Basic Syntax"* da [Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)

## Requisitos para Utilização

Para utilizar o programa, é necessário ter Python 3.11+ instalado e um ficheiro **"output.html"**.

O conjunto de dados deve ser fornecido ao programa através do ***standard input***. É possível converter um ficheiro de Markdown já existente utilizando piping (`cat {file} | python3 tp2.py`) ou redirecionamento de ficheiros (`python3 tp2.py < {file}`).

## Solução

Optou-se por utilizar expressões regulares para identificar os elementos do Markdown e substituí-los pelos elementos HTML correspondentes.
Para isso, em vez de uma leitura linha a linha, o programa lê o input na sua totalidade e as expressões regulares identificam todos os elementos presentes no texto.

É importante referir que a ordem das expressões regulares é importante, pois a ordem em que os elementos são substituídos pode afetar o resultado final.

```python
conversion_functions = [
    convert_header,
    convert_bold,
    convert_italic,
    convert_strikethrough,
    convert_ambiguous_symbols,
    convert_blockquote,
    convert_list,
    convert_image,
    convert_link,
    convert_line_break,
    convert_horizontal_rule,
    convert_fenced_code_block,
    convert_code,
    convert_paragraph,
    clear_empty_lines
]
```

As funções de conversão apresentadas acima são chamadas sequencialmente na ordem em que estão dispostas e serão abordadas com mais detalhe em seguida.

### Headers

```python
def convert_header(text):
    pattern = re.compile(r'^[ ]{0,3}(#{1,6})(?:[ ]+(.*)|\n)$', re.MULTILINE)

    def replace(match):
        level = len(match.group(1))
        content = match.group(2) if match.group(2) else ""
        return f"<h{level}>{content}</h{level}>"
    
    return re.sub(pattern, replace, text)
```

Para identificar headers utiliza-se a expressão regular `^[ ]{0,3}(#{1,6})(?:[ ]+(.*)|\n)$`, com a flag `re.MULTILINE` para que o `^` e `$` correspondam ao início e fim de cada linha, respetivamente.

> - `^[ ]{0,3}`: No início da linha existem 0 a 3 espaços
> - `(#{1,6})`: É capturado o 1º grupo, que contém entre 1 e 6 `#` para identificar o nível do header
> - `(?:[ ]+(.*)|\n)`: Podem existir 1 ou mais espaços seguidos de qualquer caracter 0 ou mais vezes (2º grupo capturado), ou um `\n`
> - `$`: A correspondência termina no fim da linha

A substituição é trivial, basta usar o tamanho do 1º grupo para determinar o nível do header e inserir o conteúdo capturado no 2º grupo, caso exista.

#### Tentativas Falhadas

- `^\s*(#{1,6})\s+(.*)$`: apanha headers que deviam ser blocos de código; não apanha headers sem conteúdo

### Bold

O negrito tem de ser convertido antes do itálico porque usam sintaxes semelhantes e o negrito é mais abrangente.

```python
def convert_bold(text):
    pattern = r'(\*\*|__)([^*_].+?)\1'
    return re.sub(pattern, lambda m: f"<strong>{m.group(2)}</strong>", text)
```

> - `(\*\*|__)`: É capturado o 1º grupo, que contém 2 `*` ou `_` para abrir a tag
> - `([^*_].+?)`: É capturado o 2º grupo, que contém qualquer caracter que não seja `*` ou `_` seguido de qualquer caracter 1 ou mais vezes (lazy)
> - `\1`: O 1º grupo é repetido para fechar a tag

Para a substituição, basta inserir o conteúdo capturado no 2º grupo entre as tags de negrito do HTML.

#### Tentativas Falhadas

- `([*|_]{1,2})(.+?)\1`: apanha tags incorretas (ex: \*\_bold\*\_; \*bold\*); não apanha bold com asteriscos ou underscores no conteúdo; falha em casos de bold com itálico
- `(\*\*|__)([^*_]+?)\1`: não apanha bold com asteriscos ou underscores no conteúdo

### Italic

```python
def convert_italic(text):
    pattern = r'(?<!\\)(\*|_)([^*_\n]+(?:\n[^*_\n]+)*)\1'
    return re.sub(pattern, lambda m: f"<em>{m.group(2)}</em>", text)
```

> - `(?<!\\)`: O caracter anterior não pode ser `\`, para evitar asteriscos ou underscores escapados
> - `(\*|_)`: É capturado o 1º grupo, que contém `*` ou `_` para abrir a tag
> - `([^*_\n]+(?:\n[^*_\n]+)*)`: É capturado o 2º grupo, que contém qualquer caracter que não seja `*`, `_` ou `\n` 1 ou mais vezes, seguido de um `\n` e o padrão anterior 0 ou mais vezes. Isto é usado para capturar itálico mesmo que esteja em linhas diferentes
> - `\1`: O 1º grupo é repetido para fechar a tag

Para a substituição, basta inserir o conteúdo capturado no 2º grupo entre as tags de itálico do HTML.

#### Tentativas Falhadas

- `\*(.+?)\*`: não apanha itálico com underscores; falha em casos de itálico em linhas diferentes; apanha asteriscos escapados
- `(\*|_)([^*_]+?)\1`: apanha listas que usam asteriscos como bullets; apanha asteriscos escapados

### Strikethrough

```python
def convert_strikethrough(text):
    pattern = r'~~([^~].+?)~~'
    return re.sub(pattern, lambda m: f"<del>{m.group(1)}</del>", text)
```

> - `~~`: São capturados 2 `~` para abrir a tag
> - `([^~].+?)`: É capturado o conteúdo, que não pode começar com `~`, seguido de qualquer caracter 1 ou mais vezes (lazy)
> - `~~`: São capturados 2 `~` para fechar a tag

Para a substituição, basta inserir o conteúdo capturado no 1º grupo entre as tags de texto riscado do HTML.

### Ambiguous Symbols

Alguns símbolos têm significados especiais em HTML e é necessário identificar e tratar esses casos de acordo com o contexto em que aparecem.

Nesta função, são tratados alguns símbolos como `<`, `>`, `"`, `'`, `*`, `_` e `~`. Muitas vezes, estes símbolos são escapados e deixam de ter significado especial, mas é necessário converter os escapes para os símbolos originais. Esta função tem de ser chamada após as funções que utilizam estes símbolos nos seus padrões para facilitar a identificação e conversão dos mesmos.

```python
LT = "&lt;"
GT = "&gt;"
QUOTE = "&quot;"
APOSTROPHE = "&#39;"

def convert_ambiguous_symbols(text):
    symbols = [
        (r'\\<', LT),
        (r'\\>', GT),
        (r'"', QUOTE),
        (r'\'', APOSTROPHE),
        (r'\\\*', '*'),
        (r'\\_', '_'),
        (r'\\~', '~'),
        (r'(^[ ]{4,}|(?<!<)(?<!</)\b\w+[ ]*)(>+)', lambda m: m.group(1) + GT * len(m.group(2)), re.MULTILINE),
        (r'(<+)(?!\w+>|/)', lambda m: LT * len(m.group(1)))
    ]
    
    for pattern, replacement, *args in symbols:
        text = re.sub(pattern, replacement, text, flags=functools.reduce(lambda x, y: x | y, args, 0))
    
    return text
```

Casos simples:

> - `\\<`: Apanha `<` escapado
> - `\\>`: Apanha `>` escapado
> - `"`: Apanha aspas
> - `\'`: Apanha apóstrofo
> - `\\\*`: Apanha asterisco escapado
> - `\\_`: Apanha underscore escapado
> - `\\~`: Apanha til escapado

A sustituição é direta, basta substituir o símbolo escapado pelo símbolo original.

Casos mais complexos (`>` e `<` usados textualmente):

> - `(^[ ]{4,}|(?<!<)(?<!</)\b\w+[ ]*)`: É capturado o 1º grupo, que pode conter 4 ou mais espaços (caso de blocos de código) no iníco da linha ou não pode conter `<` ou `</` antes de uma palavra completa seguida de 0 ou mais espaços (caso de tags HTML)
> - `(>+)`: É capturado o 2º grupo, que contém 1 ou mais `>`

Esta expressão utiliza a flag `re.MULTILINE` para que o `^` corresponda ao início de cada linha.
Para fazer a substituição, mantém-se o 1º grupo e adiciona-se `>` tantas vezes quantas as capturadas no 2º grupo.

> - `(<+)`: É capturado o 1º grupo, que contém 1 ou mais `<`
> - `(?!\w+>|/)`: O 1º grupo não pode ser seguido por uma palavra seguida de `>`, nem pode ser seguido de `/` (caso de tags HTML)

Para fazer a substituição, adiciona-se `<` tantas vezes quantas as capturadas no 1º grupo.

### Blockquote

```python
def convert_blockquote(text):
    comp_pattern = re.compile(r'^(>.*(?:\n.+)*)', re.MULTILINE)
    return comp_pattern.sub(process_blockquote, text)
```

> - `^(>.*(?:\n.+)*)`: É capturado o 1º grupo, que, no início da linha, contém um `>` seguido de qualquer caracter 0 ou mais vezes; pode ser seguido de um `\n` e qualquer caracter 1 ou mais vezes, 0 ou mais vezes

Esta expressão utiliza a flag `re.MULTILINE` para que o `^` corresponda ao início de cada linha.
Para substituir as correspondências, é chamada a função `process_blockquote` que analisa os níveis de aninhamento de cada correspondência para gerar o HTML corretamente.

#### Tentativas Falhadas

- `^(>[^\n]*(?:\n>[^\n]+)*)`: não apanha blockquotes na sua totalidade se existirem `>` singulares sem conteúdo no meio (`>\n`)
- `^(>.*(?:\n>.*)*)`: não apanha blockquotes na sua totalidade que não tenham o `>` em todas as linhas (ex: `> test\nblockquote`)

### List

As listas têm de ser convertidas depois do itálico porque podem usar asteriscos como *bullets*, que são casos mais específicos que o itálico.

```python
def convert_list(text):
    comp_pattern = re.compile(r'(?:(?<=\A)|(?<=\n{2}))[ ]*(?:\d+\.|[+*-])(?=\s).*(?:\n[ ]*.+)*')
    return comp_pattern.sub(process_list, text)
```

> - `(?:(?<=\A)|(?<=\n{2}))`: A correspondência tem de estar no início do texto ou depois de 2 `\n` (listas precisam de uma linha em branco antes de começarem)
> - `[ ]*(?:\d+\.|[+*-])`: Podem existir 0 ou mais espaços seguidos de um número e um ponto ou um dos caracteres `+`, `*` ou `-` (identificadores de listas)
> - `(?=\s)`: O identificador tem de ser seguido de qualquer caracter que seja um espaço em branco (espaço, `\n`, etc)
> - `.*`: Pode existir qualquer caracter 0 ou mais vezes (existência de conteúdo na lista)
> - `(?:\n[ ]*.+)*`: Pode existir um `\n` seguido de 0 ou mais espaços e qualquer caracter 1 ou mais vezes, 0 ou mais vezes (linhas adicionais da lista)

A substituição é feita chamando a função `process_list` que analisa os níveis de aninhamento, o tipo de lista e o conteúdo de cada correspondência para gerar o HTML corretamente.

#### Tentativas Falhadas

- `(?:^|\n)(?:\d+\.|[+*-])[ ]+(?:.*(?:\n[ ]{0,4}\S.*)*)`: apanha linha vazia antes da lista; não apanha listas sem conteúdo; não apanha listas que comecem identadas
- `(?:\d+\.|[+*-])(?:[ ]+(?:.*(?:\n[ ]*\S.*)*))?`: apanha elementos que não são listas; apanha os identificadores das listas sem conteúdo separadamente

### Image

Imagens têm de ser convertidas antes de links porque usam uma sintaxe muito semelhante e imagens são mais específicas.

```python
def convert_image(text):
    pattern = r'!\[(.*?)\]\((.*?)\)'
    return re.sub(pattern, lambda m: f"<img src=\"{m.group(2)}\" alt=\"{m.group(1)}\">", text)
```

> - `!`: É necessário que exista um `!`
> - `\[(.*?)\]`: É capturado o 1º grupo, que contém qualquer caracter 0 ou mais vezes (lazy) entre parêntesis retos (texto alternativo da imagem)
> - `\((.*?)\)`: É capturado o 2º grupo, que contém qualquer caracter 0 ou mais vezes (lazy) entre parêntesis (URL da imagem)

Para substituir basta criar uma tag de imagem com *src* a receber o conteúdo capturado no 2º grupo e *alt* a receber o conteúdo capturado no 1º grupo.

### Link

```python
def convert_link(text):
    pattern = r'\[(.*?)\]\((.*?)\)'
    return re.sub(pattern, lambda m: f"<a href=\"{m.group(2)}\">{m.group(1)}</a>", text)
```

> - `\[(.*?)\]`: É capturado o 1º grupo, que contém qualquer caracter 0 ou mais vezes (lazy) entre parêntesis retos (texto do link)
> - `\((.*?)\)`: É capturado o 2º grupo, que contém qualquer caracter 0 ou mais vezes (lazy) entre parêntesis (URL do link)

Para substituir basta criar uma tag de *anchor* com *href* a receber o conteúdo capturado no 2º grupo e inserir o conteúdo capturado no 1º grupo entre as tags.

### Line Break

```python
def convert_line_break(text):
    pattern = re.compile(r'([ ]{2,}|\\$)\n', re.MULTILINE)
    return re.sub(pattern, "<br>", text)
```

> - `([ ]{2,}|\\$)`: É capturado o 1º grupo, que contém 2 ou mais espaços, ou uma `\` no fim da linha

Esta expressão utiliza a flag `re.MULTILINE` para que o `$` corresponda ao fim de cada linha do texto.
A substituição é direta, basta substituir a correspondência por uma tag de quebra de linha.

### Horizontal Rule

```python
def convert_horizontal_rule(text):
    pattern = re.compile(r'^\n(-|\*|_)\1{2,}\n$', re.MULTILINE)
    return pattern.sub("<hr>\n", text)
```

> - `^\n`: A linha tem de começar com um `\n`
> - `(-|\*|_)`: É capturado o 1º grupo, que contém `-`, `*` ou `_`
> - `\1{2,}`: O 1º grupo é repetido 2 ou mais vezes
> - `\n$`: A linha tem de terminar com um `\n`

Esta expressão utiliza a flag `re.MULTILINE` para que o `^` e `$` correspondam ao início e fim de cada linha do texto.
A substituição é direta, basta substituir a correspondência por uma tag de regra horizontal.

### Fenced Code Block

Blocos de código têm de ser convertidos antes de código inline porque usam uma sintaxe muito semelhante e são mais específicos.

```python
def convert_fenced_code_block(text):
    pattern = r'`{3}(.+)?\n([\s\S]*?)\n`{3}'

    def replace(match):
        res = f"{match.group(2)}\n</code></pre>"
        if match.group(1) is None:
            res = f"<pre><code>{res}"       
        else:
            res = f"<pre><code class=\"language-{match.group(1)}\">{res}"
        return res

    return re.sub(pattern, replace, text)
```

> - `` `{3} ``: São capturados 3 `` ` `` para abrir o bloco de código
> - `(.+)?\n`: É capturado o 1º grupo, que pode ou não existir e contém qualquer caracter 1 ou mais vezes (linguagem do bloco de código) seguido de um `\n`
> - `([\s\S]*?)\n`: É capturado o 2º grupo, que contém qualquer caracter, incluindo caracteres de espaço em branco, 0 ou mais vezes (lazy) (conteúdo do bloco de código) seguido de um `\n`
> - `` `{3} ``: São capturados 3 `` ` `` para fechar o bloco de código

Para a substituição, basta associar o conteúdo capturado no 1º grupo à classe do bloco de código, caso exista, e inserir o conteúdo capturado no 2º grupo entre as tags de bloco de código.

### Code

```python
def convert_code(text):
    pattern = r'(`{1,2})([\s\S]+?)\1'

    def replace(match):
        pattern2 = r'^[ ](.*)[ ]$'
        formatted_content = re.sub(pattern2, r'\1', match.group(2).replace("\n", " "))
        return f"<code>{formatted_content}</code>"

    return re.sub(pattern, replace, text)
```

> - `` (`{1,2}) ``: É capturado o 1º grupo, que contém 1 ou 2 `` ` `` para abrir a zona de código
> - `([\s\S]+?)`: É capturado o 2º grupo, que contém qualquer caracter, incluindo caracteres de espaço em branco, 1 ou mais vezes (lazy) (conteúdo do bloco de código)
> - `\1`: O 1º grupo é repetido para fechar a zona de código

Para substituir, é necessário formatar a correspondência para remover os `\n` que existem antes e depois do conteúdo do bloco de código. Depois, basta inserir o conteúdo formatado entre as tags de código.

#### Tentativas Falhadas

- `(.+?)`: não apanha zonas de código com várias linhas; apanha zonas de código incorretas se os delimitadores forem 2 `` ` ``; apanha zonas de código incorretas se existirem `` ` `` no conteúdo

### Paragraph

Parágrafos têm de ser convertidos no fim para evitar que afetem outros elementos. Isto torna a conversão mais fácil com uma expressão regular mais simples, porque basta identificar o que ainda não foi convertido e excluir o que já foi.

```python
def convert_paragraph(text):
    allowed_starts = r'[A-Za-z&\-\d*~#]|<(?:(?:u|strong|em|del|code)>|(?:a|img)[ ])'
    pattern = re.compile(rf'^[ ]{{0,3}}(?:{allowed_starts}).*(?:\n(?:{allowed_starts}).*)*', re.MULTILINE)

    # there's no easy way to exclude matches inside code blocks
    code_block_pattern = re.compile(r'<pre><code.*?>[\s\S]*?</code></pre>')
    cb_intervals = [m.span() for m in re.finditer(code_block_pattern, text)]

    def allowed_sub(match):
        result = not any(start <= match.start() <= end and start <= match.end() <= end for start, end in cb_intervals)
        return f"<p>{match.group(0)}</p>" if result else match.group(0)

    return pattern.sub(allowed_sub, text)
```

Expressão regular para identificar elementos que necessitam da conversão de parágrafos:

> `[A-Za-z&\-\d*~#]`: Tem de existir um caracter alfabético, `&`, `-`, dígito, `*`, `~` ou `#`
> `<(?:(?:u|strong|em|del|code)>|(?:a|img)[ ])`: Ou tem de existir uma tag de HTML do tipo `u`, `strong`, `em`, `del` ou `code`, ou tem de existir uma tag de HTML do tipo `a` ou `img`

Expressão regular para identificar parágrafos:

> `^[ ]{0,3}`: No início da linha existem 0 a 3 espaços
> `(?:{allowed_starts})`: Pode existir um dos caracteres permitidos no início do parágrafo
> `.*`: Pode existir qualquer caracter 0 ou mais vezes
> `(?:\n(?:{allowed_starts}).*)*`: Pode existir um `\n` seguido de um dos caracteres permitidos no início do parágrafo e qualquer caracter 0 ou mais vezes, 0 ou mais vezes

Esta expressão utiliza a flag `re.MULTILINE` para que o `^` corresponda ao início de cada linha do texto.
Para substituir, é necessário verificar se a correspondência está dentro de um bloco de código, porque não existe uma maneira simples de excluir correspondências dentro de blocos de código na expressão regular.
Caso a correspondência não esteja dentro de um bloco de código, basta inserir o conteúdo entre as tags de parágrafo.

### Clear Empty Lines

Esta função não é de todo necessária e serve apenas para eliminar linhas vazias.

```python
def clear_empty_lines(text):
    pattern = r'\n{2,}'

    code_block_pattern = re.compile(r'<pre><code.*?>[\s\S]*?</code></pre>')
    cb_intervals = [m.span() for m in re.finditer(code_block_pattern, text)]

    def allowed_sub(match):
        result = not any(start <= match.start() <= end and start <= match.end() <= end for start, end in cb_intervals)
        return f"\n" if result else match.group(0)
    
    return re.sub(pattern, allowed_sub, text)
```

A substituição é direta, basta substituir 2 ou mais `\n` por um único `\n`. No entanto, mais uma vez é necessário excluir zonas de bloco de código para não afetar o seu conteúdo.

## Resultados

Os resultados obtidos com o programa são satisfatórios, mas ainda existem muitas limitações. A conversão de Markdown para HTML é um processo complexo e com muitos detalhes que podem ser difíceis de identificar e tratar.

A execução do programa com o input [input.md](input.md) gera o resultado no ficheiro [output.html](output.html).

![Output tp2](/images/tp2-output.png)

Como é possível observar na imagem acima, foi utilizado o ficheiro [expected-output.html](expected-output.html) para testar e verificar a correção do programa.
Este ficheiro contém o resultado esperado da conversão do input, com a utilização do conversor online [Markdown to HTML](https://codebeautify.org/markdown-to-html).

## Trabalho Futuro

- Suportar toda a sintaxe do Markdown e as possíveis combinações de elementos
- Tornar as expressões regulares mais genéricas para cobrir mais casos e até identificar elementos diferentes com a mesma expressão
- Respeitar todas as convenções do Markdown presentes no [CommonMark](https://spec.commonmark.org/0.31.2/)
- Criar um programa de formatação de HTML para gerar HTML mais legível e organizado

## Referências

- [Markdown to HTML](https://codebeautify.org/markdown-to-html)
- [Markdown Spec](https://spec.commonmark.org/0.31.2/)
- [Markdown Basic Syntax](https://www.markdownguide.org/basic-syntax)

---
