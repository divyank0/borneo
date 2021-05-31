


"""

this is preminary file, 
We will need to go through generated file to finalize final training data




"""


from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
nltk.download('punkt')

import re
import pickle



# build features 

def build_features(token):
    """
    build and return features for the token
    
    - Regex match to \d{3}-\d{2}-\d{4}
    - Total length of Token
    - Total digits in token
    - Total Alphabets in token
    - Char_immediately_before_match_is_digit
    - Char_immediately_before_match_is_alphabet
    - Char_immediately_after_match_is_digit

    """

    PATTERN= r'\d{3}-\d{2}-\d{4}'
    
    token_length = len(token)
    numbers = sum(c.isdigit() for c in token)
    letters = sum(c.isalpha() for c in token)
    
    regex_match = re.search(PATTERN, token)
    char_before_match_is_digit = 0
    char_before_match_is_alphabet = 0
    char_after_match_is_digit = 0
    
    if regex_match:
        span = regex_match.span()
        temp = span[0]
        if temp > 0:
            first_char = token[temp-1]
            if first_char.isdigit():
                char_before_match_is_digit = 1
                char_before_match_is_alphabet = 0
            elif first_char.isalpha():
                char_before_match_is_digit = 0
                char_before_match_is_alphabet = 1
            else:
                char_before_match_is_digit = 0
                char_before_match_is_alphabet = 0
        last_char_location = span[1]
        if len(token)> last_char_location:
            last_char  = token[last_char_location]
            char_after_match_is_digit = int(last_char.isdigit())
    
    if regex_match:
        regex_match = 1
    else:
        regex_match = 0
        
    return token_length, numbers, letters, regex_match, char_before_match_is_digit, char_before_match_is_alphabet, char_after_match_is_digit



def predict_token(text, threshold=0.70):
	"""
	return tokens with probability score greater than a threshold.  
	
	we only refer tokens which are certain to belong to some class. 

	"""

	tokens = word_tokenize(text)


	with open("model.pickle", 'rb') as file:
		model_clf  = pickle.load(file)

	x_test = [build_features(i) for i in tokens]


	predictions = model_clf.predict_proba(x_test)
	
	data  =[]
	for i in range(len(predictions)):
		if predictions[i][1]> threshold:
			data.append( (tokens[i],predictions[i][1]) )

	return data


