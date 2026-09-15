from pathlib import Path

class Pagina:
    def __init__(self, dados=None):
        if not dados:
            self.dados = bytearray(4096)
        else:
            self.dados = dados

def le_pagina(n: int=1):
    pass
