# url_feature_extractor.py
import re, numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from tqdm import tqdm
from ML_components.utils import SUSPICIOUS_KEYWORDS, strip_scheme_www, remove_vietnamese_diacritics

class URLFeatureExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        feats = []
        for url in tqdm(X, desc="Trích feature URL", disable=True):
            url = strip_scheme_www(url)
            feats.append([
                len(url),
                url.count('.'),
                url.count('-'),
                int(bool(re.search(r'(\d{1,3}\.){3}\d{1,3}', url))),  # IP-in-URL
                sum(1 for w in SUSPICIOUS_KEYWORDS if w in url)
            ])
        return np.array(feats)
