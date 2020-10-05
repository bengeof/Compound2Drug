# autodockvina-spacesearcher
Python3 script downloading a protein by its PDB ID, a ligand by its CID from
PubChem database, preparing the structures and performing space-search docking using AutoDockVina.
# Installation
1. Clone this repository:
```
$ git clone https://github.com/Rmadeye/vina-merger.git
```
2. As most of required packages are present in **requirements.txt** file, using virtual environment is strongly recommended.
If virtualenv is not installed:
```
$ pip3 install virtualenv
```
Create virtual environment and install required packages
```
$ cd venvs_location
$ virtualenv vina-merger
$ source vina-merger/bin/activate
$ pip install -r requirements.txt
```
For proper functioning of the application, you also need to have:
* Installed AutoDockVina - download and install it from http://vina.scripps.edu/ or using linux package manager:
```
sudo apt-get install -y autodock-vina
```
* Installed with AutoDockTools - download and install it from http://mgltools.scripps.edu/.
The default location of the ADT should be /home/MGLTools-1.5.6. If you chose another location, change paths in ligand_prep.py and protein_prep.py files. 

## Usage
```
$ ./main.py -ip protein_entry -il ligand_entry
```
## Important

1. The program autobuilds the docking grid around the whole protein structure. If you have several units, it encompasses all of them.
2. The script uses all available CPU cores for calculations
3. The results from docking are available at results directory
4. All other directories have files generated at every step of preparation - if you are not sure about the result, check these files.
5. Feedback is more than welcomed! If you found the tool useful/irritating, send email to rafmadaj@gmail.com
