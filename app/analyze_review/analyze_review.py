import sys
# sys.path.append('/Users/brettcastellanos/galvanize/craft_beer_ratings/src')
import re
import pickle
import pandas as pd
import numpy as np
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer


def main():
    print('Nothing to see here. Import me instead.')
    return 0

class ReviewProcessor:
    def __init__(self):
        self.stopwords = set(stopwords.words('english'))
        self.punctuation = '.!,;:\'"\(\)\[\]\n/'
        self.rgx = re.compile('[{}]'.format(self.punctuation))
        self.reviews_df = pd.read_csv(
            'data/1-clean/clean_reviews.csv'
            )
        with open(
            'models/1-nmf/TF-IDF-Vectorizer.pkl',
            'rb'
        ) as p:
            self.tfidf_vectorizer = pickle.load(p)
        self.stemmer = LancasterStemmer()
        with open(
            '/models/1-nmf/NMF.pkl',
            'rb'
        ) as p:
            self.NMF = pickle.load(p)
        with open(
            '/models/1-nmf/W.pkl',
            'rb'
        ) as p:
            self.W = pickle.load(p)

        return None

    def get_top_ten_reviews(self, topic_idx):
        top_reviews_idx = np.argsort(self.W[:, topic_idx])[-1:-11:-1]
        return self.reviews_df.iloc[top_reviews_idx]

    def get_topic_vector(self, tf_idf_vector):
        """Given a tf_idf_vector, return the topic vector.
        """
        topic_vector = tf_idf_vector.dot(self.NMF.components_.T)
        return topic_vector

    def get_tfidf_vector(self, review):
        """Given a review string, returns the TF-IDF Vector for that review.
        """
        return self.tfidf_vectorizer.transform([review])

    def clean_review(self, review):
        """Given a review, return a review ready to be vectorized.
        """
        clean_review = self.remove_punctuation(review)
        clean_review = self.remove_stopwords(clean_review)
        split_words = clean_review.split()
        stemmed_review = ' '.join(
            [self.stemmer.stem(word) for word in split_words]
        )
        return stemmed_review

    def remove_punctuation(self, review):
        """Given a review, return the review without punctuation.
        """
        return self.rgx.sub(' ', review.lower())

    def remove_stopwords(self, review):
        """Given a review, return the review minus stopwords.
        """
        split_words = review.split()

        return ' '.join(
            [word for word in split_words if word not in self.stopwords]
            )
