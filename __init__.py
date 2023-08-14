"""
Search Engine API interface
"""
import os
from .db_search import DBSearch as ds
from preprocessors.preprocessing import Text_Preprocessor

def search(search_string="", search_in=[], search_type=""):
    db_response = ""
    response = []
    search_tokens = Text_Preprocessor(search_string).process_text()
    db_response = ds().search(search_tokens)
    response.append(db_response)
    print(db_response)
    return response