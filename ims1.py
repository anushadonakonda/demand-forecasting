import pandas as pd
import re

# Load the dataset
input_path = 'C:\\Users\\varsh\\OneDrive\\Desktop\\anusha\\Inventory_DataSet.xlsx'
data = pd.ExcelFile(input_path)

# Extract relevant columns from the first sheet
columns_of_interest = ['ProductName', 'Order Date', 'Quantity']
first_sheet = data.parse(data.sheet_names[0])
data_relevant = first_sheet[columns_of_interest]

# Preprocess the data
# Convert 'Order Date' to datetime format
data_relevant['Order Date'] = pd.to_datetime(data_relevant['Order Date'], errors='coerce')

# Drop rows with missing or invalid dates/quantities
data_cleaned = data_relevant.dropna(subset=['Order Date', 'Quantity']).copy()

# Remove numbering from ProductName (e.g., DOCSIS 3.1-1 to DOCSIS 3.1)
data_cleaned['ProductName'] = data_cleaned['ProductName'].apply(lambda x: re.sub(r'-\d+$', '', x))

# Group data by ProductName and Order Date
# Ensure all product names are grouped together
data_grouped = data_cleaned.groupby(['ProductName', 'Order Date']).sum().reset_index()

# Save the grouped data to a new Excel file
output_path = 'C:\\Users\\varsh\\OneDrive\\Desktop\\anusha\\grouped_inventory_data1.xlsx'
data_grouped.to_excel(output_path, index=False)

print(f"Grouped and cleaned data saved to {output_path}")
