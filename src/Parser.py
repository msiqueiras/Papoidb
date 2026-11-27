class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.position = 0
    
    def _expected(self, token_type: str, token_value: str = None) -> str:
        current_token = self.tokens[self.position]
        
        if current_token[0] != token_type:
            raise SyntaxError(f"PARSER ESPERAVA O TIPO {token_type}, MAS RECEBU {current_token[0]}")

        if token_value is not None and current_token[1] != token_value:
            raise SyntaxError(f"PARSER ESPERAVA O VALOR {token_value}, MAS RECEBU {current_token[1]}")

        self.position += 1

        return current_token[1]

    def _accepted(self, token_type: str, token_value: str = None) -> bool:
        current_token = self.tokens[self.position]
                
        if current_token[0] != token_type:
            return False

        if token_value is not None and current_token[1] != token_value:
            return False 
        
        self.position += 1

        return True

    def parse_column(self) -> dict:

        column_identifier = self._expected("IDENTIFIER")
        column_type = self._expected("KEYWORD")
        if column_type == "INT":
            length = 4
            column_infos = {"name": column_identifier, "type": column_type, "length": length}
            return column_infos
        
        elif column_type == "CHAR":
            parenteses = self._expected("SYMBOL", "(")
            length = self._expected("NUMBER")
            parenteses = self._expected("SYMBOL", ")")
            column_infos = {"name": column_identifier, "type": column_type, "length": length}
            return column_infos

        raise SyntaxError(f"{column_type} NÃO É VÁLIDO PARA TABELAS. TENTE OS TIPOS INT OU CHAR.")

    def parse_create(self) -> dict:
        keyword_create = self._expected("KEYWORD", "CREATE")
        keyword_table = self._expected("KEYWORD", "TABLE")
        table_identifier = self._expected("IDENTIFIER")
        parenteses = self._expected("SYMBOL", "(")

        columns = []
        column = self.parse_column()
        columns.append(column)

        while self._accepted("SYMBOL", ","):
            column = self.parse_column()
            columns.append(column)

        parenteses = self._expected("SYMBOL", ")")

        create_infos = {"op": "CREATE", "table_name": table_identifier, "columns": columns}

        return create_infos
    