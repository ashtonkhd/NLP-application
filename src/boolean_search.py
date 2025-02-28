from sklearn.feature_extraction.text import CountVectorizer

def initialize_binary_engine(documents):
    cv = CountVectorizer(lowercase=True, binary=True)
    _matrix = cv.fit_transform(documents).T.todense()

    return _matrix, cv
