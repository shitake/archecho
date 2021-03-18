from typing import Dict, List, Union

import ginza
import spacy

# TYPE
TOKEN = spacy.tokens.token.Token
SPAN = spacy.tokens.span.Span

nlp = spacy.load('ja_ginza')


class Haiku:

    first_break: int = 5
    second_break: int = 12
    third_break: int = 17

    def __init__(self, doc: spacy.tokens.doc.Doc):
        self.doc: spacy.tokens.doc.Doc = doc

    def detect(self) -> Union[None, SPAN]:
        for sent in self.doc.sents:
            for token in sent:
                if token.pos_ not in ['NOUN', 'VERB']:
                    continue

                counter = Counter(span=sent[token.i:])
                res = counter.run()

                if res:
                    return counter.result

        return None


class Counter:

    def __init__(
        self,
        span: SPAN
    ):
        self.span = span

        self.cur_yomi_len: int = 0
        self.conditions: Dict[int, bool] = {
            5: False,
            12: False,
            17: False
        }
        self.result: SPAN

    def run(self) -> bool:
        """文章がパターンと一致した場合、Trueを返す"""
        for token in self.span:
            # 現在の読み長をカウントアップ
            self.cur_yomi_len += self._get_yomi_len(token)

            # 読みの長さをチェックし、条件に一致する場合、状態をTrueにする
            self._check_yomi_len()

            # 現時点で条件を満たすかチェック
            if self._confirm():
                self._make_result(token)
                return True

        return False

    def _get_yomi_len(self, token) -> int:
        yomi = ginza.reading_form(token)
        return len(yomi)

    def _check_yomi_len(self):
        k: int
        state: bool
        for k, state in self.conditions.items():
            if state:
                continue

            if self.cur_yomi_len == k:
                self.conditions[k] = True
                break

    def _confirm(self):
        for v in self.conditions.values():
            if not v:
                return False
        return True

    def _make_result(self, token: TOKEN) -> None:
        self.result = self.span[:token.i + 1]
