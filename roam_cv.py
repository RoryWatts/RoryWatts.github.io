import glob
import zipfile
import json
import datetime
import re

class RoamZip:

    def __init__(self):
        self.zip_files = glob.glob('./roam_export/*.zip')
        self.most_recent_zip = self.zip_files[-1]
        self.roam_page_name = 'curriculum vitae'
        self.cv_raw = self.get_curriculum_vitae()
        self.cv = self.format_cv(self.cv_raw)

    def get_curriculum_vitae(self):
        with zipfile.ZipFile(self.most_recent_zip, 'r') as file:
            for i in file.filelist:
                if i.filename == '{}.json'.format(self.roam_page_name):
                    with file.open(i) as cv_entry:
                        return json.load(cv_entry)[0]
    
    def format_cv(self, cv_object):
        return Chunk(cv_object, chunk_parent=None)
    
    def export_raw_cv(self, method='json'):
        time_now = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
        if method == 'json':
            with open('./raw_roam_cv/{}-{}.{}'.format(self.roam_page_name, time_now,method), 'w') as file:
                json.dump(self.cv, file)

class Chunk:
    
    def __init__(self, json_chunk, chunk_parent):
        self.parent = chunk_parent
        self.prefix = self.get_prefix()
        self.ignorestring = "private"
        try:
            self.string = self.format_words(json_chunk['title'])
        except KeyError:
            pass
        try:
            self.string = self.format_words(json_chunk['string'])
        except KeyError:
            pass
        if self.string != self.ignorestring:
            try:
                self.children = [Chunk(x, self) for x in json_chunk['children']]
            except KeyError:
                pass
    
    def get_prefix(self):
        if self.parent == None:
            return "#"
        if self.parent.prefix == "#":
            return "\n##"
        if self.parent.prefix == "\n##":
            return "-"
        else:
            return "    " + self.parent.prefix

    def format_words(self, text):
        text = re.sub(r'\[{2}', '', text)
        text = re.sub(r'\]{2}', '', text)
        text = "{} {} \n".format(self.prefix, text)
        return text

class MarkdownExporter:

    def __init__(self, formatted_cv):
        self.cv = formatted_cv
        self.markdown_document = ''
        self.flatten_chunks(self.cv)

    def flatten_chunks(self, chunk):
        self.markdown_document += chunk.string
        for child in chunk.children:
            try:
                self.flatten_chunks(child)
            except AttributeError:
                pass

    def export_as_markdown(self):
        with open('./_pages/curriculum_vitae.md', 'wb') as file:
            file.write(self.markdown_document.encode('utf-8'))