import os
from Page import *


class Volume:
    def __init__(self, vol_id):
        self.vol_id = vol_id
        self.pages = []
        root_dir = "/media/secure_volume/workset/" + vol_id
        for child in os.scandir(root_dir):
            page = Page(vol_id, child.name)
            self.pages.append(page)

        self.page_count = len(self.pages)
        self.poetry_pages = self._find_poetry_pages()

    # Return a list of page numbers in the volume that contain poetry.
    def _find_poetry_pages(self):
        poetry_pages = []
        for page in self.get_pages():
            if page.has_poetry():
                poetry_pages.append(page.number)
        return poetry_pages

    # Return a list of all page objects associated with the volume. 
    def get_pages(self):
        return self.pages

    # Return a list of page numbers in the volume that contain poetry.
    def get_poetry_page_numbers(self):
        return self.poetry_pages

    # Print all identified poems in a volume.
    def print_poems(self):
        for page in self.get_poetry_page_numbers():
            for poem in page.get_poems():
                page.print_lines(poem)


test1 = Volume("wu.89090394669")
test1.print_poems()





