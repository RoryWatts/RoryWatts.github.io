import glob
import zipfile
import json

json_files = glob.glob('./roam_export/*.zip')

json_most_recent = json_files[-1]

with zipfile.ZipFile(json_most_recent, 'r') as file:
    for i in file.filelist:
        if i.filename == 'curriculum vitae.json':
            with file.open(i) as cv_entry:
                cv = json.load(cv_entry)

print(cv)

class RoamZip:

    def __init__(self):
        self.zip_files = glob.glob('./roam_export/*.zip')
        self.most_recent_zip = self.zip_files[-1]
        self.cv = self.get_curriculum_vitae()

    def get_curriculum_vitae(self):
        with zipfile.ZipFile(self.most_recent_zip, 'r') as file:
            for i in file.filelist:
                if i.filename == 'curriculum vitae.json'
