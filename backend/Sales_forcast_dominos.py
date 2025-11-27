import pandas as pd
import statsmodels.api as sm

# 1. Load dataset
df = pd.read_csv("pizza_sales.csv")
# 2. Convert order_date to datetime
df['order_date'] = pd.to_datetime(df['order_date'])
# 3. Ensure total_price is numeric
df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce')
# 4. Aggregate daily sales
daily_sales = df.groupby('order_date')['total_price'].sum().reset_index()
# 5. Create features
daily_sales['day_of_week'] = daily_sales['order_date'].dt.dayofweek  # 0=Mon, 6=Sun
daily_sales['month'] = daily_sales['order_date'].dt.month
# 6. Ensure predictors are numeric
X = daily_sales[['day_of_week', 'month']].apply(pd.to_numeric)
X = sm.add_constant(X)  # add intercept
y = pd.to_numeric(daily_sales['total_price'])
# 7. Run regression
model = sm.OLS(y, X).fit()
# 8. Print summary
print(model.summary())
# 8. Build results table
results = pd.DataFrame({
    "Variable": model.params.index,
    "Coefficient (B)": model.params.values,
    "Std. Error": model.bse.values,
    "t-value": model.tvalues.values,
    "p-value": model.pvalues.values
})

# 9. Round for readability
results = results.round(3)

print("Regression Results")
print(results.to_string(index=False))
