# Módulo 1

## Conceitos importatnes

- Cabeçalho = 16B com metadados
- Slot = 8B com os dados

O tipo padrão `bytes` em Python é IMUTÁVEL. A função `read()` precisa retornar um `bytearray` em todas as situações para que o objeto se comporte como uma lista modificável na memória RAM.

## Decisões do M1

### Função `read()`

Caso (1) o caminho arquivo que foi passado não exista: retorna um array de 4096 bytes em "branco"

Caso (2) não existe arquivo: retornar um array de 4096 bytes em "branco"

Caso (3) o conteúdo da página é **menor** que o tamanho disponível: se pega o conteúdo do arquivo e une ao restante da página em branco com os bytes restantes
