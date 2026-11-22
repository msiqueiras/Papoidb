
class Node:
    OFFSET_IS_LEAF = 0
    OFFSET_NUM_KEYS = 1
    OFFSET_NEXT_LEAF = 3
    OFFSET_KEYS_START = 7

    def __init__(self, data: bytearray):
        self.data = data

    def isLeaf(self) -> bool:
        return self.data[self.OFFSET_IS_LEAF] == 1 #Se for folha TRUE, senão FALSE

    def setIsLeaf(self) -> None:
        self.data[self.OFFSET_IS_LEAF] = 1

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

class BplusTree:
    def __init__(self, root: Node, order: int = 341):
        self.root = root
        self.order = order

    