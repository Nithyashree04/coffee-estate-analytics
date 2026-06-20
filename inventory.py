import pandas as pd

df = pd.read_csv(
    "data/estate_data.csv",
    encoding="latin1"
)

inventory = (
    df.groupby("Category")["Quantity"]
      .sum()
      .sort_values(ascending=False)
)

print("\nINVENTORY ANALYSIS\n")
print(inventory)