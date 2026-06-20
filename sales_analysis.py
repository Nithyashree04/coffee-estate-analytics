import pandas as pd

df = pd.read_csv(
    "data/estate_data.csv",
    encoding="latin1"
)

sales_by_category = (
    df.groupby("Category")["Sales"]
      .sum()
      .sort_values(ascending=False)
)

print("\nSALES BY CATEGORY\n")
print(sales_by_category)