class Page:
    def __init__(self, data: bytearray):
        self.data = data

    def insert_record(self, slot: int, record: bytes) -> None:
        """
        Insere registro dos dados no slot solicitado. Verifica se o slot está disponível.

        Args:


        """

        offset = 16 + (slot*8) # 16 B para pular o cabeçalho e 8 B para achar o slot

        current_slot = self.data[offset : (offset+8)]

        if current_slot != (b'\x00' * 8): #verifica se os 8 bytes estão todos cheios
            raise MemoryError(f"Erro: Tentativa de inserir dado no slot {slot}. O slot está ocupado. Tente outro.")

        if len(record) > 8:
            fix_record = record[ : 8]

        elif len(record) < 8:
            fix_record = record.ljust(8, b'\x00')

        else:
            fix_record = record           
        
        self.data[offset : (offset+8)] = fix_record # começa no offset e termina no começo do próximo slot

    def get_record(self, slot: int) -> bytes:

        offset = 16 + (slot*8)
        record = bytes(self.data[offset : (offset+8)])

        return record 