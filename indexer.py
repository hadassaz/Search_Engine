import ast
import linecache
import pickle
from math import log


class Indexer:
    num_of_doc=0
    def __init__(self, config):
        # the Main Dictionary {Term:unique doc}
        self.inverted_idx = {}
        #the posting files   {term: [(doc1,freq in doc),(doc3,8),(doc5,7)]-sorted list by doc id}
        self.postingDict = {}
        # dictionary to retreive the line number of specific key..{doc id:line number in text file}
        self.Doc_Line_Number = {}
        # [doc id,[doc info]]....doc info=[max_term(str),max freq(int),unique terms(int),wij^2,dictionary{term:(freq,indices(list),wij}
        self.Doc_Info_Text = []
        #counter for the line in the text to write
        self.Next_line = 1
        self.config = config

    def add_new_doc(self, document):
        Indexer.num_of_doc = Indexer.num_of_doc + 1
        document_dictionary = document.term_doc_dictionary
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        # Go over each term in the doc
        #the upper lower sort.. decide if the word will be saved in upper or lower case and update the matches terms
        for term in document_dictionary.keys():
            upper = term.upper()
            lower = term.lower()
            toReturn=""
            # Update inverted index and posting
            if (lower not in self.inverted_idx):
                # the word start with lower case char
                if ( term[0].islower()) or (len(term)>1 and term[1].islower() and (term[0]=='@' or term[0]=='#') ):
                    self.inverted_idx[lower] = 1
                    self.postingDict[lower]=[]
                    toReturn = lower
                    if (upper in self.inverted_idx):
                        self.inverted_idx[lower] += self.inverted_idx[upper]
                        self.inverted_idx.pop(upper, None)
                        if upper in self.postingDict:
                            self.postingDict[lower].append(self.postingDict[upper])
                            self.postingDict.pop(upper,None)
                # the word start with upper case char
                else:
                    toReturn = upper
                    if (upper in self.inverted_idx):
                        self.inverted_idx[upper] += 1
                        if upper not in self.postingDict:
                            self.postingDict[upper] = []
                    else:
                        self.inverted_idx[upper] = 1
                        self.postingDict[upper]=[]
            else:
                self.inverted_idx[lower] += 1
                if lower not in self.postingDict:
                    self.postingDict[lower] = []
                toReturn=lower

            self.add_to_Posting_sorted(toReturn,document.tweet_id,document_dictionary[term])
        self.doc_info(document)
        if Indexer.num_of_doc==100000:
            self.save_with_pickle()
            self.save_file_Info()
        elif Indexer.num_of_doc%100000 == 0:
            self.merge_and_save_posting()
            self.Load_Doc_Info(document.tweet_id)


    def save_with_pickle(self):
        db=open('Pickle_Save_posting',"wb")
        pickle.dump(self.postingDict, db)
        db.close()
        self.postingDict = {}

    def load_dictionary(self):
        db=open('Pickle_Save_posting','rb')
        dbfile=pickle.load(db)
        db.close()
        return  dbfile

    def merge_and_save_posting(self):
        saved_dict = self.load_dictionary()
        for term in self.postingDict:
            if term in saved_dict:
                for doc in self.postingDict[term]:
                    saved_dict[term].append(doc)
            else:
                saved_dict[term] = self.postingDict[term]
        self.postingDict=saved_dict
        self.save_with_pickle()

    def save_file_Info(self):
        import os.path
        #check if the file is already exist
        if(os.path.isfile("Documnet_info.txt")):
            param="a"
        else:
            param="w"
        with open('Documnet_info.txt', param) as my_file:
                for doc in self.Doc_Info_Text:
                    my_file.write('%s\n' % (str(doc[1]).encode("utf-8")))
                    self.Doc_Line_Number[doc[0]]=self.Next_line
                    self.Next_line+=1
        self.Doc_Info_Text=[]

    def Load_Doc_Info (self,Doc_id):
        Doc_line = self.Doc_Line_Number[Doc_id]
        fp = open("Documnet_info.txt")
        for i, line in enumerate(fp):
            if i ==Doc_line:
                #x=linecache.getline("listfile.txt", Doc_line, module_globals=None)
                line=ast.literal_eval(line)
                line=line.decode( ("utf-8"))
                line=ast.literal_eval(line)
                print(type(line))
                print(line)
                return  line
        #fp.close()
        #x = linecache.getline("Documnet_info.txt", Doc_line, module_globals=('UTF-8'))
        #x=ast.literal_eval(x)
        #return  x

    def add_to_Posting_sorted(self, toReturn, document_tweet_id, frequency):
        if((self.postingDict[toReturn]==[])):
            self.postingDict[toReturn]=[(document_tweet_id,frequency)]
        else:
            index = self.binary_insert(self.postingDict[toReturn], document_tweet_id)
            self.postingDict[toReturn].insert(index, (document_tweet_id, frequency))

    def binary_insert(self, list_doc, doc_id):
        low = 0
        high = len(list_doc) - 1
        mid = 0
        doc_id=str(doc_id)
        if(len(list_doc)==1):
            if(doc_id<list_doc[0][0]):
                return 0
            return 1
        while low <= high:
            mid = (high + low) // 2

            if (mid == low) and ((doc_id) < list_doc[high][0]) and (doc_id > list_doc[low][0]):
                return high
            elif list_doc[mid][0] < doc_id:
                low = mid + 1
            elif list_doc[mid][0] > doc_id:
                high = mid - 1

    def doc_info(self, doc):
        text_info = [doc.max_term, len(doc.term_doc_dictionary), doc.term_doc_dictionary]
        self.Doc_Info_Text.append((doc.tweet_id, text_info))

    def add_wij_to_doc(self):
        with open('Documnet_info_Wij.txt', 'w') as to_write:
            with open('Documnet_info_Wij.txt', 'w') as to_read:
                for i, line in enumerate(to_read):
                    line = ast.literal_eval(line)
                    line = line.decode(("utf-8"))
                    doc_info_list = ast.literal_eval(line)


                    square_wij=0
                    doc_term = doc_info_list[3]
                    for term in doc_term:
                        wij = self.calc_wij(doc_term[term][0], self.inverted_idx[term], len(self.Doc_Line_Number))
                        square_wij+=wij
                        doc_term[term] = doc_term[term] + (wij,)
                    x[2] = doc_term
                    my_file.writelines(8,'%s\n' % (str(x)))

    def calc_wij(self, tf, df, n):
        return tf * (log((n - df + 0.5) / (df + 0.5)))