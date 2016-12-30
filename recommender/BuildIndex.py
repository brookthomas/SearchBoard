from __future__ import division
from Corpus import Corpus
from SentimentAnalyzer import SentimentAnalyzer
from nltk.stem.porter import *
from nltk.tokenize import sent_tokenize
import os
import re
from math import log10 
import json

class BuildIndex:

  OUTPUT_DIRECTORY = '../data/indices/'
  
  def __init__(self, corpus, open_tag, close_tag):
    self.corpus = Corpus(corpus, open_tag, close_tag)
    self.stemmer = PorterStemmer()
    self.sentiment_analyzer = SentimentAnalyzer()
    self.positional_index = {}
    self.sentiment = {}
    self.idf = {}
    self.bm25 = {}
    self.sentence_index = {}
    
  def buildAll(self):
    print 'Creating IDF Index'
    self.createIDFIndex()
    print 'Done.'
    print 'Creating Positional Index'
    self.createPositionalIndex()
    print 'Done'
    print 'Creating BM25 Index'
    self.createBM25Index()
    print 'Done'
    print 'Creating Sentiment Index'
    self.createSentimentIndex()
    print 'Done'
    print 'Creating Sentence Index'
    self.createSentenceIndex()
    print 'Done'

  """
    Core methods for generating Indexes. 
    Each can be run standalone, but some instances may initialize others first
  """
  def createPositionalIndex(self):
    if not os.path.exists(BuildIndex.OUTPUT_DIRECTORY):
      os.makedirs(BuildIndex.OUTPUT_DIRECTORY)

    while True:   # My biggest gripe with Python, no assignments in conditionals
      document = self.corpus.getNext()
      if document == None:
        break

      sentences = self.tokenizeToSentences(document['text'])

      for i in range(0, len(sentences)):
        for term in self.tokenizeOnNonAlphanumeric(sentences[i]):
          term = self.lowercase(term)
          term = self.stem(term)

          if term not in self.positional_index:
            self.positional_index[term] = {}

          if document['id'] not in self.positional_index[term]:
            self.positional_index[term][document['id']] = []

          if i not in self.positional_index[term][document['id']]:
            self.positional_index[term][document['id']].append(i)

    with open(BuildIndex.OUTPUT_DIRECTORY + 'positional_index', 'w') as outfile:
      json.dump(self.positional_index, outfile)

  def createIDFIndex(self):
    if not os.path.exists(BuildIndex.OUTPUT_DIRECTORY):
      os.makedirs(BuildIndex.OUTPUT_DIRECTORY)

    all_doc_frequency = {}
    doc_count = 0

    while True:
      document = self.corpus.getNext()
      if document == None:
        break

      this_doc = {}
      doc_count += 1

      # Log instances of terms in doc
      for term in self.tokenizeOnNonAlphanumeric(document['text']):
        term = self.lowercase(term)
        term = self.stem(term)

        if term not in this_doc:
          this_doc[term] = True

      # Add terms from that doc to overall count
      for term in this_doc:
        if term not in all_doc_frequency:
          all_doc_frequency[term] = 0
        
        all_doc_frequency[term] += 1

    # Compile IDF
    for term in all_doc_frequency:
      self.idf[term] = round(log10(doc_count/all_doc_frequency[term]),6)

    with open(BuildIndex.OUTPUT_DIRECTORY + 'idf', 'w') as outfile:
      json.dump(self.idf, outfile)

  def createBM25Index(self):
    K1 = 1.2
    B = 0.75
    document_lengths = {}
    term_document_count = {}
    
    # We need the IDF data for this, so make sure we have it
    if len(self.idf) == 0:
      self.createIDFIndex()

    # Aggregate Document Data
    while True:
      document = self.corpus.getNext()
      if document == None:
        break

      terms = self.tokenizeOnNonAlphanumeric(document['text'])
      document_lengths[document['id']] = len(terms)

      for term in terms:
        term = self.lowercase(term)
        term = self.stem(term)

        if term not in term_document_count:
          term_document_count[term] = {}

        if document['id'] not in term_document_count[term]:
          term_document_count[term][document['id']] = 0

        term_document_count[term][document['id']] += 1

    # Computer Average Document Length
    average_doc_length = sum([document_lengths[i] for i in document_lengths.keys()]) / len(document_lengths)

    # Compute BM25
    for term in term_document_count:
      for doc_id in term_document_count[term]:
        df = term_document_count[term][doc_id]
        num = df * (K1 + 1)
        den_nested = 1 - B + (B * (document_lengths[doc_id] / average_doc_length))
        bm25 = self.idf[term] * (num / (df + K1 * den_nested))

        if term not in self.bm25:
          self.bm25[term] = {}

        self.bm25[term][doc_id] = round(bm25,4)

    with open(BuildIndex.OUTPUT_DIRECTORY + 'bm25', 'w') as outfile:
      json.dump(self.bm25, outfile)

  def createSentimentIndex(self):
    if not os.path.exists(BuildIndex.OUTPUT_DIRECTORY):
      os.makedirs(BuildIndex.OUTPUT_DIRECTORY)

    while True:
      document = self.corpus.getNext()
      if document == None:
        break

      sentences = self.tokenizeToSentences(document['text'])
      self.sentiment[document['id']] = self.sentiment_analyzer.analyze(sentences)

    with open(BuildIndex.OUTPUT_DIRECTORY + 'sentiment', 'w') as outfile:
      json.dump(self.sentiment, outfile)

  def createSentenceIndex(self):
    if not os.path.exists(BuildIndex.OUTPUT_DIRECTORY):
      os.makedirs(BuildIndex.OUTPUT_DIRECTORY)

    while True:
      document = self.corpus.getNext()
      if document == None:
        break
      self.sentence_index[document['id']] = self.tokenizeToSentences(document['text'])
    
    with open(BuildIndex.OUTPUT_DIRECTORY + 'sentences', 'w') as outfile:
      json.dump(self.sentence_index, outfile)

  """
    Helper methods for text processing
  """
  REGEX_NON_ALPHANUMERIC = re.compile('[^a-zA-Z0-9]')

  def stem(self, term):
    return self.stemmer.stem(term)

  def lowercase(self, text):
    return text.lower()

  def tokenizeToSentences(self, text):
    return sent_tokenize(text)

  def tokenizeOnNonAlphanumeric(self,text):
    return [term for term in re.split(BuildIndex.REGEX_NON_ALPHANUMERIC, text) if term != '']



if __name__ == '__main__':
  buildindex = BuildIndex('../data/combined.txt', '<GAME (.*)>', '</GAME>')
  buildindex.buildAll()


