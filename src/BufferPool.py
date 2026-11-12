from src.Page import Page
from src.FileManager import FileManager

class FullCacheError(Exception):
    pass

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
        
        if page_id in table_contents: #HIT
            print("HIT: Página encontrada na Cache.")
            p = lru.pop(lru.index(page_id))
            lru.append(p)
            return table_contents[page_id].page 
        
        else: #MISS
            print("MISS: Página não encontrada na Cache.")
            fm = self.file_manager

            if len(self.pages) >= self.pool_size:
                kicked_out = False
                for pID in lru:
                    dirty_bit = table_contents[pID].dirty
                    if table_contents[pID].pin_count > 0:
                        continue
                    else:
                        if dirty_bit:
                            fm.write_in_page(pID, table_contents[pID].page.data)
                            del table_contents[pID]
                            lru.pop(lru.index(pID))
                            kicked_out = True
                            break
                        
                        del table_contents[pID]
                        lru.pop(lru.index(pID))
                        kicked_out = True
                        break

                if not kicked_out:
                    raise FullCacheError("Cache está cheia de arquivos com PIN ativo.")
                        
            page_data = fm.read_page(page_id)
            page = Page(page_data)
            new_frame = Frame(page_id, page)
            table_contents[page_id] = new_frame
            lru.append(page_id)
            return new_frame.page
