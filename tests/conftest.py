import os
import sys

import pytest
import spacy

this_file_path = os.path.abspath(__file__)
module_path = os.path.dirname(this_file_path + '/../src')
module_abs_path = os.path.abspath(module_path)
sys.path.append(module_abs_path)


@pytest.fixture
def sentence():
    return 'フクロウが鳴くと明日は晴れるので洗濯物を干せという意味'


@pytest.fixture
def nlp():
    nlp = spacy.load('ja_ginza')
    return nlp


@pytest.fixture
def span(nlp, sentence):
    return nlp(sentence).sents.__next__()


@pytest.fixture
def token(span):
    """フクロウ"""
    return span[0]
