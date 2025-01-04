import pandas as pd

# Step 1: Load the data
df = pd.read_excel(r'C:\\Users\\varsh\\OneDrive\\Desktop\\anusha\\grouped_inventory_data1.xlsx')

# Step 2: Check column names (debugging)
print("Column Names:", df.columns)

# Step 3: Convert 'Order Date' column to datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Step 4: Group by Product and Order Date to Aggregate Quantity
product_data = df.groupby(['ProductName', 'Order Date']).agg({'Quantity': 'sum'}).reset_index()

# Debugging: Print unique products and the number of data points for each product
print("Unique Products in the dataset:", product_data['ProductName'].unique())

# Inspect the number of data points for each product
for product in product_data['ProductName'].unique():
    product_data_filtered = product_data[product_data['ProductName'] == product]
    print(f"Product: {product}, Data points: {len(product_data_filtered)}")
