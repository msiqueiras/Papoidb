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
