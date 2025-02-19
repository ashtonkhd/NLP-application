from sklearn.feature_extraction.text import CountVectorizer

def initialize_ranked_engine(documents):
    cv = CountVectorizer(lowercase=True, binary=False)
    _matrix = cv.fit_transform(documents).T.todense()

    return _matrix, cv
