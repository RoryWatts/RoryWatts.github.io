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
        return Chunk(cv_object)
    
    def export_raw_cv(self, method='json'):
        time_now = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
        if method == 'json':
            with open('./raw_roam_cv/{}-{}.{}'.format(self.roam_page_name, time_now,method), 'w') as file:
                json.dump(self.cv, file)

class Chunk:
    
    def __init__(self, json_chunk):
        try:
            self.string = self.format_words(json_chunk['title'])
            self.prefix = "#"
        except KeyError:
            pass
        try:
            self.string = self.format_words(json_chunk['string'])
        except KeyError:
            pass
        try:
            self.children = [Chunk(x) for x in json_chunk['children']]
        except KeyError:
            pass

    def format_words(self, text):
        text = re.sub(r'\[*\]*', '', text)
        text = "{} \n".format(text)
        return text

class MarkdownExporter:

    def __init__(self, formatted_cv):
        self.cv = formatted_cv
        self.markdown_document = self.format_for_markdown(self.cv)

    def format_for_markdown(self, cv):
        markdown_document = ""
        counter = 0
        chunk = self.cv
        #Unfinished
        while True:
            try:
                if counter == 0:
                    markdown_document + "# {}\n".format(chunk.string)
                if counter == 1:
                    markdown_document + "## {}\n".format(chunk.string)
                else:
                    markdown_document + "{}- {}\n".format(' ' * 4 * counter, chunk.string)
                chunk = self.cv
            except:
                return markdown_document
        return markdown_document
    def export_as_markdown(self):
        with open('./_pages/curriculum_vitae.md', 'w') as file:
            file.write(self.markdown_document)