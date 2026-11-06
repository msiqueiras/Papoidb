from Page import Page
from FileManager import FileManager

class Frame:
    def __init__(self, page_id: int, page: Page):
        self.page = page
        self.page_id = page_id
        self.dirty = False
        self.pin_count = 0


class BufferPool:
    def __init__(self, file_manager: FileManager, pool_size: int):
        self.file_manager = file_manager
        self.pool_size = pool_size
        self.pages = {}
        self.lru_list = []

    def fetch_page(self, page_id: int) -> Page:
        table_contents = self.pages
        lru = self.lru_list
        
        if page_id in table_contents:
            print("HIT: Página encontrada na Cache.")
            p = lru.pop(lru.index(page_id))
            lru.append(p)
            return table_contents[page_id].page 
        
        else:
            print("MISS: Página não encontrada na Cache.")
            fm = self.file_manager
            page = fm.read_page(page_id)
            new_frame = Frame(page_id, page)
            table_contents[page_id] = new_frame
            lru.append(page_id)
            return new_frame.page
