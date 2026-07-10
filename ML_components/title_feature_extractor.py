# title_feature_extractor.py
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from tqdm import tqdm

from ML_components.utils import (
    strip_scheme_www,
    SUSPICIOUS_KEYWORDS,
    remove_vietnamese_diacritics,
)


def dedup_sub_keywords(hit_words):
    """Loại bỏ các từ khoá là phần con của từ khoá dài hơn đã match."""
    hit_words = sorted(hit_words, key=len, reverse=True) 
    unique_hits = []
    for w in hit_words:
        if not any(w in longer for longer in unique_hits):
            unique_hits.append(w)
    return unique_hits

class TitleFeatureExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, title_mapping: dict):
        self.title_mapping = title_mapping or {}

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        features = []
        for url in tqdm(X, desc="Title features", disable=True):
            clean = strip_scheme_www(url)
            title_raw = self.title_mapping.get(clean, "") or ""
            title_norm = remove_vietnamese_diacritics(title_raw.lower())

            # Tìm các từ khoá có trong title
            matched_keywords = [w for w in SUSPICIOUS_KEYWORDS if w in title_norm]
            filtered_keywords = dedup_sub_keywords(matched_keywords)
            kw_cnt = len(filtered_keywords)

            features.append([len(title_norm), kw_cnt])
            print(f"Title chuẩn hóa: \"{title_norm}\" → KW hits: {kw_cnt}")
        return np.array(features)