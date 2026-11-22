
class Node:
    OFFSET_IS_LEAF = 0
    OFFSET_NUM_KEYS = 1
    OFFSET_NEXT_LEAF = 3
    OFFSET_KEYS_START = 7

    def __init__(self, data: bytearray,  order: int = 341):
        self.order = order
        self.data = data

    def isLeaf(self) -> bool:
        return self.data[self.OFFSET_IS_LEAF] == 1 # definimos que o nó folha será 1

    def getNumKeys(self) -> int:
        return int.from_bytes(self.data[self.OFFSET_NUM_KEYS : self.OFFSET_NUM_KEYS + 2], byteorder='big')

    def setNumKeys(self, qtd: int):
        self.data[self.OFFSET_NUM_KEYS : self.OFFSET_NUM_KEYS + 2] = qtd.to_bytes(2, byteorder='big')

    def getNextKey(self):
        if not self.is_leaf():
            return -1 # Nó interno não tem próximo
        return int.from_bytes(self.data[self.OFFSET_NEXT_LEAF : self.OFFSET_NEXT_LEAF + 4], byteorder='big')


class BplusTree:
    def __init__(self, order: int = 341):
        pass
    


        