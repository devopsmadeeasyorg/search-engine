"""
This module is to preprocess search string before triggering search
"""
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class Text_Preprocessor():
    def __init__(self, search_string):
        self.search_string = search_string

    def remove_urls(self, search_string):
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        text_without_urls = url_pattern.sub('', search_string)
        return text_without_urls
    
    def remove_punctuation(self, string_without_url):
        # Define a set of punctuation to remove, excluding ' " , - _
        punct = set(string.punctuation)
        punct.discard("'")
        punct.discard('"')
        punct.discard(",")
        punct.discard("-")
        punct.discard("_")
        text_without_punct = ''.join([har if char not in punct else ' ' for char in string_without_url])
        text_without_punct = ''.join(text_without_punct.split())
        return text_without_punct
    
    def remove_stop_words(self, search_string):
        nltk.download('stopwords')
        tokens = nltk.word_tokenize(search_string)
        filtered_tokens = [token for token in tokens if token.lower() not in stopwords.words('english')]
        text_without_stopwords = ' '.join(filtered_tokens)
        return text_without_stopwords
    
    def lemmatize(self, search_string):
        nltk.download('wordnet')
        tokens = nltk.word_tokenize(search_string)
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
        text_lemmatized = ' '.join(lemmatized_tokens)
        return text_lemmatized
    
    def tokenize_text(self, search_string):
        tokens = set(nltk.word_tokenize(search_string))
        tokens = list(tokens)
        return tokens
    
    def process_text(self):
        search_string = self.remove_urls(self.search_string)
        search_string = self.remove_punctuation(self.search_string)
        search_string = self.remove_stop_words(self.search_string)
        search_string = self.lemmatize(self.search_string)
        search_string = self.tokenize_text(self.search_string)
        return search_string
    
