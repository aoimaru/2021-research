from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

import hashlib
import datetime
import json

JSON_FILE_PATH = "./JSON/"

class D2V():
    @staticmethod
    def do(training_data, name="default"):
        def toHash(word):
            hash_object = hashlib.sha256(word.encode()).hexdigest()
            return hash_object
        
        def toJson(training_data):
            objs = {}
            for td_key, td_value in training_data:
                td_hash = toHash(td_key)
                data = {
                    "location": to_key,
                    "token": td_value 
                }
                objs[toHash] = data

            current_time = str(datetime.datetime.now())
            file_path = JSON_FILE_PATH+"{}.json".format(current_time)
            try:
                with open(file_path, mode="w") as f:
                    json.dumps(objs, f, ensure_ascii=False, indent=4)
            except Exception as e:
                return False
            else:
                return True
            
        current_time = str(datetime.datetime.now())
        documents = [TaggedDocument(words=token, tags=[toHash(tag_name)]) for tag_name, token in training_data.items()]
        model = Doc2Vec(
            documents=documents, 
            min_count=1, 
            dm=1,
            window=5
        )
        model.save("./libs/D2Vs/{}-{}.model".format(name, current_time))
        Flag = toJson(training_data)




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



        