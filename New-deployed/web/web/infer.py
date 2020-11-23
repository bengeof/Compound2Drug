import tensorflow as tf
from models import *
import pickle
from api import *
from collections import Counter
from gensim.models import KeyedVectors
import pickle
import warnings
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

cid_mapping = get_cid_mapping()

graph_mapping = {}

def most_frequent(List):
    return max(set(List), key=List.count)

def in_graph(cid):
    return True in [cid in mapping for mapping in cid_mapping]

def get_graph_num(cid):
    graph_index = [cid in mapping for mapping in cid_mapping].index(True)
    graph_mapping[cid] = graph_index
    return graph_index

def keep_getting_list(cid):
    cids = get_list(cid)
    cids = list(filter(in_graph, cids))
    votes = list(map(get_graph_num, cids))

    return cids, votes

def predict(cid):
    cids = [cid]
    votes = []
    # chose 10 randomly
    while len(cids) < 10:
        for cid in cids:
            cids_, votes_ = keep_getting_list(cid)
            cids += cids_
            votes += votes_
            if len(cids) >= 10:
                break
    cids = cids[1:]
    graph_num = most_frequent(votes)
    condensed_cids = [cid for cid in cids if cid in graph_mapping if graph_mapping[cid] == graph_num]
    
    n2v = KeyedVectors.load_word2vec_format(f"./vectors/wheel_mode_graph-{graph_num}.bin")
    X = np.array([n2v[cid] for cid in condensed_cids]).reshape(-1, 32)
    cids_pbdids = pickle.load(open("./cids_pbdids.pkl", "rb"))
    pbdid_dict = cids_pbdids[graph_num][1]

    if graph_num > 4:
        model = pickle.load(open(f"./trained_models/small_graphs/train_set{graph_num}/Regressor_model.sav", "rb"))
        # yhat = np.array([np.where(row == 1) for row in model.predict(X)])
        yhat = np.argmax(model.predict(X), 1)
    else:
        model = tf.keras.models.load_model(f"./trained_models/big_graphs/graph{graph_num}-ep50.h5")
        yhat = model.predict(X)
        yhat = np.argmax(yhat, 1)
        pbdids = [pbdid_dict[pbdid] for pbdid in sorted(yhat.tolist(), key = lambda ele: yhat.tolist().count(ele))][::-1]
        pbdids = [tup[1].lower() for tup in enumerate(pbdids) if tup[0] == pbdids.index(tup[1])]
 
    return {
        "input_cid": cid,
        "residing_graph": graph_num,
        "highest_match": pbdid_dict[most_frequent(yhat.tolist())],
        "predicted_pbdids": pbdids
    }
