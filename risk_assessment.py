


"""

it will database name as input, discovery 3 recusrive folders in them 

and will generate aggregated stats for 3 of them 

print and save the stats 

"""
import os, inspect
import subprocess
import random
import numpy as np


CURRENT_DIRECTORY  = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
database_name = 'Trombone'
database_location = os.path.join(CURRENT_DIRECTORY, 'dataset', database_name)
RESULT_DIRECTORY = "results"




def PII_detection_model(bucket_name, database_location):
    """
    bash_command = "grep -ch -P '\d{3}-\d{2}-\d{4}' {source_folder}*  > {output_file}"
    
    """
    # prepare input and output folder
    source_folder= os.path.join(database_location, bucket_name,"")
    output_file = os.path.join(CURRENT_DIRECTORY, RESULT_DIRECTORY, bucket_name +'.txt')
    
    # count model occurence a grep file for now. 
    with open(output_file, 'w') as f:
        subprocess.run( ["grep", "-crhP", "\d{3}-\d{2}-\d{4}", source_folder, ], 
                     stdout=f)



def sample_model(bucket_name, sampling_percentage=10):

	"""
	take n samples from the bucket and calculate resultant statisitcs about it. 


	"""

	output_file = os.path.join(CURRENT_DIRECTORY, RESULT_DIRECTORY, bucket_name +'.txt')


	occurences_sampled = []
	total_lines = 0
	with open(output_file) as f:
		for line in f:
			total_lines = total_lines +1
			if random.random()*100 < sampling_percentage:
				occurences_sampled.append(int(line.strip()))

	mean = round(np.mean(occurences_sampled),2)
	std = round(np.std(occurences_sampled),2)
	count = round(len(occurences_sampled))
	return {"mean": mean, "std":std, "samples_observed":count, 
			"size":total_lines, "sampling_percentage":sampling_percentage}


def aggregate_results(data):


	total_s3_buckets = len(data)

	total_occurences = sum([i["size"] for i in data])

	aggregated_mean  = sum([i["size"]*i["mean"] for i in data]) / total_occurences

	aggregated_variance  = sum([ (i["size"]/total_occurences)**2 * (i["size"] - i["samples_observed"]) / i["size"] * i["std"]**2 / i["samples_observed"] for 
	                         i in data] )

	aggregated_variance = aggregated_variance**0.5

	sampling = sum([i["size"]*i["sampling_percentage"] for i in data]) / total_occurences

	print(""" total {aggregated_mean} occurrences of SSN detected across
	{total_s3_buckets} S3 buckets,
	 with a {aggregated_variance} of variance 
	 based on sampling {sampling}% of data.
	    """. format(sampling= round(sampling,3), 
	    	aggregated_mean = int(aggregated_mean*total_occurences) , 
	        total_s3_buckets = total_s3_buckets, 
	        aggregated_variance = round(aggregated_variance, 5)
	        ))

def main():

	# generated invidual stats for each document
	buckets = next(os.walk(database_location))[1]
	for bucket in buckets:
		PII_detection_model(bucket, database_location)

	# sample the resultant document and generate aggrgate results
	individual_aggregates = {}
	for bucket in buckets:
		rst = sample_model(bucket)
		individual_aggregates[bucket] = rst

	aggregate_results(individual_aggregates.values())

if __name__ == '__main__':


	main()

