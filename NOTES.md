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

---

# Módulo 2

## Conceitos importantes

- Hit e Miss: quando a cpu for procurar algo na cache, ele irá verificar se aquela página possui um frame correspondente ou não. Caso encontre o frame na cache, diz-se ser um HIT (acerto). Caso não encontre, ocorre o MISS (falha) e o processador terá que pedir para a memória secundária essa página.
- LRU: last recently use é um algoritmo de gerência de memória qu elemento mais antigo a ser utilizado é descartado
- Pin: quando aquele frame está sendo utilizado, a característica `pin_count` sai de zero para dizer ao processador que ela está sendo usada em algum lugar e que não pode ser retirada da cache naquele momento
- Dirty Bit: quando uma página está na cache, na verdade, quem está é uma cópia dela, isso é, o frame daquela página. Quando se faz alguma alteração nele, ele é dito como sujo (dirty), pois está diferente da página que foi clonada. Para que o frame retorne para a memória secundária, é preciso regravá-lo antes de retirá-lo da cache

## Decisões do M2

### Classe Frame

É uma classe para representar justamente o elemento que é uma cópia exata de uma página dentro da cache, possuindo informações sobre os seus pins e se está ou não limpo

### Classe BufferPool

É a construção mais importante do M2, pois nela há os conceitos de pool, que é a quantidade de páginas/frames suportados na cache, a tabela de páginas que está dentro da cache, a ordenação de quem foi utilizado para uso e o método de busca de uma página dentro da cache

## Decisão mais importante:

Implementar a lógica de exceção para o caso de o cache estar cheio de páginas pinadas . Foi necessário criar uma *flag booleana* (`kicked_out`) para controlar o fluxo. O objetivo era garantir que o loop percorresse toda a lista LRU em busca de uma "vítima". Se o loop terminasse sem que nenhuma página tivesse sido expulsa, a flag permaneceria `False` e a exceção `FullCacheError` seria lançada. Essa abordagem foi escolhida em vez de contar iterações, pois é mais segura caso a página expulsa esteja no meio da lista (quando o loop é interrompido com `break`).