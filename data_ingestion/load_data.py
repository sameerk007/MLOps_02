# load_data.py
import argparse
from sklearn.datasets import fetch_california_housing
import pandas as pd
import os
from azureml.core import Run

def load_data(output_path):
    print(f"Loading data and saving to: {output_path}")

    # Load data
    data = fetch_california_housing()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target

    # Save data to the output folder specified in the argument
    output_folder = os.path.join(output_path, 'outputs')
    os.makedirs(output_folder, exist_ok=True)
    df.to_csv(os.path.join(output_folder, 'california_housing.csv'), index=False)

    # Log the output folder as the result of the step
    run = Run.get_context()
    run.log('output_folder', output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load California housing data.")
    parser.add_argument("--output_path",required=True, type=str, help="Path to the output folder.")

    args = parser.parse_args()

    load_data(args.output_path)
