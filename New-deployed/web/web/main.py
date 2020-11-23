from run import *
from infer import *

if __name__ == "__main__":
    protein_ligand = str(input("Enter the CID: "))
    predictions = predict(protein_ligand)["predicted_pbdids"]
    print("The PDB IDs predicted by the Machine Learning/Deep Learning model are", predictions)
    
