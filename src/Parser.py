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

    def parse_value(self) -> dict:
        current_token = self.tokens[self.position][0]
        if current_token == "NUMBER":
            value = self._expected("NUMBER")
        elif current_token == "STRING":
            value = self._expected("STRING")
        else:
            raise SyntaxError(f"ERA ESPERADO UM NÚMERO OU UM TEXTO, MAS FOI RECEBIDO {current_token}")
        return value

    def parse_insert(self) -> dict:
        keyword_insert = self._expected("KEYWORD", "INSERT")
        keyword_into = self._expected("KEYWORD", "INTO")
        table_identifier = self._expected("IDENTIFIER")
        keyword_values = self._expected("KEYWORD", "VALUES")
        parenteses = self._expected("SYMBOL", "(")

        values = []
        value = self.parse_value()
        values.append(value)

        while self._accepted("SYMBOL", ","):
            value = self.parse_value()
            values.append(value)

        parenteses = self._expected("SYMBOL", ")")

        insert_infos = {"op": "INSERT", "table_name": table_identifier, "values": values}

        return insert_infos

    def parse_select(self) -> dict:
        keyword_select = self._expected("KEYWORD", "SELECT")
        
        columns = []
        current_token = self.tokens[self.position][0]

        if current_token == "SYMBOL":
            allnames = self._expected("SYMBOL", "*")
            columns.append(allnames)
        elif current_token == "IDENTIFIER":
            table_identifier = self._expected("IDENTIFIER")
            columns.append(table_identifier)

            while self._accepted("SYMBOL", ","):
                table_identifier = self._expected("IDENTIFIER")
                columns.append(table_identifier)

        keyword_from = self._expected("KEYWORD", "FROM")
        table_identifier = self._expected("IDENTIFIER")

        where = None
        if self._accepted("KEYWORD", "WHERE"):
            where_column = self._expected("IDENTIFIER")
            self._expected("SYMBOL", "=")
            where_value = self.parse_value()
            where = {"column": where_column, "value": where_value}

        select_info = {"op": "SELECT", "table_name": table_identifier, "columns": columns, "where": where}
        return select_info

    def parse(self):
        current_token = self.tokens[self.position]
        keyword_type_token = current_token[1]
        if keyword_type_token == "CREATE":
            infos = self.parse_create()
        elif keyword_type_token == "INSERT":
            infos = self.parse_insert()
        elif keyword_type_token == "SELECT":
            infos = self.parse_select()
        else:
            raise SyntaxError("COMANDO DIGITADO INVÁLIDO. TENTE: CREATE, INSERT, SELECT")

        self._accepted("SYMBOL", ";")
        if not self._accepted("EOF"):
            raise SyntaxError(f"TOKEN INESPERADO '{current_token[1]}' APÓS O FIM DO COMANDO")

        return infos

        