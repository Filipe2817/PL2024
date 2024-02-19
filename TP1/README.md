# TPC1 - Análise de Datasets de Exames Médicos Desportivos

---

## Autor: [Filipe Simões Pereira](https://github.com/Filipe2817), A100552

## Tabela de Conteúdos

- [Objetivos do Trabalho](#objetivos-do-trabalho)
- [Requisitos para Utilização](#requisitos-para-utilização)
- [Solução](#solução)
- [Resultados](#resultados)
- [Trabalho Futuro](#trabalho-futuro)

---

## Objetivos do Trabalho

Este trabalho tem como propósito analisar um conjunto de dados de exames médicos desportivos em formato CSV e gerar um conjunto de estatísticas sobre os atletas que realizaram os exames, sem recorrer a expressões regulares ou a bibliotecas que abstraiam e automatizem a leitura e o tratamento dos dados.

Para alcançar este objetivo, o programa deve ser capaz de:

1. Ler um dataset e processar os dados;
2. Gerar uma lista ordenada alfabeticamente com as modalidades desportivas existentes;
3. Determinar a percentagem de atletas aptos e inaptos para a prática desportiva;
4. Gerar a distribuição de atletas por escalão etário (escalão = intervalo de 5 anos): ... [30-34], [35-39], ...;

## Requisitos para Utilização

Para utilizar o programa, é necessário ter **Python 3.x** instalado e um ficheiro CSV com dados que respeitem o seguinte formato:

```csv
_id,index,dataEMD,nome/primeiro,nome/último,idade,género,morada,modalidade,clube,email,federado,resultado
```

Exemplo:

```csv
6045087f9ee16ada34f21ae4,100,2023-01-13,Glenn,Best,50,M,Graball,abc,AVCfamalicão,glenn.best@avcfamalicão.ca,true,true
```

O conjunto de dados deve ser fornecido ao programa através do ***standard input***, seja por meio de *piping* (`cat emd.csv | python3 tp1.py`) ou redirecionamento de ficheiros (`python3 tp1.py < emd.csv`).

## Solução

### Leitura e Tratamento dos Dados (1)

Como o objetivo principal do trabalho é gerar as estatísticas sobre os atletas, não foi criada uma classe para representar os atletas indivualmente. Neste caso, as
propriedades e vantagens que as classes trazem ao programador não seriam devidamente aproveitadas, porque apenas serviriam para armazenamento temporário dos dados. Portanto, optou-se por uma abordagem mais simplista e direta, em que os atletas são guardados numa lista e cada atleta é representado por uma lista de strings que correpondem diretamente aos campos do dataset.

Na função `parse_csv` é feita a leitura do dataset, linha a linha, começando por excluir a linha do cabeçalho. Cada linha tem os espaços em branco finais removidos e é então dividida em campos, que são guardados numa lista. Depois de processada a linha, a lista de campos é adicionada à lista de atletas. Para além disso, é mantido um contador que guarda o número de atletas lidos. No final, a função retorna a lista de atletas com os respetivos campos e o número total de atletas processados.

```python
def parse_csv():
    athletes = []
    total = 0
    line = sys.stdin.readline() # skip csv header
    for line in sys.stdin:
        line = line.rstrip()
        athlete = line.split(',')
        athletes.append(athlete)
        total += 1
    return (athletes, total)
```

### Lista Ordenada de Modalidades Desportivas (2)

Tendo já a lista de atletas, é possível gerar a lista ordenada de modalidades existentes. Inicialmente, é criada uma lista com as modalidades de todos os atletas, `[athlete[8] for athlete in athletes]`, que é depois ordenada alfabeticamente de forma *case-insensitive* com recurso à função `sorted(..., key = lambda x: x.lower())`. De seguida, a função `groupby()` do módulo **itertools** é usada para agrupar modalidades consecutivas idênticas em subgrupos, onde cada subgrupo é identificado pela própria modalidade. Por fim, é utilizada uma lista por compreensão para extrair as chaves dos subgrupos, que correspondem às modalidades ordenadas e não repetidas.

```python
modalities = [k for k, _ in itertools.groupby(sorted([athlete[8] for athlete in athletes], key = lambda x: x.lower()))]
```

### Percentagem de Atletas Aptos e Inaptos (3)

Para calcular a percentagem de atletas aptos, a função `percentage_apt_athletes` verifica quantos atletas estão determinados como aptos na lista de atletas. A função retorna a percentagem de atletas aptos em relação ao total de atletas.

```python
def percentage_apt_athletes(athletes, total):
    apt = sum(1 for athlete in athletes if athlete[12] == "true")
    return (apt / total) * 100
```

Depois de obter a percentagem de atletas aptos, a percentagem de atletas inaptos é derivável pelo complemento da percentagem de atletas aptos.

```python
(apt_string, inapt_string) = (f"Apt: {apt_athletes:.2f}%", f"Inapt: {100 - apt_athletes:.2f}%")
```

### Distribuição de Atletas por Escalão Etário (4)

Para gerar a distribuição de atletas por escalão etário, a função `generate_age_group_distribution` determina os grupos etários existentes com base no intervalo de idades fornecido e cria um dicionário, inserindo os grupos como chaves e associando uma lista com duas estatísticas: o número de atletas e a sua percentagem em relação ao total. De seguida, itera sobre a lista de atletas e faz a contagem de atletas em cada grupo etário. Por fim, calcula a percentagem de atletas em cada grupo e retorna o dicionário com as estatísticas de distribuição.

```python
def generate_age_group_distribution(athletes, age_range, total):
    (min_age, max_age) = age_range
    age_groups = {}
    start = min_age - (min_age % 5)

    for age in range(start, max_age + 1, 5):
        age_groups[(age, age + 4)] = [0, 0]

    for athlete in athletes:
        age = int(athlete[5])
        group = (age - (age % 5), age - (age % 5) + 4)
        age_groups[group][0] += 1

    for group in age_groups:
        age_groups[group][1] = (age_groups[group][0] / total) * 100

    return age_groups
```

### Funcionalidades Adicionais

O programa apresenta os resultados de forma tabular, para tornar o *output* visualmente mais agradável e facilitar a leitura e análise das estatísticas. A tabela gerada é dinâmica, expandindo-se conforme necessário para acomodar todos os dados produzidos pelo programa, garantindo uma formatação correta e consistente para qualquer dataset fornecido.

## Resultados

A execução do programa com o dataset [emd.csv](emd.csv) gera o seguinte *output*:

![Output tpc1](../images/tpc1-output.png)

> Nota: Qualquer dataset que cumpra os [requisitos](#requisitos-para-utilização), deverá gerar um *output* semelhante ao apresentado acima.

## Trabalho Futuro

- Adicionar tipos e exceções para melhorar a robustez do código
- Adicionar constantes com os índices dos campos dos atletas utilizados, para melhorar a legibilidade do código
- Aplicar um algoritmo de arredondamento para diminuir a perda de precisão nos cálculos de percentagens
- Otimizar o cálculo da distribuição (provavelmente aplicar *incremental averaging* modificada para reduzir cálculos e acessos às estruturas de dados ou repensar a lógica de cálculo no geral)
- Melhorar a apresentação do *output* com uma biblioteca de formatação e/ou abstrair toda a lógica de criação da tabela
- Adicionar a funcionalidade de guardar os resultados em ficheiros

---
