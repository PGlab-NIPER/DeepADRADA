#!/usr/bin/env python3

""" 
DeepADRA2A is a Deep Neural Network-based tool to predict Adrenergic α2a (ADRA2A) inhibitors.

It calculates descriptors using PaDEL and uses them to predict inhibitors for ADRA2A with a trained DNN model. 

The compound's SMILES must be in the .smi file in the same folder.
Data (data.csv), model (DeePredmodel.h5), and PaDEL folder must be in the same folder, too. 

Prediction results (class and probability) will be saved in Predictions.csv

Edited by Anju Sharma
"""

import os
import sys
import pandas as pd  
import numpy as np
import subprocess
from sklearn.preprocessing import StandardScaler
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder



# Create function to get predictions using trained model
def adra2a(input_ar: pd.DataFrame) -> np.ndarray:
    """Function to predict activity for a set
    set of samples with PaDEL features.

    Args:
        input_ar (pd.DataFrame): PaDEL Features for compounds

    Returns:
        np.ndarray: class (1 inhibitor; 0 non-inhibitor)
    """
    # Encoding class labels
    A = ['Inhibitor', 'Noninhibitor']
    encoder = LabelEncoder()
    encoder.fit(A)
    encoded_Y = encoder.transform(A)
    
    # Load training data and scale it 
    ar_data = pd.read_csv(os.path.join(path, "data.csv"), header=None)
    scaler = StandardScaler()  
    ar_data = scaler.fit_transform(ar_data)  
   
   # Transform user data to numpy to avoid conflict with names
    ar_user_input = scaler.transform(input_ar.to_numpy())
    
    # Load model
    loaded_model = load_model(os.path.join(path, "deepSSLmodel.h5")) 
    print("Model loaded")
   
   # Get predictions for user input
    prediction = loaded_model.predict(ar_user_input)

    a = prediction[:,1]
    b = prediction[:,0]
    c=[]
    for i in range(len(a)):
        if a[i] >= b[i]:
            c.append(a[i])
        else:
            c.append(b[i])
    
    prediction = encoder.inverse_transform(prediction.argmax(axis=1))
   
    return prediction, c
    

# Create the main function to run descriptor calculation and predictions 

def run_prediction(folder: str) -> None:
    """Function to calculate descriptors (using PaDEL) and to generate
    predictions of Adrenergic α2a (ADRA2A) inhibitors/ noninhibitors for a set of compounds (SMILES).

    Args:
        folder (str): Folder to search for ".smi" file (multiple structures)

    Returns:
        CSV file with resulting Adrenergic α2a (ADRA2A) activity class (1 inhibitor; 0 noninhibitor)
    """
    # Define command for PaDEL
    padel_cmd = [
        'java', '-jar', 
        os.path.join(path, 'PaDEL-Descriptor/PaDEL-Descriptor.jar'),
        '-descriptortypes', 
        os.path.join(path, 'PaDEL-Descriptor/descriptors.xml'), 
        '-dir', folder, '-file', folder + '/PaDEL_features.csv', 
        '-2d', '-fingerprints', '-removesalt', '-retainorder', '-detectaromaticity', 
        '-standardizenitro']
    # Calculate features
    subprocess.call(padel_cmd)
    print("Features calculated")
    # Create Dataframe for calculated features
    input_ar =pd.read_csv(folder + "/PaDEL_features.csv")
    input_ar.fillna(0, inplace=True)
    # Store name of each sample
    names = input_ar['Name'].copy()
    input_ar = input_ar.drop(['Name','BCUTw-1l','BCUTw-1h','BCUTc-1l','BCUTc-1h','BCUTp-1l','BCUTp-1h','SCH-3','SCH-4','SCH-5','SCH-6','SCH-7','VCH-3','VCH-4','VCH-5','VCH-6','VCH-7','SC-3','SC-4','SC-5','SC-6','VC-3','VC-4','VC-5','VC-6','SPC-4','SPC-5','SPC-6','VPC-4','VPC-5','VPC-6','SP-0','SP-1','SP-2','SP-3','SP-4','SP-5','SP-6','SP-7','ASP-0','ASP-1','ASP-2','ASP-3','ASP-4','ASP-5','ASP-6','ASP-7','VP-0','VP-1','VP-2','VP-3','VP-4','VP-5','VP-6','VP-7','AVP-0','AVP-1','AVP-2','AVP-3','AVP-4','AVP-5','AVP-6','AVP-7','VABC','PubchemFP880'], axis=1)
    # Run predictions
    pred,c = adra2a(input_ar)    
    
    # Create Dataframe with results
    res = pd.DataFrame(names)
    res['Predicted_class'] = pred
    res['Probability'] = c
    # Save results to csv
    res.to_csv('Predictions.csv', index=False)
    
    return None
    

# Run script
if __name__ == "__main__":
    # Define current directory
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = os.getcwd()
    # Verify existence of file with SMILES
    exists = [fname for fname in os.listdir(path) if fname.endswith(".smi")]
    if exists:
        # Get predictions
        run_prediction(path)        
    else:
        raise FileNotFoundError("Input File NOT found")
