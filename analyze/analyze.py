"""
    Identify the top 20 relevant keywords that categorizes that transcript.
    (uniqueness of word, frequency and relevance)

    Bonus: Topic modeling

    Upload dataset's before:
    $ python3 dataset.py
"""

from __future__ import print_function
# import nltk
import logging
import json

from nltk.tokenize import sent_tokenize, word_tokenize, WordPunctTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from gensim import models, corpora

File = './files/asrOutput.json'


def read_transcript_from_file():
    """ Load Input data """
    with open(File, 'rb') as fl:
        tscribe_json = json.load(fl)

    return tscribe_json['results']['transcripts'][0]['transcript']


def process(input_text):
    """
    words, and stemming
    :param input_text:
    :return:
    """
    # tokens = word_tokenize(input_text)
    # Create a regular expression tokenizer
    tokenizer = RegexpTokenizer(r'\w+')

    # Tokenize the input string
    tokens = tokenizer.tokenize(input_text.lower())

    # Create a Snowball stemmer
    stemmer = SnowballStemmer('english')

    # Get the list of stop words
    stop_words = stopwords.words('english')

    # Remove the stop words
    tokens = [x for x in tokens if not x in stop_words]

    # Perform stemming on the tokenized words
    tokens_stemmed = [stemmer.stem(x) for x in tokens]

    return tokens_stemmed


def lda_contributing_words(input_text, num_topics=1, num_words=20, passes=100):
    """
    Generate the Latent Dirichlet Allocation (LDA) model

    :param input_text:
    :param num_topics: Define the number of topics for the LDA model
    :param num_words: the top contributing words for each topic
    :param passes: Generate the Latent Dirichlet Allocation (LDA) model
    :return:
    """
    # make sentences
    input_text = input_text.split('.')

    # Create a list for sentence tokens
    tokens = [process(x) for x in input_text]

    # Create a dictionary based on the sentence tokens
    dict_tokens = corpora.Dictionary(tokens)

    # Create a document-term matrix
    doc_term_mat = [dict_tokens.doc2bow(token) for token in tokens]

    # Generate the Latent Dirichlet Allocation (LDA) model
    ldamodel = models.ldamodel.LdaModel(doc_term_mat,
                                        num_topics=num_topics, id2word=dict_tokens, passes=passes)

    print('\nTop ' + str(num_words) + ' contributing words to each topic:')
    for item in ldamodel.print_topics(num_topics=num_topics,
                                      num_words=num_words):
        print('\nTopic', item[0])
        # Print the contributing words along with their relative contributions

        list_of_strings = item[1].split(' + ')
        for text in list_of_strings:
            weight = text.split('*')[0]
            word = text.split('*')[1]
            print(word, '==>', str(round(float(weight) * 100, 2)) + '%')


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)

    input_text = read_transcript_from_file()
    print(input_text)

    # Topic modeling using Latent Dirichlet Allocation
    lda_contributing_words(input_text)
