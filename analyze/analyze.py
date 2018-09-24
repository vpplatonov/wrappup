"""
    Identify the top 20 relevant keywords that categorizes that transcript.
    (uniqueness of word, frequency and relevance)

    frequency of terms using a Bag of Words model

    Bonus: Topic modeling

    Upload dataset's before:
    $ python3 dataset.py
"""

from __future__ import print_function
# import nltk
import logging
import json

from nltk.tokenize import sent_tokenize, word_tokenize, WordPunctTokenizer

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords, brown
from nltk.stem.snowball import SnowballStemmer
from gensim import models, corpora

File = './files/asrOutput.json'


def read_transcript_from_file():
    """ Load Input data """
    with open(File, 'rb') as fl:
        tscribe_json = json.load(fl)

    return tscribe_json['results']['transcripts'][0]['transcript']


def chunker(input_words, N=100):
   """
   Split the input text into chunks, where each chunk contains N words
   :param input_data: Array
   :param N:
   :return:
   """
   # input_words = input_data.split(' ')
   output = []

   cur_chunk = []
   count = 0
   for word in input_words:
       cur_chunk.append(word)
       count += 1
       if count == N:
           output.append(' '.join(cur_chunk))
           count, cur_chunk = 0, []
   output.append(' '.join(cur_chunk))
   return output


def remove_stop_words(tokens, lng='english'):
    # Get the list of stop words
    stop_words = stopwords.words(lng)

    # Remove the stop words
    return [x for x in tokens if not x in stop_words]


def process(input_text):
    """
    words, and stemming
    :param input_text:
    :return:
    """
    # Create a regular expression tokenizer
    tokenizer = RegexpTokenizer(r'\w+')

    # Tokenize the input string
    tokens = tokenizer.tokenize(input_text.lower())

    # Create a Snowball stemmer
    stemmer = SnowballStemmer('english', ignore_stopwords=True)

    tokens = remove_stop_words(tokens)

    # Perform stemming on the tokenized words
    tokens_stemmed = [stemmer.stem(x) for x in tokens]

    return tokens_stemmed


def lda_contributing_words(input_text, num_topics=2, num_words=10, passes=25):
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
    topics = []
    for item in ldamodel.print_topics(num_topics=num_topics,
                                      num_words=num_words):
        print('\nTopic', item[0])
        # Print the contributing words along with their relative contributions

        list_of_strings = item[1].split(' + ')
        topic = []
        for text in list_of_strings:
            weight = text.split('*')[0]
            word = text.split('*')[1]
            topic.append(word.replace('"', ''))
            print(word, '==>', str(round(float(weight) * 100, 2)) + '%')
        topics.append(' '.join(topic))

    return topics


def bag_words_model(input_text):
    # Frequency of terms using a Bag of Words model
    tokens = word_tokenize(input_text)
    tokens = remove_stop_words(tokens)

    # Number of words in each chunk
    chunk_size = 300
    text_chunks = chunker(tokens, chunk_size)

    # Convert to dict items
    chunks = []
    for count, chunk in enumerate(text_chunks):
        d = {'index': 0, 'text': chunk}
        chunks.append(d)

    # Extract the document term matrix
    # minimum and maximum document frequency
    count_vectorizer = CountVectorizer(min_df=2, max_df=20)
    document_term_matrix = count_vectorizer.fit_transform([chunk['text'] for
                                                           chunk in chunks])

    # Extract the vocabulary and display it
    vocabulary = np.array(count_vectorizer.get_feature_names())
    print("\nVocabulary:\n", vocabulary)

    # Generate names for chunks
    chunk_names = []
    for i in range(len(text_chunks)):
        chunk_names.append('Chunk-' + str(i + 1))

    # Print the document term matrix
    print("\nDocument term matrix:")
    formatted_text = '{:>12}' * (len(chunk_names) + 1)
    print('\n', formatted_text.format('Word', *chunk_names), '\n')
    for word, item in zip(vocabulary, document_term_matrix.T):
        # 'item' is a 'csr_matrix' data structure
        output = [word] + [str(freq) for freq in item.data]
        print(formatted_text.format(*output))


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)

    input_text = read_transcript_from_file()
    # print(input_text)

    # Frequency of terms using a Bag of Words model
    bag_words_model(input_text)

    # Topic modeling using Latent Dirichlet Allocation
    topics = lda_contributing_words(input_text)

    print(topics)


