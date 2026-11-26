class Node:
    OFFSET_IS_LEAF = 0
    OFFSET_NUM_KEYS = 1
    OFFSET_NEXT_LEAF = 3
    OFFSET_KEYS_START = 7

    def __init__(self, data: bytearray):
        self.data = data

    def isLeaf(self) -> bool:
        return self.data[self.OFFSET_IS_LEAF] == 1 #Se for folha TRUE, senão FALSE

    def setIsLeaf(self, is_leaf: bool) -> None:
        self.data[self.OFFSET_IS_LEAF] = 1 if is_leaf else 0

    def getNumKeys(self) -> int:
        return int.from_bytes(self.data[self.OFFSET_NUM_KEYS : self.OFFSET_NUM_KEYS + 2], byteorder='big')

    def setNumKeys(self, qnt: int) -> None:
        self.data[self.OFFSET_NUM_KEYS : self.OFFSET_NUM_KEYS + 2] = qnt.to_bytes(2, byteorder='big')

    def getKey(self, index: int) -> int:
        offset = self.OFFSET_KEYS_START + (index * 8)
        return int.from_bytes(self.data[offset : offset + 4], byteorder='big')

    def setKey(self, index: int, value: int) -> None:
        offset = self.OFFSET_KEYS_START + (index * 8)
        self.data[offset : offset + 4] = value.to_bytes(4, byteorder='big')

    def getPointer(self, index: int) -> int:
        offset = self.OFFSET_KEYS_START + (index * 8) + 4
        return int.from_bytes(self.data[offset : offset + 4], byteorder='big')

    def setPointer(self, index: int, value: int) -> None:
        offset = self.OFFSET_KEYS_START + (index * 8) + 4
        self.data[offset : offset + 4] = value.to_bytes(4, byteorder='big')

    def getChildPointer(self, index: int) -> int:
        if index == 0:
            return int.from_bytes(self.data[self.OFFSET_NEXT_LEAF : self.OFFSET_NEXT_LEAF + 4], byteorder='big')
        offset = self.OFFSET_KEYS_START + (index * 8) - 4
        return int.from_bytes(self.data[offset : offset + 4], byteorder='big')

    def setChildPointer(self, index: int, value: int) -> None:
        if index == 0:
            self.data[self.OFFSET_NEXT_LEAF : self.OFFSET_NEXT_LEAF + 4] = value.to_bytes(4, byteorder='big')
        else:
            offset = self.OFFSET_KEYS_START + (index * 8) - 4
            self.data[offset : offset + 4] = value.to_bytes(4, byteorder='big')


class BplusTree:
    def __init__(self, nodes: dict, order: int = 341):
        self.nodes = nodes
        self.order = order
        self.next_node_id = 0

        page = bytearray(4096)
        self.root = Node(page)
        self.root.setIsLeaf(True)  
        self.root.setNumKeys(0)

        self.nodes[0] = self.root
        self.next_node_id = 1

    def search(self, key: int) -> int | None:
        node = self.root

        while not node.isLeaf():
            i = 0
            while (i < node.getNumKeys()) and (key >= node.getKey(i)):
                i += 1

            child_id = node.getChildPointer(i)
            node = self.nodes[child_id]
        
        for k in range(node.getNumKeys()):
            if key == node.getKey(k):
                return node.getPointer(k)
        
        return None

    def getNewNodeID(self):
        node_id = self.next_node_id
        self.next_node_id += 1
        return node_id

    def insert(self, key: int, ptr: int):
        node = self.root
        node_id = 0
        parent = None # define nó pai, inicialmente None, pois o nó incial é raiz
        parent_id = None

        while not node.isLeaf():
            i = 0
            while (i < node.getNumKeys()) and (key >= node.getKey(i)):
                i += 1

            parent = node # salva o nó pai
            parent_id = node_id

            child_id = node.getChildPointer(i)
            node_id = child_id
            node = self.nodes[child_id]

        old_node_id = node_id

        print(f"Pai: {parent_id}") # apenas para depuraçao
        print(f"Nó encontrado: {old_node_id}")

        for k in range(node.getNumKeys()): #se há duplicatas
            if key == node.getKey(k):
                print(f"Chave {key} já existe na árvore.")
                return
            
        if node.getNumKeys() < (self.order - 1): #se há espaço na folha
            pos = 0
            while (pos < node.getNumKeys()) and (key > node.getKey(pos)):
                pos += 1

            for k in range(node.getNumKeys(), pos, -1):
                node.setKey(k, node.getKey(k-1))
                node.setPointer(k, node.getPointer(k-1))

            node.setKey(pos, key)
            node.setPointer(pos, ptr)
            node.setNumKeys(node.getNumKeys() + 1)
            print(f"Chave {key} inserida com sucesso.")
        else:
            ### raise OverflowError("A CHAVE NÃO FOI INSERIDA. FOLHA ALCANÇOU O LIMITE DE CHAVES.")

            # cria novo no
            page = bytearray(4096)
            new_node = Node(page)

            # configura novo no
            new_node.setIsLeaf(True)
            new_node.setNumKeys(0)
            new_node_id = self.getNewNodeID()
            self.nodes[new_node_id] = new_node

            # faz a folha antiga apontar para a nova, preservando o ponteiro que ela tinha
            old_node_ptr = node.getChildPointer(0)
            node.setChildPointer(0, new_node_id)
            new_node.setChildPointer(0, old_node_ptr)

            # cria estrutura temporaria com o conteudo da folha original + a chave e ponteiro adicionados alem do limite da ordem 
            overflow_node = []
            for i in range(node.getNumKeys()):
                overflow_node.append((node.getKey(i), node.getPointer(i)))
            overflow_node.append((key, ptr))

            # ordena a estrutura pelo valor da chave
            overflow_node.sort(key=lambda item: item[0])

            # divide a estrutura em duas partes
            mid = len(overflow_node) // 2
            left_entries = overflow_node[:mid]
            right_entries = overflow_node[mid:]

            # adiciona as chaves e ponteiros na folha antiga (esquerda)
            for i, (k, p) in enumerate(left_entries):
                node.setKey(i, k)
                node.setPointer(i, p)
            node.setNumKeys(len(left_entries))

            # adiciona as chaves e ponteiros na folhas nova (direita)
            for i, (k, p) in enumerate(right_entries):
                new_node.setKey(i, k)
                new_node.setPointer(i, p)
            new_node.setNumKeys(len(right_entries))

            separator = new_node.getKey(0)

            if parent is None:
                root_page = bytearray(4096)
                new_root = Node(root_page)
                new_root.setIsLeaf(False)
                new_root.setKey(0, separator)
                new_root.setNumKeys(1)
                new_root.setChildPointer(0, old_node_id)
                new_root.setChildPointer(1, new_node_id)

                new_root_id = self.getNewNodeID()
                self.nodes[new_root_id] = new_root
                self.root = new_root
            else:
                # apenas o cenário com pai existente e com espaço
                if parent.getNumKeys() >= (self.order - 1):
                    raise NotImplementedError(
                        "Split de nó interno ainda não implementado."
                    )
                
                pos = 0
                while ((pos < parent.getNumKeys()) and (separator > parent.getKey(pos))):
                    pos += 1

                n = parent.getNumKeys()

                # abre espaço para a nova chave separadora
                for i in range(n - 1, pos - 1, -1):
                    parent.setKey(i + 1, parent.getKey(i))

                # abre espaço para o novo ponteiro de filho
                # O ponteiro em pos continua apontando para a folha antiga
                for i in range(n, pos, -1):
                    parent.setChildPointer(i + 1, parent.getChildPointer(i))

                parent.setKey(pos, separator)
                parent.setChildPointer(pos + 1, new_node_id)
                parent.setNumKeys(n + 1)

            print(f"Chave {key} inserida com sucesso.")
