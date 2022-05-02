
import pandas as pd
#import sys
from sqlalchemy import create_engine

from nltk.corpus import stopwords
import spacy
from sklearn.feature_extraction.text import CountVectorizer
import string

import time
import optparse
#from nltk.stem.wordnet import WordNetLemmatizer



## Implement the string data

def remove_punctuations(txt, punct = string.punctuation):
    '''
    This function will remove punctuations from the input text
    '''
    return ''.join([c for c in txt if c not in punct])

def remove_stopwords(txt, sw = list(stopwords.words('english'))):
    '''
    This function will remove the stopwords from the input txt
    '''
    return ' '.join([w for w in txt.split() if w.lower() not in sw])


en_nlp = spacy.load('en_core_web_sm',disable=['ner','pos'])
def clean_text(txt):
    '''
    This function will clean the text being passed by removing specific line feed characters
    like '\n', '\r', and '\'
    '''

    txt = txt.replace('\n', ' ').replace('\r', ' ').replace('\'', '')
    txt = remove_punctuations(txt)
    txt = remove_stopwords(txt)
    return txt.lower()

def clean_text_vi(txt):
    '''
    This function will clean the text being passed by removing specific line feed characters
    like '\n', '\r', and '\'
    '''

    txt = txt.replace('\n', ' ').replace('\r', ' ').replace('\'', '')
    txt = remove_punctuations(txt)

    return txt.lower()
#en_nlp = spacy.load('en_core_web_sm',disable=['ner','pos'])
#en_nlp.disable_pipes('tagger', 'ner')
en_nlp = spacy.load('en_core_web_sm', disable=['ner', 'parser'])
#en_nlp.add_pipe(en_nlp.create_pipe('sentencizer'))

def lemma_text(text_line):
    #test_file_clean = []
    doc_spacy = en_nlp(text_line)
    line = [ a.lemma_ for a in doc_spacy]
    #sentence = " ".join(line)
    #test_file_clean.append(sentence)

    return " ".join(line)


#vectorizer0 = CountVectorizer(ngram_range=(1,1))
vectorizer1 = CountVectorizer(ngram_range=(2,4))
vectorizer2 = CountVectorizer(ngram_range=(2,4),min_df=0.55)

class Lemma_checker():
    ## Connect to the MySQL server
    engine = create_engine('mysql://root:kakalot123@localhost:3306/db')
    # book_id =177
    # language = 'en'
    def __init__(self,version):
        self.version = version
        #self.score = score
        #self.test_id = test_id
        if(self.version =='esv'):
            self.book_id =177
            self.language ='en'
        elif(self.version =='vie2010'):
            self.book_id =397
            self.language ='vi'
        self.train_query = """select verses.id,verses.text from verses  inner join books on verses.book_id = books.id where verses.book_id!={} and books.language='{}' and books.version='{}'""".format(self.book_id,self.language,self.version)
        self.train_model = pd.read_sql_query(self.train_query, self.engine)
        # print(self.test_id)
        # print(self.version)
        # print(self.book_id)
        # print(self.language)
        #self.test_query = """select verses.id,verses.text from verses  inner join books on verses.book_id = books.id where verses.book_id={} and books.language='{}' and verses.id ={} and books.version='{}'""".format(self.book_id,self.language,self.test_id,self.version)
        #self.test_model = pd.read_sql_query(self.test_query,self.engine)
        self.text = self.train_model['text'].tolist()
        if(self.version=='esv'):
            self.text = [clean_text(txt) for txt in self.text]
            self.text = [lemma_text(txt) for txt in self.text ]
        elif(self.version =='vie2010'):
            self.text = [clean_text_vi(txt) for txt in self.text]
            #self.test_file = clean_text_vi(self.test_file)
        self.verses_id = self.train_model['id'].tolist()
        self.s_vector = list(zip(self.verses_id,self.text))
        #self.test_file = self.test_model['text'].apply(str)
    def create_table(self):
        result = {'text':[], 'verse_id':[]}
        if(self.version=='esv'):
            self.text = [clean_text(txt) for txt in self.text]
            self.text = [lemma_text(txt) for txt in self.text ]
            result['text'] = self.text
            result['verse_id'] = self.verses_id
            result = pd.DataFrame(result)
            result.to_sql('english_model',self.engine)
        elif(self.version =='vie2010'):
            self.text = [clean_text_vi(txt) for txt in self.text]
            result['text'] = self.text
            result['verse_id'] = self.verses_id
            result = pd.DataFrame(result)
            result.to_sql('vietnamese_model',self.engine)

def main():
    start = time.time()
    parser = optparse.OptionParser()

    # add options
    parser.add_option('-v','--version', dest = 'version',
                      type = 'string',
                      help = 'choose english or vietnamese version')
    # parser.add_option('-t','--testid', dest = 'testid',
    #                   type = 'string',
    #                   help = 'please enter the test id')
    # parser.add_option('-s','--score', dest = 'score',
    #                   type = 'string',
    #                   help = 'please enter the algorithm score')


    (options, args) = parser.parse_args()
    if (options.version == None):
            print ("Version is not null")
            exit(0)
    else:
            version = options.version

    # if (options.testid == None):
    #         print ("Test id is not null")
    #         exit(0)
    # else:
    #         testid = options.testid

    # if (options.score == None):
    #         print ("The score is not null")
    #         exit(0)
    # else:
    #         score = options.score
    my_checker = Lemma_checker(version)
    print(my_checker.version)
    # print(my_checker.score)
    # print(my_checker.test_id)
    print(my_checker.create_table())

    end = time.time()
    print("It takes: ",end -start)


if __name__ == "__main__":
    main()