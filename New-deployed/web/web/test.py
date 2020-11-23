import sys
from infer import *
import numpy as np
from src import protein_prep, ligand_prep, perform_docking
import os, tempfile
if __name__ == "__main__":
    try:
        cid = str(sys.argv[1])
    except:
        cid = "2000"

        #unwanted code
    cid = input("Enter Cid :  ")
    predictions = predict(cid)
    #print("The Cid's Based on Neural Network Prediction are :  ")
    
    print(predictions)
    print(type(predictions))
    np.save("list.npy",predictions)
    li_g=predictions['highest_match']
    print("PDB IDs predicted by the Machine Learning/Deep Learning model are  ",li_g)
            
    home = os.path.expanduser("~")


    def execute(PDB_list: list, CID_list: list):
        assert (os.path.isdir(
            home + '/MGLTools-1.5.6')), "AutoDockTools not found! Script stopped"  # check if mgltools are present
        for CID_entry in CID_list:
            with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmpdir:
                ligand_prep.LigandPreparer(CID_entry, dir=tmpdir).prepare_ligand()
                for PDB_entry in PDB_list:
                    protein_prep.ProteinPreparer(PDB_entry, dir=tmpdir).prepare_protein()
                    perform_docking.VinaDocker(protentry=PDB_entry,
                                            ligentry=CID_entry,
                                            protein_pdbqt=tmpdir + '/' + PDB_entry,
                                            ligand_pdbqt=tmpdir + '/' + CID_entry,
                                            dir=tmpdir
                                            ).dock_merge_plip()   
    
    ligand = [] ; ligand.append(str(cid))
    proteins = [] ; proteins.append(str(li_g))
    execute(proteins,ligand)
