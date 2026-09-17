# Módulo 1

## Conceitos importatnes

- Cabeçalho = 16B com metadados
- Slot = 8B com os dados

O tipo padrão `bytes` em Python é IMUTÁVEL. A função `read()` precisa retornar um `bytearray` em todas as situações para que o objeto se comporte como uma lista modificável na memória RAM.

## Decisões do M1

### Classe FileManager

#### Função `read_page()`

Caso (1) o caminho arquivo que foi passado não exista: retorna um array de 4096 bytes em "branco".

Caso (2) não existe arquivo: retornar um array de 4096 bytes em "branco".

Caso (3) o conteúdo da página é **menor** que o tamanho disponível: se pega o conteúdo do arquivo e une ao restante da página em branco com os bytes restantes.

#### Função `write_in_page()`

A função escreve dados na página n. A implementação trava se o tamanho do arquivo não coincidir com o tamanho padrão de 4096 bytes.

### Classe Page

#### Função `insert_record()`

Pula o cabeçalho de 16 B para ir para o primeiro slot vazio disponível para inserção de registros. Para quando o registro ser de um tamanho diferente do que 8 B, a decisão para lidar com essas peculiaridades foi de modo a cair em dois casos:

Caso (1): Registro maior do que 8 B. O registro é truncado até a posição 8 para caber no slot.

Caso (2): Registro menor do que 8 B. O registro concatena os bytes inseridos mais bytes nulos a esquerda.

#### Função `get_record()`

Puxa o registro da memória.

