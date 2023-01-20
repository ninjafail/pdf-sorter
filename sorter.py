from PyPDF2 import PdfWriter, PdfReader
import re
from song_info import song_info
from pdfgen import canvas

class Sorter:
    def __init__(self, pdfpath: str):
        self.pdfpath = pdfpath

    def readsongs(self):
        input = PdfReader(self.pdfpath)
        page_info = []
        for i, page in enumerate(input.pages):
            page_info.extend(self.extract_song_names(page.extract_text(), i))
        page_info.sort(key=(lambda x: x['num']))

        for i, v in enumerate(page_info):
            if (v['num'] < 72 and v['page'] > 49) or (v['num'] > 71 and v['page'] < 50):
                page_info.pop(i)
        
        for v in page_info: print(f'{v}, ')

    def extract_song_names(self, text: str, page_num):
        text = text.replace('  ', '').replace('\n', '')
        song_tuples = re.findall('(\d+)([a-zA-Z ,()-]+)', text)
        res = []
        for t in song_tuples:
            song = {
                'num': int(t[0]),
                'name': t[1].lstrip().rstrip(),
                'page': page_num,
            }
            res.append(song)
        return res

    def create_bookmarks(self, songs_info: dict):
        input = PdfReader(self.pdfpath)
        output = PdfWriter()
        for i, page in enumerate(input.pages): output.add_page(page)

        for si in songs_info:
            output.add_outline_item(f"{si['num']}. {si['name']}", si['page'])
        
        with open('test.pdf', 'wb') as res:
            output.write(res)

    def create_toc(self, songs_info: dict):
        input = PdfReader(self.pdfpath)
        output = PdfWriter()

        write_height = 0


        for i, page in enumerate(input.pages): output.add_page(page)

        for si in songs_info:
            output.add_outline_item(f"{si['num']}. {si['name']}", si['page'])
        
        with open('test.pdf', 'wb') as res:
            output.write(res)

Sorter('sorted_songs.pdf').create_toc(song_info)
