
import pandas as pd

def load_data(file_path):
    """
    Loads the credit card fraud detection dataset from a CSV file.

    Args:
        file_path (str): The path to the creditcard.csv file.

    Returns:
        pandas.DataFrame: The loaded dataset.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Dataset loaded successfully from {file_path}. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the dataset: {e}")
        return None

if __name__ == "__main__":
    # Example usage: Assumes creditcard.csv is in the ../data/ directory relative to src/
    data_path = "../data/creditcard.csv"
    credit_card_df = load_data(data_path)
    if credit_card_df is not None:
        print("First 5 rows of the dataset:")
        print(credit_card_df.head())
        print("Dataset Info:")
        credit_card_df.info()
