
import random
import yaml
import string
import pathlib
import os, inspect
import numpy as np


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
    """
    create and return the full of each bucket
    """
    CURRENT_DIRECTORY  = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    all_folders = {i['name']:CURRENT_DIRECTORY + "/dataset/" + source_config['s3_server']['name'] + "/" + i['name'] for i in source_config['s3_server']['buckets']}

    print(all_folders)
    for folder in all_folders.values():
        x=pathlib.Path(folder).mkdir(parents=True, exist_ok=True) 
    
    return all_folders

def generate_SSN():
    # format of SSN is 000-00-0000
    p1 = "".join(random.choices(string.digits, k=3 ))
    p2 = "".join(random.choices(string.digits, k=2 ))
    p3 = "".join(random.choices(string.digits, k=4 ))
    return "-".join([p1,p2,p3])

def generate_occurence_count(mean, std):
    """
    generate data which is sampled from a normal distribution with mean mean and
    standard deviation std
    """
    while True:
        yield np.random.normal(mean, std)


def generate_documents(location,  total_files, mean, std):
    """
    generate new documents based on above configuration parameters"""
    
    if location[-1] != '/':
        location = location + '/'
    
    s=get_sample_data()
    occurence_generator = generate_occurence_count(mean,std)
    
    for i in range(total_files):

        with open(location +"document_"+ str(i)+".txt",'w+') as f:
            f.write(next(s))
            f.write('\n')
            occurence = next(occurence_generator)
            o=0
            while o < occurence:
                o = o +1
                f.write(generate_SSN())
                f.write('\n')
                f.write(next(s))
                f.write('\n')

    print("Succesfully created " , total_files, " text files in location ", location )







def main():

    source_config = get_config()

    all_buckets = make_buckets(source_config)

    for bucket in source_config['s3_server']['buckets']:
        mean = bucket['mean']
        std = bucket['std']
        total_files = bucket['total_files']
        name = bucket['name']
        location = all_buckets[name]
        print(mean, std, total_files, name, location)
        generate_documents(location, total_files, mean, std)


    print(".......", "data generation Succesfully ","..............")


if __name__ == '__main__':
    main()



