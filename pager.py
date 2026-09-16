from pathlib import Path

class Pager:
    def __init__(self, path_file):

        pf = Path(path_file)
        if not pf.exists():
            self.path_file = pf.touch() #cria um arquivo vazio
        else:
            self.path_file = path_file


    def read(self, n: int=1) -> bytearray: #n é o número da página
        """
        Lê o conteúdo de uma página de um arquivo binário vindo do disco rígido.
        Args:
            n (int): o número da página que o usuário deseja ler

        Returns:
            bytearray: sequência de bytes mutável que contém o conteúdo que se deseja ler
        
        """
        try:
            with open(self.path_file, "rb") as bf: #bf = binary file
                starting_point = n*4096 # 4096 bytes é o tamanho de cada página, o começo dela é sempre no índice n*4096
                bf.seek(starting_point) #abre o arquivo e pula para o início da página
                content = bf.read(4096)

                if not content: #se o arquivo estiver vazio
                    return bytearray(4096)

                elif len(content) < 4096:
                    full_page = bytearray(4096)
                    full_page[: len(content)] = content

                    return bytearray(full_page) 
                
        except PermissionError:
            print("Permissão para acesso do arquivo negada.")


    def write(self, n: int, data: bytearray) -> None:
        pass