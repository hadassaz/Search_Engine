import ast
import re

from nltk.corpus import wordnet

import search_engine

if __name__ == '__main__':
    corpus_path= 'C:/Users/Admin/Desktop/data'
    output_path="C:/Users/Admin/Documents/GitHub/Engine_Search"
    stemming=False
    queries=["going"]
    num_docs_to_retrieve=20
    search_engine.main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve)

