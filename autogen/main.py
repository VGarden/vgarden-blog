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
    
    def articles(self, category, existing_toc):
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
                    article_name = article
                    article_hyperlink = "/".join(('.', category_folder, article, file_name))
                    for entry in existing_toc:
                        if entry['hyperlink'] == article_hyperlink:
                            if 'name' not in entry:
                                continue
                            article_name = entry['name']
                            break
                    else:
                        article_name = self.__interaction_ask_article_name(
                            article_hyperlink, article_name
                        )
                            
                    articles.append({
                        'hyperlink': article_hyperlink,
                        'name': article_name
                    })
                
        return articles
    
    def __interaction_ask_article_name(self, hyperlink, article):
        print(f"Automaton discovered article @{{{hyperlink}}}.\n\tHow to name it? ({article}) ", end='')
        candidate = input().strip()
        if not candidate:
            print(f"\tEmpty candidate, using {article} instead")
            return article
        else:
            print(f"\tAcknowledge {candidate} for @{hyperlink}")
            return candidate
    
    def navigation_json(self, mode='w'):
        return open(os.path.join(
            self.root_path,
            self.config['FOLDER_STRUCTURE']['SOURCE'],
            self.config['OUTPUTS']['NAVIGATION_JSON']
        ), mode)


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
    
    categories = ('CS', 'MATH')
    
    with helper.navigation_json(mode='r') as f:
        existing_toc = json.load(f)
    existing_toc = [entries for categ in categories for entries in existing_toc[categ]]
    
    navigation_json = {k: helper.articles(k, existing_toc) for k in categories}
    
    with helper.navigation_json(mode='w') as f:
        json.dump(navigation_json, f)
    
    
