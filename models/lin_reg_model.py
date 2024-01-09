#lin_reg_model.py


""" Use of Linear Regression model"""

import os
import argparse
import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

from azureml.core import Run

def lin_reg_model(input_path, output_path):
    
    # Load data
    df = pd.read_csv(os.path.join(input_path,'outputs','cleaned_data.csv'))
    # Split data into features and target
    X = df.drop('target', axis=1)
    y = df['target']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Create a linear regression model
    model = LinearRegression()

    # Fit the model to the training data
    model.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Log metrics using Azure ML
    run = Run.get_context()
    run.log('mse', mse)
    run.log('r2', r2)
    


    # Save cleaned data
    output_path = os.path.join(output_path, 'outputs')  
    # Create the outputs folder if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    # pickle.dump(model, open(os.path.join(output_path, 'model.pkl'), 'wb')) #Saving the model
    pickle.dump(model,open('outputs/lin_reg_model.pkl', 'wb')) #Saving the model

   


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean California housing data.")
    parser.add_argument("--input_path", type=str, help="Path to the input folder.")
    parser.add_argument("--output_path", type=str, help="Path to the output folder.")

    args = parser.parse_args()

    if not args.input_path or not args.output_path:
        raise ValueError("Please provide both input_path and output_path.")

    lin_reg_model(args.input_path, args.output_path)