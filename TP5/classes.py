import json
from datetime import datetime

BOLD_RED = "\033[1;91m"
BOLD_GREEN = "\033[1;92m"
BOLD_BLUE = "\033[1;94m"
BOLD_YELLOW = "\033[1;93m"
WHITE = "\033[0;97m"

class Product:
    def __init__(self, cod, name, quant, price):
        self.cod = cod
        self.name = name
        self.quant = quant
        self.price = price

    def __str__(self):
        # cod
        spaces = 27 - len(self.cod)
        lspaces = spaces // 2
        rspaces = spaces // 2 if spaces % 2 == 0 else spaces // 2 + 1
        cod_string = f"{' ' * lspaces}{self.cod}{' ' * rspaces}"
        # name
        spaces = 28 - len(self.name)
        lspaces = spaces // 2
        rspaces = spaces // 2 if spaces % 2 == 0 else spaces // 2 + 1
        name_string = f"{' ' * lspaces}{self.name}{' ' * rspaces}"
        # quant
        spaces = 34 - len(str(self.quant))
        lspaces = spaces // 2
        rspaces = spaces // 2 if spaces % 2 == 0 else spaces // 2 + 1
        quant_string = f"{' ' * lspaces}{self.quant}{' ' * rspaces}"
        # price
        spaces = 29 - len(str(self.price))
        lspaces = spaces // 2
        rspaces = spaces // 2 if spaces % 2 == 0 else spaces // 2 + 1
        price_string = f"{' ' * lspaces}{self.price}{' ' * rspaces}"
        # total
        return f"|{cod_string}|{name_string}|{quant_string}|{price_string}|\n+=========================================================================================================================+"
        
"""
+=========================================================================================================================+
|            COD            |            NOME            |            QUANTIDADE            |            PREÇO            |
+=========================================================================================================================+
|27|28|34|29|
"""

class VendingMachine:
    def __init__(self, filename, lexer, errors):
        self.lexer = lexer
        self.lex_err = errors
        self.products = {}
        self.balance = 0
        self.coins = {}
        self.running = True
        self.load_data(filename)
        self.puts(f"{datetime.now().strftime('%Y-%m-%d')}, Stock carregado, Estado atualizado.")
        self.puts("Bom dia. Estou disponível para atender o seu pedido.")
        

    def load_data(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.products = {prod["cod"]: Product(prod["cod"], prod["nome"], prod["quant"], prod["preco"]) for prod in data.get("items", [])}
            self.coins = data.get("coins", {})

    def save_data(self):
        data = {
            "items": [{"cod": product.cod, "nome": product.name, "quant": product.quant, "preco": product.price} for product in self.products.values()],
            "coins": self.coins
        }
        with open("updated.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def __str__(self):
        string = "+=========================================================================================================================+\n"
        string += f"|            {BOLD_RED}COD{WHITE}            |            {BOLD_GREEN}NOME{WHITE}            |            {BOLD_BLUE}QUANTIDADE{WHITE}            |            {BOLD_YELLOW}PREÇO{WHITE}            |\n"
        string += "+=========================================================================================================================+\n"
        for product in self.products.values():
            string += str(product) + "\n"
        return string[:-1]
    
    def puts(self, string):
        print("maq:", string)

    def execute(self, data):
        self.lexer.input(data)

        tokens = [tok for tok in self.lexer] # Need to iterate over the lexer to find errors

        if self.lex_err:
            self.handle_errors()

        for token in tokens:
            type, value = token.type, token.value
            match type:
                case "LISTAR":
                    self.puts("\n" + str(self))
                case "MOEDA":
                    self.balance += value
                    self.coins[self.value_to_coins(value)] += 1
                case "DOT":
                    self.print_balance()
                case "SELECIONAR":
                    self.get_product(value.upper())
                    self.print_balance()
                case "SAIR":
                    self.running = False
                    self.give_change()
                    self.save_data()
                case "SALDO":
                    self.print_balance()
                case "NOVO":
                    cod, name, quant, price = value.split()
                    self.add_product(cod.upper(), name[1:-1], int(quant), float(price))
                case "REABASTECE":
                    cod, quant = value.split()
                    self.restock_product(cod.upper(), int(quant))
                case _:
                    self.puts("Invalid command.")
                    return

    def handle_errors(self): # LEXSEP, LEXERROR        
        err_str = ""
        tok_str = ""

        for type, value in self.lex_err:
            if type == "LEXERROR":
                tok_str += value
            else:
                if tok_str:
                    err_str += f"\nInvalid input: '{tok_str}'"
                    tok_str = ""
        
        if tok_str:
            err_str += f"\nInvalid input: '{tok_str}'"
        
        if err_str:
            self.puts(err_str)

        self.lex_err.clear()

    def value_to_coins(self, value):
        euros = int(value)
        cents = round((value - euros) * 100)
        
        if euros == 0 and cents == 0:
            return "0c"

        coin_parts = []

        if euros > 0:
            coin_parts.append(f"{euros}e")
        if cents > 0:
            coin_parts.append(f"{cents}c")

        return ''.join(coin_parts)
    
    def print_balance(self):
        self.puts(f"Saldo = {self.value_to_coins(self.balance)}")

    def get_product(self, cod):
        product = self.products.get(cod)

        if product is None:
            self.puts("Produto inexistente.")
        elif product.quant <= 0:
            self.puts("Produto esgotado.")
        elif product.price > self.balance:
            self.puts(f"Saldo insuficiente para \"{product.name}\". O produto custa {self.value_to_coins(product.price)}.")
        else:
            self.balance -= product.price
            product.quant -= 1
            self.puts(f"Pode retirar o produto dispensado \"{product.name}\".")

    def balance_to_coins(self):
        res = []
        self.balance = round(self.balance * 100)
        for coin, count in self.coins.items():
            value = int(coin[:-1]) if coin[-1] == 'c' else int(coin[:-1]) * 100
            n_coins = min(int(self.balance // value), count)
            if n_coins > 0:
                self.balance -= n_coins * value
                res.extend([value] * n_coins)
        return list(map(lambda x: x / 100, res))
    
    def give_change(self):
        coins = self.balance_to_coins()
        
        if self.balance > 0:
            self.puts("Não é possível devolver o troco.")
            return

        out_coins = dict.fromkeys([*self.coins], 0)

        for coin in coins:
            coin_str = self.value_to_coins(coin)
            self.coins[coin_str] -= 1
            out_coins[coin_str] += 1
        
        if len(coins) > 0:
            self.puts(f"Pode retirar o troco: {', '.join([f'{n}x {coin}' for coin, n in out_coins.items() if n > 0])}.")
        self.puts("Até à próxima.")

    def add_product(self, cod, name, quant, price):
        product = self.products.get(cod)

        if product is not None:
            self.puts("Produto já existente.")
        else:
            self.products[cod] = Product(cod, name, quant, price)
            self.puts(f"Produto \"{name}\" adicionado com sucesso.")

    def restock_product(self, cod, quant):
        product = self.products.get(cod)

        if product is None:
            self.puts("Produto inexistente.")
        else:
            product.quant += quant
            self.puts(f"Produto \"{product.name}\" reabastecido com sucesso.")
