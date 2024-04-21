import ply.lex as lex

tokens = [
    'INPUT',
    'OUTPUT',
    'ASSIGN',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'VAR',
    'NUMBER',
    'LPAREN',
    'RPAREN'
]

t_INPUT = r'\?'
t_OUTPUT = r'!'
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_VAR(t):
    r'[a-zA-Z_]\w*'
    return t

def t_NUMBER(t):
    r'[+-]?\d+(?:\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

t_ignore = ' \n\t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
