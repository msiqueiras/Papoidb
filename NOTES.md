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

## Decisão mais importante

Implementar a lógica de exceção para o caso de o cache estar cheio de páginas pinadas . Foi necessário criar uma *flag booleana* (`kicked_out`) para controlar o fluxo. O objetivo era garantir que o loop percorresse toda a lista LRU em busca de uma "vítima". Se o loop terminasse sem que nenhuma página tivesse sido expulsa, a flag permaneceria `False` e a exceção `FullCacheError` seria lançada. Essa abordagem foi escolhida em vez de contar iterações, pois é mais segura caso a página expulsa esteja no meio da lista (quando o loop é interrompido com `break`).

---

# Módulo 3

## Conceitos importantes

- A árvore B+ é uma variação da árvore B, onde todos os nós folhas estão no mesmo nível. Além disso, há ponteiros na profundidade das folhas que permitem que esse nível seja lido de forma sequencial ordenamente crescente.
- As chaves dos nós folhas apontam diretamente para o registro no disco por meio de um ponteiro.
- Os nós internos são como guias para navegação durante inserções e buscas.
- Uma árvore B+ possui ordem `m`, que é a quantidade máxima de filhos que um nó interno não-raiz pode ter.
- Cada nó interno possui no máximo, `m-1` chaves.
- Ao gerar overflow na inserção de chaves, pegamos a chave ao meio para criarmos mais um nó ou inseri-la em outro nó, seja ele no mesmo nível, seja ele no nível acima. Isso se chama *split*.

### Classe Node

É a classe do nó da árvore B+. É nela em que sabemos o cabeçalho geral daquele nó, se ele é nó folha, quantas chaves aquele nó possui, o ponteiro para a próxima chave e as chaves em si. Os offsets definidos no ínicio são parte do cabeçalho da página/nó definindo onde cada informação pode ser encontrada na página.

- Observação 1: O cálculo da chave+ponteiro é feita com base no pulo do cabeçalho:  
  - Chave: ponto de partida (byte 7) + (índice em que está a chave)*8. Esse 8 são os bytes da chave+ponteiro (4 bytes cada).
  - Ponteiro: mesma fórmula com um +4 significa apenas que o ponteiro começa 4 bytes depois de onde está a sua chave.
- Observação 2: Também foram implementados métodos para acessar e modificar os ponteiros dos filhos dos nós internos, permitindo a navegação pela árvore.

### Classe BplusTree

É a classe responsável pelo gerenciamento da árvore. Ela mantém os nós armazenados em um dicionário (`nodes`), controla a raiz e disponibiliza os métodos de busca (`search`) e inserção (`insert`).

Para identificar os nós, foi adicionado o atributo `next_node_id`, que gera identificadores únicos por meio do método `getNewNodeID()`. Assim, cada novo nó criado durante um split pode ser armazenado e posteriormente localizado no dicionário.

## Decisão mais importante

Arquiterualmente, a decisão que mais impactou na construção do módulo foi o encapsulamento da classe Node, já que em algumas implementações da internet, vimos que a estrutura do nó era criada dentro da classe da árvore diretamente, o que não fazia sentido para nós por estarmos manipulando bytes.

Também foi implementado o *split* de nós folhas. Quando uma folha atinge seu limite de chaves, é criado um novo nó folha e as entradas são reunidas em uma estrutura temporária, ordenadas e divididas em duas partes. A folha original mantém a primeira metade, enquanto a nova recebe a segunda. Além disso, os ponteiros entre as folhas são atualizados para preservar a sequência.

Para integrar os dois nós à árvore, foi necessário armazenar também o nó pai durante a navegação da inserção. A primeira chave da nova folha é utilizada como separadora e inserida no pai, acompanhada do ponteiro para o novo filho.

Quando a folha dividida é a própria raiz, é criada uma nova raiz interna, que passa a apontar para as duas folhas. Isso permite que a árvore deixe de ser formada por apenas um nível.

**Limitações da implementação atual:**

- A propagação do split para níveis superiores não foi implementada.
- O split de nós internos não foi implementado. Caso o nó pai esteja cheio, é lançada uma exceção `NotImplementedError`.
- Não foi implementado o controle de altura da árvore.
- A remoção de chaves não foi implementada.
- Casos mais complexos de inserção e reorganização da árvore ainda não são tratados.

Portanto, a implementação atual permite buscas, inserções em folhas com espaço disponível e split de folhas, incluindo a criação de uma nova raiz e a atualização de um pai que ainda possua espaço.