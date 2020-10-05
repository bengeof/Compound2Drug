import numpy as np
import requests
import pandas as pd
import pickle

URL1 = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/cid/{}/cids/TXT"
URL2 = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsuperstructure/cid/{}/cids/TXT?identity_type=same_connectivity"
URL3 = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsubstructure/cid/{}/cids/TXT?identity_type=same_connectivity"

def get_cid_mapping():
    graphs = []
    cids_pbdids = pickle.load(open("./cids_pbdids.pkl", "rb"))
    for cids, _ in cids_pbdids:
        graphs.append(cids)
    return graphs

def get_list(cid):
    """
        input = cid: str
        output = cids: list (str)
    """
    r1 = requests.get(URL1.format(cid))
    cids1 = r1.content
    r2 = requests.get(URL2.format(cid))
    cids2 = r2.content
    r3 = requests.get(URL3.format(cid))
    cids3 = r3.content
    cids1 = [cid for cid in cids1.decode("utf-8").split("\n") if cid != ""]
    cids2 = [cid for cid in cids2.decode("utf-8").split("\n") if cid != ""]
    cids3 = [cid for cid in cids3.decode("utf-8").split("\n") if cid != ""]
    return sorted(list(set(cids1 + cids2 + cids3)))

def get_data(cid, filter_result=True):
    """
        input - cid: str
        output - pd.DataFrame, list
    """
    cids = get_list(cid)
    cids = [cid for cid in cids if cid != ""]
    connection = sqlite3.connect("./DB/drugs.db")
    df = pd.read_sql_query("SELECT * from drugs_interaction_processed", connection)
    df = df.drop(["index"], axis=1)
    if filter_result:
        return df.loc[df["cid"].isin(cids)], cids
    else:
        return df, cids
