import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv(
    "data/estate_data.csv",
    encoding="latin1"
)

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Daily sales
daily_sales = (
    df.groupby("Order Date")["Sales"]
      .sum()
      .reset_index()
)

# Create numerical day count
daily_sales["Days"] = (
    daily_sales["Order Date"]
    - daily_sales["Order Date"].min()
).dt.days

X = daily_sales[["Days"]]
y = daily_sales["Sales"]

model = LinearRegression()
model.fit(X, y)

# Predict next 30 days
future_days = pd.DataFrame({
    "Days": range(
        daily_sales["Days"].max() + 1,
        daily_sales["Days"].max() + 31
    )
})

predictions = model.predict(future_days)

print("\nNEXT 30 DAY FORECAST\n")

for day, value in enumerate(predictions, start=1):
    print(f"Day {day}: {value:.2f}")