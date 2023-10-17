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

    def find_poetry(self):
        poetry_pages = []
        for page in self.pages:
            if page.has_poetry:
                poetry_pages.append(page.number)
        print(poetry_pages)


test1 = Volume("wu.89090394669")
test1.find_poetry()





