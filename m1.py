from pathlib import Path

def le_pagina(n: int = 1):

    caminho_arquivo = Path("arquivo_binario.bin")

    if not caminho_arquivo.exists():    
        return bytearray(4096) #quando o arquivo não existir

    else:
        try:
            with open(caminho_arquivo, "rb") as ab:
                comeco_pagina = n*4096 # 4096 bytes é o tamanho de cada página
                ab.seek(comeco_pagina)
                conteudo_arquivo = ab.read(4096)

                if not conteudo_arquivo:
                    return bytearray(4096)
                
                elif len(conteudo_arquivo) < 4096: #em caso do conteúdo ser menor do que o tamanho da página
                    pagina_completa = bytearray(4096)
                    pagina_completa[: len(conteudo_arquivo)] = conteudo_arquivo
                    return pagina_completa

                return bytearray(conteudo_arquivo)

        except PermissionError:
            print("Permissão para acessar o arquivo negada.")

