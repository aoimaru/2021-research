from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

import hashlib
import datetimes

class D2V():
    @staticmethod
    def execute(tokens):
        hash_dict = {}
        hash_key = []
        training_docs = []
        for token in tokens:
            rs = " ".join(token)
            hash_object = hashlib.sha256(rs.encode()).hexdigest()
            hash_key.append(hash_object)
            if not hash_key in hash_dict:
                hash_dict[hash_key] = []
            hash_dict[hash_key].append(token)
            training_doc = TaggedDocument(
                words=token, 
                tags=[hash_object]
            )

            training_docs.append(training_doc)
        model = Doc2Vec(documents=training_docs, min_count=1, dm=0)


        