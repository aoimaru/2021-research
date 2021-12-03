from gensim.models import word2vec
import datetime

class W2V(object):
    @staticmethod
    def execute(corpus, name="default"):
        current_time = str(datetime.datetime.now())
        model = word2vec.Word2Vec(corpus, size=200, min_count=20, window=5)
        model.save("./libs/delv/{}-{}.model".format(name, current_time))
