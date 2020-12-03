import ast
import os
import pickle
import re
import  stemmer
from nltk.corpus import wordnet, stopwords
import  parser_module

import search_engine

if __name__ == '__main__':
    # stop_words = stopwords.words('english')
    # print("IS" in stop_words)

    General_Posting = {"a": [1, {}], "b": [1, {}], "c": [1, {}], "d": [1, {}], "e": [1, {}], "f": [1, {}],
                            "g": [1, {}], "h": [1, {}], "i": [1, {}], "j": [1, {}], "k": [1, {}], "l": [1, {}],
                            "m": [1, {}], "n": [1, {}], "o": [1, {}], "p": [1, {}], "q": [1, {}], "r": [1, {}],
                            "s": [1, {}], "t": [1, {}], "u": [1, {}], "v": [1, {}], "w": [1, {}], "x": [1, {}],
                            "y": [1, {}], "z": [1, {}], "@": [1, {}], "#": [1, {}], "other": [1, {}]}
    corpus_path= 'C:/Users/Admin/Desktop/data'
    output_path="C:/Users/Admin/Documents/GitHub/Engine_Search"
    stemming=False
    parser=parser_module.Parse(stemming,output_path)
    queries=["Dr. Anthony Fauci wrote in a 2005 paper published in Virology Journal that hydroxychloroquine was effective in treating SARS.",
             "The seasonal flu kills more people every year in the U.S. than COVID-19 has to date.","Coronavirus is less dangerous than the flu",
             "The coronavirus pandemic is a cover for a plan to implant trackable microchips and that the Microsoft co-founder Bill Gates is behind it",
            "Microsoft co-founder Bill Gates said `only the people who have all the vaccines will still be able to move freely`",
            "Bill Gates owns the patent and vaccine for coronavirus.",
            "Herd immunity has been reached.",
            "Children are “almost immune from this disease.”",
            "A study from the CDC and the WHO “proves face masks do not prevent the spread of a virus.”",
            "hydroxychloroquine, zinc, and Zithromax can cure coronavirus",
            "U.S. has “one of the lowest mortality rates in the world” from COVID-19",
            "The spread of COVID-19 will slow down as the weather warms up",
            "5G helps the spread of Covid-19",
            "Injecting or consuming bleach or disinfectant can cure coronavirus",
            "The COVID-19 pandemic was planned by the Rockefeller Foundation in “Operation Lockstep.“",
            "COVID-19 could lose its epidemic status in the United States because of declining coronavirus death rates according to CDC data.",
            "healthy people should NOT wear masks",
            "coronavirus is a bioweapon created in a lab in Wuhan",
            "The outbreak began because people ate bat soup",
            "Outbreak people ate bat",
            "coronavirus eat bat soup",
            "Wearing a mask to prevent the spread of COVID-19 is unnecessary because the disease can also be spread via farts.",
            "For younger people, seasonal flu is “in many cases” a deadlier virus than COVID-19.",
            "The coronavirus disease (COVID-19) is caused by a virus",
            "Covid-19 is not caused by bacteria",
            "The prolonged use of medical masks when properly worn, DOES NOT cause CO2 intoxication nor oxygen deficiency",
            "Masks don't cause CO2 intoxication.",
            "The COVID-19 coronavirus pandemic caused a nationwide shortage of U.S. coins in circulation during the summer of 2020.",
            "Coins shortage due to coronavirus",
            "People should NOT wear masks while exercising"]

    # for doc in queries:
    #     print("the originial quert_______________"+doc)
    #     print(parser.parse_sentence(doc))
    # def load_dictionary(name):
    #     db=open(name,'rb')
    #     dbfile=pickle.load(db)
    #     db.close()
    #     return  dbfile
    # print(load_dictionary("inverted_index.pkl.pkl"))

    #corpus_path = "testData"
    output_path = 'posting'
    num_docs_to_retrieve = 20

    search_engine.main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve)



# w1 = wordnet.synset('ship.n.01')
    # w2 = wordnet.synset('boat.n.01')
    # print(w1.wup_similarity(w2))
    # my_list=[]
    # word="dog"
    # synonyms = []
    # for syn in wordnet.synsets(word):
    #     print(syn)
    #     for l in syn.lemmas():
    #         synonyms.append(l.name())
    # my_list=(set(synonyms))
    # print(my_list)
    # for word_2 in my_list:
    #     print(word.wup_similarity(word_2)
    #
