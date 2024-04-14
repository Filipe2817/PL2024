import ply.lex as lex
import sys

# Reserved words
reserved = {
    'select': 'SELECT',
    'from': 'FROM',
    'where': 'WHERE',
    'create': 'CREATE',
    'table': 'TABLE',
    'int': 'INT',
    'primary': 'PRIMARY',
    'key': 'KEY',
    'varchar': 'VARCHAR',
    'not': 'NOT',
    'null': 'NULL',
    'insert': 'INSERT',
    'into': 'INTO',
    'values': 'VALUES',
    'update': 'UPDATE',
    'set': 'SET',
    'delete': 'DELETE',
    'limit': 'LIMIT',
    'decimal': 'DECIMAL',
    'default': 'DEFAULT',
    'constraint': 'CONSTRAINT',
    'foreign': 'FOREIGN',
    'references': 'REFERENCES',
    'join': 'JOIN',
    'on': 'ON',
    'avg': 'AVG',
    'as': 'AS',
    'group': 'GROUP',
    'by': 'BY',
    'max': 'MAX',
    'and': 'AND',
    'order': 'ORDER',
    'desc': 'DESC'
}

# List of token names
tokens = [
    'ID',
    'NUMBER',
    'STRING',
    'OPERATOR',
    'ASTERISK'
] + list(reserved.values())

# List of literals
literals = ['(', ')', ',', ';', '.']

# Regex rules for tokens
t_STRING = r"'[^']*'"
t_OPERATOR = r'[><=]=?'
t_ASTERISK = r'\*'

# Regex rules for tokens with additional logic
def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

def t_NUMBER(t):
    r'[+-]?\d+(?:\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignored characters
t_ignore = ' \t'

# Error handling for unknown characters
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

def main():
    data = sys.stdin.read()

    lexer = lex.lex()
    lexer.input(data)

    for token in lexer:
        print(token)

if __name__ == '__main__':
    main()
