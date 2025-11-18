import pandas as pd

def save_csv(df: pd.DataFrame, filename="products.csv"):
    df.to_csv(filename, index=False)
    print(f"Saved to {filename}")
