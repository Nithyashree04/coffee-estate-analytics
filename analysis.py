import pandas as pd

print("Loading dataset...")

df = pd.read_csv(
    "data/estate_data.csv",
    encoding="latin1"
)

print("\nFIRST 5 ROWS")
print(df.head())

print("\nDATASET SHAPE")
print(df.shape)

print("\nCOLUMN NAMES")
print(df.columns.tolist())