
import random
import yaml

import pathlib
import os, inspect


def get_sample_data():
    source_files = ["frankenstien.txt", "the_great_gatsby.txt",
                    "the_importance_of_being_earnest.txt", "pride_and_prejudice.txt"]
    while True:
        source = random.choice([0,1,2,3])
        source_filename = source_files[source]
        print("fetching data from : " + source_filename)

        with open("source_dataset/" + source_filename) as f:
            data = f.read()
        
        # yield the sample data
        s=0
        size = 800
        while s < len(data):
            yield data[s:s +size]
            s= s+ size
            
        
def get_config():
    with open('data_generation.yaml', 'r') as f:
        source_config = yaml.load(f)
    return source_config


def make_buckets(source_config):
    CURRENT_DIRECTORY  = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    all_folders = [CURRENT_DIRECTORY + "/dataset/" + source_config['s3_server']['name'] + "/" + i['name'] for i in source_config['s3_server']['buckets']]

    for folder in all_folders:
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True) 



def main():

    source_config = get_config()

    make_buckets(source_config)
    



