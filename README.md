The aim of this repository is to Connect to S3 and build a statistical model to classify risk exposure of an S3 bucket. 









## Generate dataset 

` rm -dr dataset`
` python3 generate_data.py`


- a folder with 1000 documents takes around 5 MB of space. 
- Configuration is stored in data_generation.yaml




## sample data and generate stats for each Bucket. 



`python3 risk_assessment.py`