from lexer import lexer
import sys

"""
TPC(6): GIC LL(1)

- Parser recursivo descendente
- Prioridade de operadores (aumenta quanto mais fundo na árvore, logo * e / têm de apareces depois de + e -)
- Garantir que a gramática é LL(1)
- Calcular os LA para todas as produções

? a
! a * 2 + 7
b = (a + 3) * 4 - 5
! b * 3
b = a * 2 / (27 - 3)
! a + b
c = a * b / (a / b)
! c

? - input
! - print

===============================================================

G = <T, N, S, P> = <{id, num, ')', '(', '+', '-', '*', '/', '=', '?', '!', '$'}, {S', S, Stmt, Expr, Term, Factor}, S', P=regras>

S' -> S $

S -> Stmt S
   | &

Stmt -> '?' id
      | '!' Expr
      | id '=' Expr

Expr -> Term '+' Expr
      | Term '-' Expr
      | Term

Term -> Factor '*' Term
      | Factor '/' Term
      | Factor

Factor -> '(' Expr ')'
        | id
        | num

Nullable(S) = Nullable(Stmt S) OR Nullable(&) = True
Nullable(Stmt) = Nullable('?' id) OR Nullable('!' Expr) OR Nullable(id '=' Expr) = False
Nullable(Expr) = Nullable(Term '+' Expr) OR Nullable(Term '-' Expr) OR Nullable(Term) = False
Nullable(Term) = Nullable(Factor '*' Term) OR Nullable(Factor '/' Term) OR Nullable(Factor) = False
Nullable(Factor) = Nullable('(' Expr ')') OR Nullable(id) OR Nullable(num) = False

First(S) = First(Stmt S) U First(&) = First(Stmt) U 0 = {'?', '!', id}
First(Stmt) = First('?' id) U First('!' Expr) U First(id '=' Expr) = {'?', '!', id}
First(Expr) = First(Term '+' Expr) U First(Term '-' Expr) U First(Term) = First(Term), Term not nullable = First(Factor), Factor not nullable = {'(', id, num}
First(Term) = First(Factor '*' Term) U First(Factor '/' Term) U First(Factor) = First(Factor), Factor not nullable = {'(', id, num}
First(Factor) = First('(' Expr ')') U First(id) U First(num) = {'(', id, num}

Follow(S) = { $ }
Follow(Stmt) = Follow(S), S nullable + First(S) = { $, '?', '!', id }
Follow(Expr) = Follow(Stmt) + ')' = { $, '?', '!', id, ')' }
Follow(Term) = Follow(Expr) + '+' + '-' = { $, '?', '!', id, ')', '+', '-' }
Follow(Factor) = Follow(Term) + '*' + '/' = { $, '?', '!', id, ')', '+', '-', '*', '/' }

LA(S -> Stmt S) = First(Stmt) = {'?', '!', id}
LA(S -> &) = Follow(S) = { $ }
Intersect = {}

LA(Stmt -> '?' id) = First('?' id) = {'?'}
LA(Stmt -> '!' Expr) = First('!' Expr) = {'!'}
LA(Stmt -> id '=' Expr) = First(id '=' Expr) = {id}
Intersect = {}

LA(Expr -> Term '+' Expr) = First(Term) = {'(', id, num}
LA(Expr -> Term '-' Expr) = First(Term) = {'(', id, num}
LA(Expr -> Term) = First(Term) = {'(', id, num}
Intersect = {'(', id, num}

LA(Term -> Factor '*' Term) = First(Factor) = {'(', id, num}
LA(Term -> Factor '/' Term) = First(Factor) = {'(', id, num}
LA(Term -> Factor) = First(Factor) = {'(', id, num}
Intersect = {'(', id, num}

LA(Factor -> '(' Expr ')') = First('(' Expr ')') = {'('}
LA(Factor -> id) = First(id) = {id}
LA(Factor -> num) = First(num) = {num}
Intersect = {}

Esta gramática não respeita a condição de LL(1) porque existem interseções não nulas nos LA de símbolos não terminais.
===============================================================

G = <T, N, S, P> = <{$, '?', id, '!', '=', '+', '-', '*', '/', '(', ')', num}, {S', S, Stmt, Expr, Expr2, Term, Term2, Factor}, S', P=regras>

S' -> S $

S -> Stmt S
   | &

Stmt -> '?' id
      | '!' Expr
      | id '=' Expr

Expr -> Term Expr2

Expr2 -> '+' Expr
       | '-' Expr
       | &

Term -> Factor Term2

Term2 -> '*' Term
       | '/' Term
       | &

Factor -> '(' Expr ')'
        | id
        | num

Nullable(S) = True
Nullable(Stmt) = False
Nullable(Expr) = False
Nullable(Expr2) = True
Nullable(Term) = False
Nullable(Term2) = True
Nullable(Factor) = False

Não é necessário calcular Lookaheads de S', Expr e Term porque só têm uma produção e não existe interseção de LA's, logo não há ambiguidade.

LA(S -> Stmt S) = First(Stmt), Stmt not nullable = {'?', '!', id}
LA(S -> &) = Follow(S) = { $ }
Intersect = {}

LA(Stmt -> '?' id) = First('?' id) = {'?'}
LA(Stmt -> '!' Expr) = First('!' Expr) = {'!'}
LA(Stmt -> id '=' Expr) = First(id '=' Expr) = {id}
Intersect = {}

LA(Expr2 -> '+' Expr) = First('+' Expr) = {'+'}
LA(Expr2 -> '-' Expr) = First('-' Expr) = {'-'}
LA(Expr2 -> &) = Follow(Expr2) = Follow(Expr) = Follow(Stmt) + ')' = Follow(S), S nullable + First(S) + ')' = { $, '?', '!', id, ')' }
Intersect = {}

LA(Term2 -> '*' Term) = First('*' Term) = {'*'}
LA(Term2 -> '/' Term) = First('/' Term) = {'/'}
LA(Term2 -> &) = Follow(Term2) = Follow(Term) = First(Expr2) + Follow(Expr2), Expr2 nullable = {'+', '-', $, '?', '!', id, ')'}
Intersect = {}

LA(Factor -> '(' Expr ')') = First('(' Expr ')') = {'('}
LA(Factor -> id) = First(id) = {id}
LA(Factor -> num) = First(num) = {num}
Intersect = {}

Esta gramática respeita a condição de LL(1) porque todas as interseções de LA's nos símbolos não terminais são nulas.
"""

YELLOW = "\033[93m"
RESET = "\033[0m"
next_symb = None
file = None

def parser(data):
    global next_symb
    global file
    lexer.input(data)
    next_symb = lexer.token()
    file.write(f"Program: {rec_S()} $\n")

def rec_terminal(type):
    global next_symb
    if next_symb.type == type:
        value = str(next_symb.value)
        next_symb = lexer.token()
        return value
    parse_error(f"Expected {type} but got {next_symb.type}")

def parse_error(e):
    print("Syntax error:", e)
    sys.exit(1)

def rec_S():
    global next_symb
    global file
    string = ""
    if next_symb is None:
        string += "&"
        file.write(f"Recognized: S -> & [{string}]\n")
    else:
        string += rec_Stmt() + " | "
        string += rec_S()
        file.write(f"Recognized: S -> Stmt S [{string}]\n")
    return string

def rec_Stmt():
    global next_symb
    global file
    string = ""
    if next_symb.type == "INPUT":
        string += rec_terminal("INPUT") + " "
        string += rec_terminal("VAR")
        file.write(f"Recognized: Stmt -> ? id [{string}]\n")
    elif next_symb.type == "OUTPUT":
        string += rec_terminal("OUTPUT") + " "
        string += rec_Expr()
        file.write(f"Recognized: Stmt -> ! Expr [{string}]\n")
    elif next_symb.type == "VAR":
        string += rec_terminal("VAR") + " "
        string += rec_terminal("ASSIGN") + " "
        string += rec_Expr()
        file.write(f"Recognized: Stmt -> id = Expr [{string}]\n")
    else:
        parse_error(f"Expected Stmt but got {next_symb.type}")
    return string

def rec_Expr():
    global next_symb
    global file
    string = rec_Term() + " "
    string += rec_Expr2()
    file.write(f"Recognized: Expr -> Term Expr2 [{string}]\n")
    return string

def rec_Expr2():
    global next_symb
    global file
    string = ""
    if next_symb is None or next_symb.type in ["INPUT", "OUTPUT", "VAR", "RPAREN"]: # None to handle EOF (doesn't have type attribute)
        string += "&"
        file.write(f"Recognized: Expr2 -> & [{string}]\n")
    elif next_symb.type == "PLUS":
        string += rec_terminal("PLUS") + " "
        string += rec_Expr()
        file.write(f"Recognized: Expr2 -> + Expr [{string}]\n")
    elif next_symb.type == "MINUS":
        string += rec_terminal("MINUS") + " "
        string += rec_Expr()
        file.write(f"Recognized: Expr2 -> - Expr [{string}]\n")
    else:
        parse_error(f"Expected Expr2 but got {next_symb.type}")
    return string

def rec_Term():
    global next_symb
    global file
    string = rec_Factor() + " "
    string += rec_Term2()
    file.write(f"Recognized: Term -> Factor Term2 [{string}]\n")
    return string

def rec_Term2():
    global next_symb
    global file
    string = ""
    if next_symb is None or next_symb.type in ["PLUS", "MINUS", "INPUT", "OUTPUT", "VAR", "RPAREN"]: # None to handle EOF (doesn't have type attribute)
        string += "&"
        file.write(f"Recognized: Term2 -> & [{string}]\n")
    elif next_symb.type == "MULTIPLY":
        string += rec_terminal("MULTIPLY") + " "
        string += rec_Term()
        file.write(f"Recognized: Term2 -> * Term [{string}]\n")
    elif next_symb.type == "DIVIDE":
        string += rec_terminal("DIVIDE") + " "
        string += rec_Term()
        file.write(f"Recognized: Term2 -> / Term [{string}]\n")
    else:
        parse_error(f"Expected Term2 but got {next_symb.type}")
    return string

def rec_Factor():
    global next_symb
    global file
    string = ""
    if next_symb.type == "LPAREN":
        string += rec_terminal("LPAREN") + " "
        string += rec_Expr() + " "
        string += rec_terminal("RPAREN")
        file.write(f"Recognized: Factor -> ( Expr ) [{string}]\n")
    elif next_symb.type == "VAR":
        string += rec_terminal("VAR")
        file.write(f"Recognized: Factor -> id [{string}]\n")
    elif next_symb.type == "NUMBER":
        string += rec_terminal("NUMBER")
        file.write(f"Recognized: Factor -> num [{string}]\n")
    else:
        parse_error(f"Expected Factor but got {next_symb.type}")
    return string

def main():
    global file
    data = sys.stdin.read()
    file = open("logs.txt", "w")
    print(f"{YELLOW}Generating logs...{RESET}")
    parser(data)
    file.close()
    print(f"{YELLOW}Logs generated successfully!{RESET}")

if __name__ == "__main__":
    main()
