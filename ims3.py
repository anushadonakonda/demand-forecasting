import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import os

# Step 1: Load the cleaned dataset
input_path = r'C:\\Users\\varsh\\OneDrive\\Desktop\\anusha\\grouped_inventory_data1.xlsx'
df = pd.read_excel(input_path)

# Step 2: Ensure the 'Order Date' is in datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Step 3: Group by ProductName and Order Date to aggregate quantities monthly
df['YearMonth'] = df['Order Date'].dt.to_period('M')
data_grouped = df.groupby(['ProductName', 'YearMonth']).agg({'Quantity': 'sum'}).reset_index()

# Step 4: Create output folder if it doesn't exist
output_folder = r'C:\\Users\\varsh\\OneDrive\\Desktop\\anusha\\forecasted_output'
os.makedirs(output_folder, exist_ok=True)

# Step 5: Initialize an empty DataFrame to hold all the forecasted data
forecasted_all = pd.DataFrame()

# Step 6: Loop through each unique product and apply the forecasting model
for product in data_grouped['ProductName'].unique():
    print(f"Forecasting for {product}...")

    # Filter data for the current product
    product_data = data_grouped[data_grouped['ProductName'] == product]

    # Check if there are enough data points (minimum 2)
    if len(product_data) < 2:
        print(f"Skipping {product} due to insufficient data points ({len(product_data)}).")
        continue

    # Prepare the data for Linear Regression: convert YearMonth to ordinal format (e.g., year + month)
    product_data['YearMonth_Ordinal'] = product_data['YearMonth'].dt.year * 12 + product_data['YearMonth'].dt.month

    # Define X (features) and y (target)
    X = product_data[['YearMonth_Ordinal']]  # Year-Month as feature
    y = product_data['Quantity']            # Quantity as target

    # Initialize the Linear Regression model
    model = LinearRegression()

    # Fit the model
    model.fit(X, y)

    # Generate forecast for the next 12 months (1 year)
    future_months = pd.date_range(start=product_data['YearMonth'].max().end_time + pd.Timedelta(days=1), periods=12, freq='MS')
    
    # Convert future_months to PeriodIndex and then extract year and month
    future_months_period = future_months.to_period('M')
    future_months_ordinal = future_months_period.year * 12 + future_months_period.month
    future_months_ordinal = future_months_ordinal.values.reshape(-1, 1)

    # Predict the quantities for the future months
    forecasted_quantities = model.predict(future_months_ordinal)

    # Create a DataFrame for the forecasted data
    forecasted_data = pd.DataFrame({
        'YearMonth': future_months,
        'Forecasted Quantity': forecasted_quantities,
        'ProductName': product
    })

    # Append to the final DataFrame
    forecasted_all = pd.concat([forecasted_all, forecasted_data])

    # Plot the historical data and the forecasted data
    plt.figure(figsize=(10, 6))
    plt.scatter(product_data['YearMonth'].dt.to_timestamp(), product_data['Quantity'], color='blue', label='Historical Data')
    plt.plot(future_months, forecasted_quantities, color='red', label='Forecasted Data')
    plt.title(f'Forecast for {product} Demand (Monthly)')
    plt.xlabel('Month')
    plt.ylabel('Quantity')
    plt.legend()
    plt.xticks(rotation=45)

    # Save the plot
    plot_path = os.path.join(output_folder, f'{product}_forecast_plot.png')
    plt.savefig(plot_path)
    plt.close()

# Step 7: Save the forecasted data to an Excel file
output_excel = os.path.join(output_folder, 'forecasted_demand_monthly_linear_regression.xlsx')
forecasted_all.to_excel(output_excel, index=False)

print(f"Forecasted data saved to {output_excel}")
