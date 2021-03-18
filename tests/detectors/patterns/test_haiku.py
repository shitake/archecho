import pytest
import spacy

from src.detectors.patterns.haiku import Counter, Haiku


def test_haiku(nlp):
    t = '明日の天気は雪'
    res = helper_make_res(nlp, t)
    assert res is None

    t = 'オムライス焼肉お寿司ピザカレー'
    res = helper_make_res(nlp, t)
    assert isinstance(res, spacy.tokens.span.Span)
    assert res.text == t

    t = '焼肉オムライスお寿司ピザカレー'
    res = helper_make_res(nlp, t)
    assert res is None

    t = 'フクロウが鳴くとあしたは晴れるので洗濯物を干せという意味'
    res = helper_make_res(nlp, t)
    assert isinstance(res, spacy.tokens.span.Span)
    assert res.text == 'フクロウが鳴くとあしたは晴れるので'


def helper_make_res(nlp, t):
    doc = nlp(t)
    h = Haiku(doc)
    return h.detect()


class TestCounter:
    def test__get_yomi_len(self, span, token):
        counter = Counter(span)

        res = counter._get_yomi_len(token)
        assert res == 4  # フクロウ

    def test__check_yomi_len(self, span):
        conditions = [5, 12, 17]

        counter = Counter(span)

        # 現在の読み長が 0
        counter.cur_yomi_len = 0
        counter._check_yomi_len()
        for c in conditions:
            assert not counter.conditions[c]

        # 現在の読み長が 5
        counter.cur_yomi_len = 5
        counter._check_yomi_len()
        assert counter.conditions[5]
        assert not counter.conditions[12]
        assert not counter.conditions[17]

        # 現在の読み長が 11
        counter.cur_yomi_len = 11
        counter._check_yomi_len()
        assert counter.conditions[5]
        assert not counter.conditions[12]
        assert not counter.conditions[17]

        # 現在の読み長が 12
        counter.cur_yomi_len = 12
        counter._check_yomi_len()
        assert counter.conditions[5]
        assert counter.conditions[12]
        assert not counter.conditions[17]

        # 現在の読み長が 17
        counter.cur_yomi_len = 17
        counter._check_yomi_len()
        assert counter.conditions[5]
        assert counter.conditions[12]
        assert counter.conditions[17]

    def test__confirm(self, span):
        counter = Counter(span)

        print(counter.conditions)

        assert not counter._confirm()

        counter.conditions[5] = True
        assert not counter._confirm()

        counter.conditions[12] = True
        assert not counter._confirm()

        counter.conditions[17] = True
        assert counter._confirm()
