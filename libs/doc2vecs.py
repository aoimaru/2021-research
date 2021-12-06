from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

import hashlib
import datetime

class D2V():
    



    @staticmethod
    def execute_old(tokens, name="default"):
        hash_dict = {}
        hash_key = []
        training_docs = []
        current_time = str(datetime.datetime.now())
        for token in tokens:
            # print("token:", token)
            rs = " ".join(token)
            hash_object = hashlib.sha256(rs.encode()).hexdigest()
            hash_key.append(hash_object)
            if not hash_object in hash_dict:
                hash_dict[hash_object] = []
            hash_dict[hash_object].append(token)
            training_doc = TaggedDocument(
                words=token, 
                tags=[hash_object]
            )

            training_docs.append(training_doc)
        model = Doc2Vec(documents=training_docs, min_count=1, dm=0)
        model.save("./libs/D2Vs/{}-{}.model".format(name, current_time))
        return model, hash_dict, hash_key
    


    @staticmethod
    def execute_sec(tokens):
        hash_dict = {}
        hash_key = []
        training_docs = []
        for token in tokens:
            # print("token:", token)
            rs = " ".join(token)
            hash_object = hashlib.sha256(rs.encode()).hexdigest()
            hash_key.append(hash_object)
            if not hash_object in hash_dict:
                hash_dict[hash_object] = []
            hash_dict[hash_object].append(token)
            training_doc = TaggedDocument(
                words=token, 
                tags=[hash_object]
            )

            training_docs.append(training_doc)
        model = Doc2Vec(documents=training_docs, min_count=1, dm=0)
        return model, hash_dict, hash_key



        