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

        page = bytearray(4096)
        self.root = Node(page)
        self.root.setIsLeaf(True)  
        self.root.setNumKeys(0)

        self.nodes[0] = self.root

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

    def insert(self, key: int, ptr: int):
        node = self.root

        while not node.isLeaf():
            i = 0
            while (i < node.getNumKeys()) and (key >= node.getKey(i)):
                i += 1

            child_id = node.getChildPointer(i)
            node = self.nodes[child_id]

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
            raise OverflowError("A CHAVE NÃO FOI INSERIDA. FOLHA ALCANÇOU O LIMITE DE CHAVES.")