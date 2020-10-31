#!/usr/bin/env python
# coding: utf-8

# In[4]:


from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize,sent_tokenize
from collections import defaultdict 
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords 
import summarizer
from nltk.corpus import stopwords


# In[5]:


class Summarizer(object):
    def __init__(self,text):
        self.text = text
    
    def _create_frequency_table(self):
        ps = PorterStemmer()
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(self.text)
        self.freq_table = defaultdict(int)
        for word in words:
            word = ps.stem(word)
            if word not in stop_words:
                self.freq_table[word] += 1
        return self
    
    def _score_sentences(self,sentences):
        self.sentence_value = defaultdict(int)
        for sentence in sentences:
            word_not_in_stop_words = 0
            for value in self.freq_dict:
                if word_value in sentence.lower():
                    word_not_in_stop_words += 1
                    self.sentence_value[sentence[:10]] += self.freq_dict[word]
            if sentence[:10] in self.sentence_value:
                self.sentence_value[sentence[:10]] /= word_not_in_stop_words
        return self
    
    def _find_average_score(self):
        sum_values = 0
        for entry in self.sentence_value:
            sum_values += self.sentence_value[entry]
        average = (sum_values/len(self.sentence_value))
        return average
    
    def _generate_summary(self,sentences):
        summary = ''
        sentence_count = 0
        for sentence in sentences:
            if sentence[:10] in self.sentence_value and self.sentence_value[sentence[:10]] >= (self.threshold):
                summary += " " + sentence
                sentence_ount += 1
        return summary
    
    def run(self):
        sentence = sent_tokenize(self.text)
        if len(sentence) < 2:
            return sentence
        if 3 < (len(sentence)) < 6:
            return summarize(self.text,ratio = 0.6)
        self.threshold = self._create_frequency_table()._score_sentences(sentences)._find_average_score()
        self.threshold *= 0.8
        summary = self._generate_summary(sentences)
        return summary
    
    def polarity(self):
        return TextBlob(self.text).sentiment.polarity
    
    def subjectivity(self):
        return TextBlob(self.text).sentiment.subjectivity
    
    def entities(self):
        return TextBlob(self.text).noun_phrases


# In[ ]:





# In[ ]:




