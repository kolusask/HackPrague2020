#!/usr/bin/env python
# coding: utf-8

# In[24]:


import pandas as pd                       
from sklearn.svm import LinearSVC
from nltk.classify import SklearnClassifier
from random import shuffle
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
import numpy as np
import nltk
import abc
import pickle
from nltk.corpus import stopwords
from collections import defaultdict
from collections import Counter
from nltk import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
nltk.download('punkt')
nltk.download('wordnet')


# In[2]:


class PreProcessor(abc.ABC):
    @abc.abstractmethod
    def apply(self,obj):
        pass

class SimpleTokenizer(PreProcessor):
    def apply(self,text):
        return word_tokenize(text)
    
class Lemmatization(PreProcessor):
    
    def __init__(self,lemmatizer):
        self._lemmatizer = lemmatizer
        self.table = str.maketrans({key: None for key in string.punctuation})
    
    def apply(self,text):
        filtered_tokens = []
        stop_words = set(stopwords.words('english'))
        text = text.translate(self.table)
        for word in text.split():
            if word not in stop_words:
                filtered_tokens.append(self._lemmatizer.lemmatize(word.lower()))
        return filtered_tokens

class AdvancedLemmatization(PreProcessor):
    def __init__(self,lemmatizer):
        self._lemmatizer = lemmatizer
        self.table = str.maketrans({key: None for key in string.punctuation})
    
    def apply(self,text):
        filtered_tokens = []
        lemmatized_tokens = []
        stop_words = set(stopwords.words('english'))
        text = text.translate(self.table)
        for word in text.split():
            if word not in stop_words:
                lemmatized_tokens.append(self._lemmatizer.lemmatize(word.lower()))
            filtered_tokens = [' '.join(l) for l in nltk.bigrams(lemmatized_tokens)] + lemmatized_tokens
        return filtered_tokens


# In[3]:


class Encoder(abc.ABC):
    
    @abc.abstractmethod
    def encode(self,item):
        pass

class BinaryEncoder(Encoder):
    def __init__(self):
        self._features = Counter()
    def encode(self,tokens): 
        self._features += Counter(tokens)
        return Counter(tokens)
            


# In[4]:


class DataSet:
    
    def __init__(self,path,label_column = 'LABEL',delimiter = '\t',mapping = None,transformators = []):
        self._data = pd.read_csv(path,delimiter = delimiter)
        if mapping is not None:
            self._data[label_column] = self._data[label_column].map(mapping)
        self.raw_data = []
        self.preprocessed = []
        self._transformators = transformators
    
    def extract_item(self,position,args):
        return tuple(self._data[args].iloc[position])
    
    def transform(self,args,apply_to):
        self.index = apply_to
        for idx in range(self._data.shape[0]):
            items = self.extract_item(idx,args)
            self.raw_data.append(items)
            transformed = items[apply_to]
            for transformer in self._transformators:
                transformed = transformer.apply(transformed)
            temp_items = list(items)
            temp_items[apply_to] = transformed
            self.preprocessed.append(tuple(temp_items))


            
                        
            


# In[27]:


class Classification:
    def __init__(self,dataset,model = LinearSVC,**kwargs):
        self._dataset = dataset
        self._model = SklearnClassifier(Pipeline([('ml_model',model(**kwargs))]))
        self.train_data = []
        self.test_data = []
        
    def split(self,ratio,vectorizer):
        raw_length = len(self._dataset.raw_data)
        middle = int(raw_length/2)
        traning_number = int(ratio*raw_length/2)
        for item in self._dataset.preprocessed[:traning_number] + self._dataset.preprocessed[middle:middle+traning_number:]:
            self.train_data.append((vectorizer.encode(item[self._dataset.index]),item[-1]))
        for item in self._dataset.preprocessed[traning_number:middle] + self._dataset.preprocessed[middle+traning_number:]:
            self.test_data.append((vectorizer.encode(item[self._dataset.index]),item[-1]))
    
    def train(self,train_data):
        return self._model.train(train_data)
    
    def predict(self,review,vectorizer = BinaryEncoder(),tokenizer = SimpleTokenizer()):
        return self._model.classify(vectorizer.encode(tokenizer.apply(review)))
    
    def load(self,path):
        with open(path,'rb') as f:
            self._model = pickle.load(f)
    
    def save(self,path):
        with open(path,'rb') as f:
            pickle.dump(self._model,f)
            
    def predict_many(self,reviews):
        return self._model.classify_many(map(lambda t:t[0],reviews))
    
    def cross_validation(self,folds):
        shuffle(self.train_data)
        self.cv_ = []
        fold = int(len(self.train_data)/folds)
        for idx in range(0,len(self.train_data),fold):
            clf = self.train(self.train_data[:idx] + self.train_data[fold+idx:])
            y_predicted = self.predict_many(self.train_data[idx:idx +fold])
            a = accuracy_score(list(map(lambda d:d[1],self.train_data[idx:idx+fold])),y_predicted)
            (p,r,f,_) = precision_recall_fscore_support(list(map(lambda d : d[1], self.train_data[idx:idx+fold])), y_predicted, average ='macro')
            print(p,r,f)
            self.cv_.append((a,p,r,f))
        self.cv_ = (np.mean(np.array(self.cv_),axis =  0))
        


# In[132]:


reader = DataSet('amazon_reviews.txt',mapping = {'__label1__':'FAKE','__label2__':'NOT FAKE'},transformators= [SimpleTokenizer()])
reader.transform(['DOC_ID','REVIEW_TEXT','LABEL'],apply_to = 1)


# In[135]:


clf = Classification(reader)
clf.split(0.8,BinaryEncoder())
clf.train(clf.train_data)


# In[136]:


clf.cross_validation(10)


# In[137]:


clf.cv_


# ## With Lemmatization and removing all non important word

# In[7]:


reader = DataSet('amazon_reviews.txt',mapping = {'__label1__':'FAKE','__label2__':'NOT FAKE'},transformators= [Lemmatization(WordNetLemmatizer())])
reader.transform(['DOC_ID','REVIEW_TEXT','LABEL'],apply_to = 1)


# In[8]:


clf_1 = Classification(reader)
clf_1.split(0.8,BinaryEncoder())
clf_1.train(clf_1.train_data)
clf_1.cross_validation(10)


# In[9]:


clf_1.cv_


# In[13]:


reader = DataSet('amazon_reviews.txt',mapping = {'__label1__':'FAKE','__label2__':'NOT FAKE'},transformators= [AdvancedLemmatization(WordNetLemmatizer())])
reader.transform(['DOC_ID','REVIEW_TEXT','LABEL'],apply_to = 1)


# In[16]:


clf_2 = Classification(reader,model = LinearSVC,C = 0.01)
clf_2.split(0.8,BinaryEncoder())
clf_2.train(clf_2.train_data)
clf_2.cross_validation(10)


# In[17]:


clf_2.cv_


# In[18]:


df = pd.read_csv('amazon_reviews.txt',delimiter = '\t')
df.columns


# In[22]:


reader = DataSet('amazon_reviews.txt',label_column = 'RATING',transformators = [AdvancedLemmatization(WordNetLemmatizer())])
reader.transform(['DOC_ID','REVIEW_TEXT','RATING'],apply_to = 1)


# In[23]:


clf_3 = Classification(reader,model = LinearSVC,C = 0.01)
clf_3.split(0.8,BinaryEncoder())
clf_3.train(clf_3.train_data)
clf_3.cross_validation(10)


# In[26]:


clf_3.cv_

