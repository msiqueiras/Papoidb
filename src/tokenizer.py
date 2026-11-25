RESERVED_KEYWORDS = ["CREATE", "SELECT", "FROM", "INT", "CHAR", "INSERT", "INTO", "VALUES", "WHERE", "AND", "OR"]
CUSTOM_SYMBOLS = ["(", ")", "*", ",", ";", "=", ">", "<"]
TOKENS_TYPES = ["KEYWORD", "NUMBER", "IDENTIFIER", "STRING", "SYMBOL", "EOF"]

class Tokenizer:
    def __init__(self):
        self.keywords = RESERVED_KEYWORDS
        self.symbols = CUSTOM_SYMBOLS
        self.tokens_types = TOKENS_TYPES

    def tokenize(self, sql_text: str) -> list:
        tokens = []

        word = ""
        digits = ""
        index = 0

        while index < len(sql_text):
            character = sql_text[index]

            if character in self.symbols:
                tokens.append(("SYMBOL", character))
                index += 1

            elif character.isalpha() or character == "_":
                while index < len(sql_text) and (sql_text[index].isalnum() or sql_text[index] == "_"):
                    word += sql_text[index]
                    index += 1

                if word.upper() in self.keywords:
                    tokens.append(("KEYWORD", word.upper()))
                else:
                    tokens.append(("IDENTIFIER", word))

                word = ""

            elif character.isnumeric():
                while index < len(sql_text) and sql_text[index].isnumeric():
                    digits += sql_text[index]
                    index += 1

                if index < len(sql_text) and (sql_text[index].isalpha() or sql_text[index] == "_"):
                    while index < len(sql_text) and (sql_text[index].isalnum() or sql_text[index] == "_"):
                        index += 1
                        raise SyntaxError("IDENTIFICADOR INVÁLIDO COMEÇANDO COM NÚMERO.")
                else:
                    tokens.append(("NUMBER", int(digits)))

                digits = ""

            elif character.isspace():
                index += 1

            else:
                index += 1

        tokens.append(("EOF", None))

        return tokens