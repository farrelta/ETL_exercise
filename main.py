from utils.extract import extract_all
from utils.transform import transform
from utils.load import save_csv

def run_etl():
    print("Starting ETL...")

    raw = extract_all(1, 50)
    df = transform(raw)
    save_csv(df, "products.csv")

    print("ETL Finished!")

if __name__ == "__main__":
    run_etl()
