from pathlib import Path

class FileManager:
    def __init__(self, path_file):

        pf = Path(path_file)
        if not pf.exists():
            pf.touch() #cria um arquivo vazio
        
        self.path_file = path_file


    def read_page(self, n: int=1) -> bytearray: #n é o número da página
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

                elif len(content) < 4096: # se o conteudo do arquivo for menor que 4096Kbytes, o bytes restantes sao preenchidos com 0
                    full_page = bytearray(4096) # cria pagina com bytes zerados
                    full_page[: len(content)] = content # completa a pagina com os bytes lidos

                    return bytearray(full_page)
                 
                else: # quando len(content) == 4096
                     return bytearray(content) 

        except PermissionError:
            print("Permissão para acesso do arquivo negada.")


    def write_in_page(self, n: int, data: bytearray) -> None:
        """
        Escreve um conteúdo binário dentro de uma página.

        Args:
            n (int): o número da página onde se deve inserir o dado
            data (bytearray): o conteúdo a ser escrito na página
        
        Returns:
            None
        """

        if len(data) != 4096:
                            raise ValueError(f"Erro fatal: Tentativa de gravar página com {len(data)} bytes. Tamanho obrigatório é 4096 bytes.")
        
        try:
            with open(self.path_file, "r+b") as bf:
                starting_point = n*4096
                bf.seek(starting_point)
                bf.write(data)
            

        except PermissionError:
            print("Permissão para acesso e modificação do arquivo negada.")