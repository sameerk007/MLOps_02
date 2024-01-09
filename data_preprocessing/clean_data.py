# clean_data.py

import argparse
import pandas as pd
import os

def clean_data(input_path, output_path):
    print(f"Cleaning data from: {input_path} and saving to: {output_path}")

    
    # Load data
    df = pd.read_csv(os.path.join(input_path, 'outputs', 'california_housing.csv'))

    # Perform data cleaning (modify as needed)
    # ...
    df = df.dropna()

    # Save cleaned data
    output_path = os.path.join(output_path, 'outputs')  
    # Create the outputs folder if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    df.to_csv(os.path.join(output_path, 'cleaned_data.csv'), index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean California housing data.")
    parser.add_argument("--input_path", type=str, help="Path to the input folder.")
    parser.add_argument("--output_path", type=str, help="Path to the output folder.")

    args = parser.parse_args()

    if not args.input_path or not args.output_path:
        raise ValueError("Please provide both input_path and output_path.")

    clean_data(args.input_path, args.output_path)
