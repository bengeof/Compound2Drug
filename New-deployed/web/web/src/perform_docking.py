import os, shutil
from biopandas.pdb import PandasPdb
from src.plip_extension import ObtainInteractionsFromComplex


class VinaDocker:

    def __init__(self, ligentry: str, protentry: str, protein_pdbqt: str, ligand_pdbqt: str, dir: str):
        self.protein = protein_pdbqt + '.pdbqt'
        self.protpdb = protentry + '.pdb'
        self.protname = os.path.basename(self.protein)
        self.ligand = ligand_pdbqt + '.pdbqt'
        self.ligname = os.path.basename(self.ligand)
        self.tmpdir = dir
        self.docklog = './results/' + protentry + '_' + ligentry + '_docking.log'
        self.dockfile =  './results/' + protentry + '_' + ligentry + '.out'
        self.complex_name = protentry + '_' + ligentry + '_cplx.pdb'

    def dock_merge_plip(self):
        df = PandasPdb().read_pdb(self.tmpdir + '/' + self.protpdb)  # opens protein to calculate grid
        minx = df.df['ATOM']['x_coord'].min()
        maxx = df.df['ATOM']['x_coord'].max()
        cent_x = round((maxx + minx) / 2, 2)
        size_x = round(abs(maxx - minx) + 3, 2)
        miny = df.df['ATOM']['y_coord'].min()
        maxy = df.df['ATOM']['y_coord'].max()
        cent_y = round((maxy + miny) / 2, 2)
        size_y = round(abs(maxy - miny) + 3, 2)
        minz = df.df['ATOM']['z_coord'].min()
        maxz = df.df['ATOM']['z_coord'].max()
        cent_z = round((maxz + minz) / 2, 2)
        size_z = round(abs(maxz - minz) + 3, 2)
        assert (type(cent_x) != None), "Protein structure is damaged"
        assert (type(cent_y) != None), "Protein structure is damaged"
        assert (type(cent_z) != None), "Protein structure is damaged"


        print("Center point of docking grid for {} is as follows: "
              "x: {}, y: {}, z: {}".format(self.protein, size_x, size_y, size_z))
        print("Sizes of docking grid are as follows:"
              "x: {}, y: {}, z: {}".format(cent_x, cent_y, cent_z))
        os.system(
            'vina --receptor {} --ligand {} --center_x {} --center_y {} --center_z {} --size_x {} --size_y {} --size_z {} --log {} --out {}'.format(
                self.protein,
                self.ligand,
                cent_x,
                cent_y,
                cent_z,
                size_x,
                size_y,
                size_z,
                self.docklog,
                self.dockfile
            ))
        """Postprocessing of docking files"""

        df.df['ATOM']['segment_id'].replace(r'.{1,}', '', regex=True, inplace=True) # Clean pdbqt inheritance
        df.df['ATOM']['blank_4'].replace(r'.{1,}', '', regex=True, inplace=True)
        docking_output_df = PandasPdb().read_pdb(self.dockfile)
        docking_output_df.df['HETATM'].drop_duplicates(subset='atom_number', keep='first', inplace=True)  # extract first model
        docking_output_df.df['HETATM']['segment_id'].replace(r'.{1,}', '', regex=True, inplace=True)
        docking_output_df.df['HETATM']['blank_4'].replace(r'.{1,}', '', regex=True, inplace=True)  # clean pdbqt inheritance
        df.df['ATOM'] = df.df['ATOM'].append(docking_output_df.df['HETATM'], ignore_index=True) # merges the files
        df.to_pdb(path = self.complex_name,
                  records=['ATOM','HETATM'],
                  gz = False,
                  append_newline=True)
        try:
            ObtainInteractionsFromComplex(self.complex_name).connect_retrieve() # PLIP analysis
        except:
            pass
        shutil.move(self.complex_name, './results')
