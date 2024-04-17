import ply.lex as lex

errors = []

tokens = [
    'LISTAR',
    'MOEDA',
    'DOT',
    'SELECIONAR',
    'SAIR',
    'SALDO',
    'NOVO',
    'REABASTECE'
]

states = (
    ('moedas', 'exclusive'),
    ('produtos', 'exclusive'),
    ('adiciona', 'exclusive')
)

t_ANY_ignore = '\t\n' # not ignoring spaces because they are needed for the error handling
t_moedas_ignore = ',\t\n' # same here

t_LISTAR = r'(?i:listar)'
t_SAIR = r'(?i:sair)'
t_SALDO = r'(?i:saldo)'

####### Coins

def t_begin_moedas(t):
    r'(?i:moeda)'
    t.lexer.begin('moedas')

def t_moedas_MOEDA(t):
    r'2e|1e|50c|20c|10c|5c|2c|1c'

    if t.value[-1] == 'e':
        t.value = int(t.value[:-1])
    else:
        t.value = int(t.value[:-1]) / 100

    return t

def t_moedas_DOT(t):
    r'\.'
    t.lexer.begin('INITIAL')
    return t

####### Products

def t_begin_produtos(t):
    r'(?i:selecionar)'
    t.lexer.begin('produtos')

def t_produtos_SELECIONAR(t):
    r'[a-zA-Z]\d{2}'
    t.lexer.begin('INITIAL')
    return t

####### Add new product

def t_begin_adiciona(t):
    r'(?i:novo|reabastece)'
    t.lexer.begin('adiciona')

def t_adiciona_NOVO(t):
    r'[a-zA-Z]\d{2}\s\"[^\"]+\"\s\d+\s\d+(?:\.\d+)?' # cod "name" quantity price
    t.lexer.begin('INITIAL')
    return t

def t_adiciona_REABASTECE(t):
    r'[a-zA-Z]\d{2}\s\d+' # cod quantity
    t.lexer.begin('INITIAL')
    return t

####### Error

def t_ANY_space(t):
    r'\s+'
    errors.append(("LEXSEP", t.value[0]))
    # can't skip, because it's not an error (consumed)

def t_ANY_error(t):
    errors.append(("LEXERROR", t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()
