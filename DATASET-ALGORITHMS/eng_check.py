import sqlalchemy as db
import pandas as pd
import sys
from sqlalchemy import create_engine, MetaData,Table, Column, Numeric, Integer, VARCHAR
from sklearn.metrics.pairwise import cosine_similarity
import pymysql

from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import spacy
from sklearn.feature_extraction.text import CountVectorizer

## Connect to the MySQL server
engine = create_engine('mysql://root:kakalot123@localhost:3306/db')


## Training data
train_model_en = pd.read_sql_query("select verses.id,verses.book_id,verses.chapter,verses.number,verses.text,books.id as books_id,books.name_id,books.name,books.short_name,books.version,books.language from verses  inner join books on verses.book_id = books.id where verses.book_id!=177 and books.language='en' and books.version='esv'", engine)
#train_model_en =train_model_en.drop(['concordance_index','created_at','updated_at','created_at','updated_at'],axis=1)
#print(train_model_en.head())

##Testing data, take a parameter from the system
test_value = sys.argv[1]
query_test = f"select verses.id,verses.book_id,verses.chapter,verses.number,verses.text,books.id as books_id,books.name_id,books.name,books.short_name,books.version,books.language from verses  inner join books on verses.book_id = books.id where verses.book_id=177 and books.language='en' and books.version='esv' and verses.id ={test_value}"
test_model_en = pd.read_sql_query(query_test,engine)
test_model_result =test_model_en.drop(['books_id','name','short_name','version','language'],axis=1)
print("Original version of test file: ")
print(test_model_result)

## Implement the string data
import string
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


en_nlp = spacy.load('en_core_web_sm')

def clean_text(txt):
    '''
    This function will clean the text being passed by removing specific line feed characters
    like '\n', '\r', and '\'
    '''

    txt = txt.replace('\n', ' ').replace('\r', ' ').replace('\'', '')
    txt = remove_punctuations(txt)
    txt = remove_stopwords(txt)
    return txt.lower()


def lemma_text(text_line):
    #test_file_clean = []
    doc_spacy = en_nlp(text_line)
    line = [ a.lemma_ for a in doc_spacy]
    #sentence = " ".join(line)
    #test_file_clean.append(sentence)
    return " ".join(line)



vectorizer1 = CountVectorizer(ngram_range=(2,4),stop_words="english")
vectorizer2 = CountVectorizer(ngram_range=(2,4),stop_words="english",min_df=0.55)

def check_plagiarism(train_file,test_file,vectorizer):
    documents = [train_file,test_file]
    sparse_matrix = vectorizer.fit_transform(documents)
    score = cosine_similarity(sparse_matrix)[0][1]
    return score

def show_result(train_file,test_file):
    score = check_plagiarism(train_file,test_file,vectorizer1)
    if score >0.2:
        score = check_plagiarism(train_file,test_file,vectorizer2)
    return score

text = train_model_en['text'].tolist()
verses_id = train_model_en['id'].tolist()

s_vector = list(zip(verses_id,text))

def check_plagiarism_soft(test_file,s_vector):
    result = {"id":[],"score":[]}
    for a,v_vector in s_vector:
        test_file = clean_text(test_file)
        test_file = lemma_text(test_file)
        v_vector = clean_text(v_vector)
        v_vector = lemma_text(v_vector)
        score = show_result(v_vector,test_file)
        result['id'].append(a)
        result['score'].append(score)
    dt = pd.DataFrame(result)
    result_file =[dt.loc[dt['score']==max(dt['score'])]['id'].tolist()[0],dt.loc[dt['score']==max(dt['score'])]['score'].tolist()[0]]
    return result_file

#Take the text of the test file
test_file = test_model_en['text'].apply(str)
result = check_plagiarism_soft(test_file,s_vector)

result_model_en = pd.read_sql_query(f"select verses.id,verses.book_id,verses.chapter,verses.number,verses.text from verses where verses.id={result[0]}", engine)
result_model_en['score'] = result[1]
print("Result: ")
print(result_model_en)