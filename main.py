from run import *
from infer import *

if __name__ == "__main__":
    protein_ligand = str(input("Enter the CID: "))
    predictions = predict(protein_ligand)["predicted_pbdids"]
    print("The PDB IDs predicted by the Machine Learning/Deep Learning model are", predictions)
    for pdbid in predictions:
        try:
            try:
                execute([pdbid], [protein_ligand])
            except:
                execute([pdbid.upper()], [protein_ligand])
        except:
             pass
