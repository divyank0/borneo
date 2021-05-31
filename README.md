The aim of this repository is to Connect to S3 and build a statistical model to classify risk exposure of an S3 bucket. 


## requirments

- Python3
- Linux




## Create virtual Env

` python3 -m virtualenv virtual_borneo`
` pip3 install -r requirements.txt`


## Generate dataset 

` python3 generate_data.py`



## train a decision tree

we already have curated training data in training_data.csv

` python3 train.py`




- a folder with 1000 documents takes around 5 MB of space. 
- Configuration is stored in data_generation.yaml




## sample data and generate stats for each Bucket. 

`python3 risk_assessment.py  --<classification_model_type>`

classification_model_type = nlp or regex

- aggregated results are printed.
- individual results are stored in result.json in results folder. 
