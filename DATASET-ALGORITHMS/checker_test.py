#import cProfile
import pandas as pd
#import sys
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import spacy
from sklearn.feature_extraction.text import CountVectorizer
import string
import concurrent.futures
import time
import optparse


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

en_nlp = spacy.load('en_core_web_sm')
def lemma_text(text_line):
    #test_file_clean = []
    doc_spacy = en_nlp(text_line)
    line = [ a.lemma_ for a in doc_spacy]
    #sentence = " ".join(line)
    #test_file_clean.append(sentence)
    return " ".join(line)



vectorizer1 = CountVectorizer(ngram_range=(2,4),stop_words="english")
vectorizer2 = CountVectorizer(ngram_range=(2,4),stop_words="english",min_df=0.55)

class Checker():
    ## Connect to the MySQL server
    engine = create_engine('mysql://root:kakalot123@localhost:3306/db')
    # book_id =177
    # language = 'en'
    def __init__(self,version,score,test_id):
        self.version = version
        self.score = score
        self.test_id = test_id
        if(self.version =='esv'):
            self.book_id =177
            self.language ='en'
            self.train_query = """select * from english_model"""
            self.train_model = pd.read_sql_query(self.train_query, self.engine)
            self.text = self.train_model['text'].tolist()
            self.verses_id = self.train_model['verse_id'].tolist()
        elif(self.version =='vie2010'):
            self.book_id =397
            self.language ='vi'
            self.train_query = """select * from vietnamese_model"""
            self.train_model = pd.read_sql_query(self.train_query, self.engine)
            self.text = self.train_model['text'].tolist()
            self.verses_id = self.train_model['verse_id'].tolist()

        # print(self.test_id)
        # print(self.version)
        # print(self.book_id)
        # print(self.language)
        self.test_query = """select verses.id,verses.book_id,verses.chapter,verses.number,verses.text,books.id as books_id,books.name_id,books.name,books.short_name,books.version,books.language from verses  inner join books on verses.book_id = books.id where verses.book_id={} and books.language='{}' and verses.id ={} and books.version='{}'""".format(self.book_id,self.language,self.test_id,self.version)
        self.test_model = pd.read_sql_query(self.test_query,self.engine).drop(['books_id','name','short_name','version','language'],axis=1)
        #self.text = self.train_model['text'].tolist()

        #self.verses_id = self.train_model['id'].tolist()
        if(self.version =='esv'):
            self.test_file = clean_text(self.test_model['text'].apply(str))
            self.test_file = lemma_text(self.test_file)
        elif(self.version =='vie2010'):
            self.test_file = clean_text_vi(self.test_model['text'].apply(str))
        self.s_vector = list(zip(self.verses_id,self.text))
        #self.test_file = self.test_model['text'].apply(str)

    def check_plagiarism(self,train_file,test_file,vectorizer):
        documents = [train_file,test_file]
        sparse_matrix = vectorizer.fit_transform(documents)
        score = cosine_similarity(sparse_matrix)[0][1]
        return score
    def show_result(self,train_file,test_file):

        score = self.check_plagiarism(train_file,test_file,vectorizer1)
        if score >float(self.score):
            score = self.check_plagiarism(train_file,test_file,vectorizer2)
        return score



    #def check_plagiarism_soft(self,test_file,s_vector):
    def check_plagiarism_soft(self):
        #self.test_file = test_file
        #self.text = text
        #self.verses_id = verses_id
        #self.s_vector = s_vector
        result = {"id":[],"score":[]}

        # if(self.version=='esv'):
        #     self.text = [clean_text(txt) for txt in self.text]
        #     self.text = [lemma_text(txt) for txt in self.text ]
        #     self.test_file = clean_text(self.test_file)
        #     self.test_file = lemma_text(self.test_file)
        # elif(self.version =='vie2010'):
        #     self.test_file = clean_text_vi(self.test_file)
        test_file_list =[self.test_file for i in range(len(self.text))]
        # for i in range(len(self.text)):
        #     test_file_list.append(self.test_file)
        result['id'] = self.verses_id
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            score = executor.map(self.show_result,self.text,test_file_list)
        result['score'] = score

        # for a,v_vector in self.s_vector:
        #     test_file = clean_text(self.test_file)

        #     if(self.version=='esv'):
        #         v_vector = clean_text(v_vector)
        #         test_file = lemma_text(test_file)
        #         v_vector = lemma_text(v_vector)
        #     elif(self.version =='vie2010'):
        #         v_vector = clean_text_vi(v_vector)
        #     score = self.show_result(v_vector,test_file)
        #     result['id'].append(a)
        #         #score.append(executor.submit(self.show_result, train_file=v_vector,test_file=test_file))
        #     result['score'].append(score)

        #     result['score'] = score
        dt = pd.DataFrame(result)
        result_file =[dt.loc[dt['score']==max(dt['score'])]['id'].tolist()[0],dt.loc[dt['score']==max(dt['score'])]['score'].tolist()[0]]
        return result_file


    def show_final_result(self):
        #result = self.check_plagiarism_soft(self.test_file,self.s_vector)
        result = self.check_plagiarism_soft()
        result_model = pd.read_sql_query(f"select verses.id,verses.book_id,verses.chapter,verses.number,verses.text from verses where verses.id={result[0]}", self.engine)
        result_model['score'] = result[1]
        df = result_model.to_dict('records')
        return df






def main():
    start = time.time()
    parser = optparse.OptionParser()

    # add options
    parser.add_option('-v','--version', dest = 'version',
                      type = 'string',
                      help = 'choose english or vietnamese version')
    parser.add_option('-t','--testid', dest = 'testid',
                      type = 'string',
                      help = 'please enter the test id')
    parser.add_option('-s','--score', dest = 'score',
                      type = 'string',
                      help = 'please enter the algorithm score')


    (options, args) = parser.parse_args()
    if (options.version == None):
            print ("Version is not null")
            exit(0)
    else:
            version = options.version

    if (options.testid == None):
            print ("Test id is not null")
            exit(0)
    else:
            testid = options.testid

    if (options.score == None):
            print ("The score is not null")
            exit(0)
    else:
            score = options.score
    my_checker = Checker(version,score,testid)
    print(my_checker.version)
    print(my_checker.score)
    print(my_checker.test_id)
    print(my_checker.show_final_result())

    end = time.time()
    print("It takes: ",end -start)


if __name__ == "__main__":
    main()