import os
import sys
import configparser
import json

class Helper:
    def __init__(self, root_path):
        self.root_path = root_path
        self.config = configparser.ConfigParser()
        self.config.sections()
        self.config.read(os.path.join(
            self.root_path,
            'autogen/config'
        ))
    
    def articles(self, category):
        extension = self.config['FILE_DEFAULTS']['DEFAULT_EXTENSION']
        source = self.config['FOLDER_STRUCTURE']['SOURCE']
        category_folder = self.config['FOLDER_STRUCTURE'][category]
        folder = os.path.join(
            self.root_path,
            source,
            category_folder
        )
        
        articles = []
        for article in folder_iterator(folder):
            for file_name in file_iterator(os.path.join(folder, article)):
                if file_name.endswith(extension):
                    articles.append({
                        'hyperlink': "/".join(('.', category_folder, article, file_name)),
                        'name': article
                    })
                
        return articles
    
    def navigation_json(self):
        return open(os.path.join(
            self.root_path,
            self.config['FOLDER_STRUCTURE']['SOURCE'],
            self.config['OUTPUTS']['NAVIGATION_JSON']
        ), 'w')


def folder_iterator(folder):
    return (_.name for _ in os.scandir(folder) if _.is_dir())
    
def file_iterator(folder):
    return (_.name for _ in os.scandir(folder) if _.is_file())


if __name__ == '__main__':
    if "VGARDEN_CONFIG" in os.environ:
        config_file = os.environ.get("VGARDEN_CONFIG")
    else:
        config_file = sys.argv[1]
    helper = Helper(config_file)
    
    navigation_json = {k: helper.articles(k) for k in ('CS', 'MATH')}
    
    with helper.navigation_json() as f:
        json.dump(navigation_json, f)
    
    
