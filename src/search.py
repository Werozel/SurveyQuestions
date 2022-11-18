import dataclasses
from functools import cache
from typing import List

import nltk
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from globals import morph, session_factory
from models.Question import Question
from src.normalizer import normalize_str


@dataclasses.dataclass
class RankedResult:
    score: float
    question: str


class Searcher:

    __tfidf_vect = TfidfVectorizer(
        analyzer='word',
        max_df=0.95,
        min_df=3,
        ngram_range=(1, 2),
        max_features=100_000,
        stop_words=nltk.corpus.stopwords.words('russian')
    )
    __lsa = TruncatedSVD(
        n_components=100,
        n_iter=1000
    )

    @staticmethod
    def print_closest(
            question_to_search: str,
            ranked_results: List[RankedResult],
            n: int = 10
    ):
        print(question_to_search, end="\n\n")
        for ranked_result in ranked_results[1: n]:
            print(ranked_result.score, ranked_result.question, sep=": ")

    @staticmethod
    def get_tfidf_results(question_to_search: str) -> List[RankedResult]:
        df = Searcher.__prepare_df(question_to_search)
        tfidf_model = Searcher.__get_tfidf_model(df)
        return Searcher.__rank_results(tfidf_model, df)

    @staticmethod
    def get_lsa_results(question_to_search: str) -> List[RankedResult]:
        df = Searcher.__prepare_df(question_to_search)
        tfidf_model = Searcher.__get_tfidf_model(df)
        lsa_model = Searcher.__lsa.fit_transform(tfidf_model)
        return Searcher.__rank_results(lsa_model, df)

    @staticmethod
    def __get_tfidf_model(df: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame.sparse.from_spmatrix(
            Searcher.__tfidf_vect.fit_transform(df['transformed'])
        )

    @staticmethod
    def __rank_results(
        model_df: pd.DataFrame,
        df: pd.DataFrame
    ) -> List[RankedResult]:
        cos_sim = cosine_similarity(model_df)
        enum_cos_sim = enumerate(cos_sim[0])
        enum_sort_cos_sim = sorted(enum_cos_sim, key=lambda x: x[1], reverse=True)
        return list(
            map(
                lambda x: RankedResult(x[1], df["raw"][x[0]]),
                enum_sort_cos_sim
            )
        )

    @staticmethod
    @cache
    def __prepare_df(question_to_search: str) -> pd.DataFrame:

        normalized_question = normalize_str(question_to_search, morph)

        with session_factory() as session:
            question_pair = [(question_to_search, normalized_question)] + \
                            session.query(Question.raw, Question.transformed).all()
        return pd.DataFrame(question_pair, columns=['raw', 'transformed'])

#%%
