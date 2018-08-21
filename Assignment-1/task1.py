import string
import pandas as pd

from collections import Counter

from nltk.corpus import stopwords
from nltk import wordpunct_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

from argparse import ArgumentParser as AP

p = AP()
p.add_argument('--datasrc', type=str, required=True,
                            help='Source for the documents. To be presented in CSV format')
p.add_argument('--remove_stopword', action='store_true',
                                    help='Toggle to remove stop words from the text')
p.add_argument('--stem', action='store_true',
                         help='Toggle to stem the terms collected from the text')
p.add_argument('--lemmatize', action='store_true',
                              help='Toggle to lemmative the terms collected from the text')
p = p.parse_args()

NO_STOPWORD = p.remove_stopword
STEM = p.stem
LEMMATIZE = p.lemmatize

# Use Pandas for storing the text
# Get the textual part of the dataset, and separate out the text and the doc ID
doc_db = pd.read_csv(p.datasrc)
doc_db_text = doc_db['Text'].
doc_db_id = doc_db['TextId']

# Iterate over each document and perform the following
# 1. Case folding: bring all documents to lower case
# 2. Process text
#   2a. Tokenize the documents
#   2b. Remove stopwords (If required)
#   2c. Stemming (If required)
#   2d. Lemmatize (If required)
# 3. Collect all the unique vocabulary from all the documents into a Counter object. This sorts by default

TRANSLATION_TABLE = str.maketrans('', '', string.punctuation)

if NO_STOPWORD:
    ALL_STOPWORDS = set(stopwords.words('english'))  # Set is faster because set uses hashes
if STEM:
    stemmer = PorterStemmer()
if LEMMATIZE:
    lemmatizer = WordNetLemmatizer()

all_counter = Counter()
for doc_id in doc_db_id:
    tmp = doc_db_text[doc_id]
    tmp = tmp.lower()  # Case folding
    tmp = tmp.translate(TRANSLATION_TABLE)  # Removal of punctuation
    tmp = word_tokenize(tmp)  # Tokenization
    
    if NO_STOPWORD:
        tmp = [tmp_w for tmp_w in tmp if tmp_w not in ALL_STOPWORDS]  # Stopword removal
    if STEM:
        tmp = [stemmer.stem(tmp_w) for tmp_w in tmp]  # Stemming
    if LEMMATIZE:
        tmp = [lemmatizer.lemmatize(tmp_w) for tmp_w in tmp]  # Lemmatize

    tmp = [tmp_w for tmp_w in tmp if tmp_w != '']  # Stemming and Lemmatization can cause empty string results
    all_counter += Counter(tmp)

# Print the top 20 elements
print(all_counter.most_common(20))