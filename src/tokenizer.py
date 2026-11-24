RESERVED_KEYWORDS = ["CREATE", "SELECT", "FROM", "INT", "CHAR", "INSERT", "INTO", "VALUES", "WHERE", "AND", "OR"]
CUSTOM_SYMBOLS = ["(", ")", "*", ","]

class Tokenizer:
    def __init__(self):
        self.keywords = RESERVED_KEYWORDS
        self.symbols = CUSTOM_SYMBOLS

    def tokenize(self, sql_text: str) -> list:
        tokens = []
        
        word = ""         # Acumula letras para formar palavras/nomes
        number_str = ""   # Acumula dígitos para formar números
        in_string = False # Flag para saber se estamos dentro de aspas
        
        for index in range(len(sql_text)):
            character = sql_text[index]
            
            if in_string:
                if character == "'":
                    in_string = False
                    tokens.append(("STRING", word))
                    word = ""
                else:
                    word += character
                continue 

            elif character == "'":
                in_string = True
                word = ""
                
            elif character == " ":
                if word != "":
                    if word.upper() in self.keywords:
                        tokens.append(("KEYWORD", word.upper()))
                    else:
                        tokens.append(("IDENTIFIER", word))
                    word = ""
                if number_str != "":
                    tokens.append(("NUMBER", int(number_str)))
                    number_str = ""

            elif character.isnumeric():
                number_str += character

            
            elif character in CUSTOM_SYMBOLS:
                if word != "":
                    if word.upper() in self.keywords:
                        tokens.append(("KEYWORD", word.upper()))
                    else:
                        tokens.append(("IDENTIFIER", word))
                    word = ""
                if number_str != "":
                    tokens.append(("NUMBER", int(number_str)))
                    number_str = ""
                tokens.append(("SYMBOL", character))

            else:
                word += character

        if word != "":
            if word.upper() in self.keywords:
                tokens.append(("KEYWORD", word.upper()))
            else:
                tokens.append(("IDENTIFIER", word))
        if number_str != "":
            tokens.append(("NUMBER", int(number_str)))

        tokens.append(("EOF", None))
        return tokens