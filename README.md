# DeepADRA2A

**DeepADRA2A** is a Deep Neural network-based model for prediction of Adrenergic α2a (ADRA2A) inhibitors using 
Simplified Molecular Input Line Entry System (SMILES) notation of Compounds.

## Contents

The files contained in this repository are as follows:
 * ``prediction_script.py``: Main script to run predictions
 * ``smiles.smi``: User input structures (multiple)
 * ``deepSSLmodel.h5``: DNN prediction model
 * ``data.csv``: Dataset
 * ``PaDEL``: Folder with an executable for feature calculation

## Requirements

* Install Java for running the PaDel subprocess

Install the following packages using the pip command (''pip install name_of_package = version'')
* Python (version 3.9) #pip install python
* Numpy (version 1.22)
* Pandas (version 1.5)
* Keras (version 2.11)
* Tensorflow (version 2.11)

## Usage

In order to run ADRA2A inhibitor predictions, save input structures as SMILES in a single file (e.g. ``smiles.smi``) or input SMILES notation.
 
1. Download this repository and ensure that all the files are present in the same folder when running the script.
2. Run ``prediction_script.py``. 
  ```bash
  python prediction_script.py <folder>
  ```
   If ``<folder>`` is not provided, the script runs in the current directory.
   A csv file (``...csv``) will be created in the folder where the script is run.
   A file containing the features generated by PaDEL will be also saved to disk (``PaDEL_features.csv``).
  
> **_NOTE:_** Remember to activate the corresponding conda environment before running the script, if applicable.
3. Prediction results will be saved in ``Predictions.csv`` which includes predicted class and associated probability

## Citation

If you use **.............** in your publication, consider citing the [paper](https://............):
```
@ARTICLE{,
AUTHOR={},   
TITLE={},      
JOURNAL={},      
VOLUME={},           
YEAR={},     
URL={},       
DOI={},      	
ISSN={}
}
```
