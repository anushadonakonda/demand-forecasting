import streamlit as st
import pandas as pd
import altair as alt

# Load the data
def load_data():
    file_path = r'C:\Users\varsh\OneDrive\Desktop\anusha\forecasted_output\forecasted_demand_monthly_linear_regression.xlsx'
    df = pd.read_excel(file_path)
    df['YearMonth'] = pd.to_datetime(df['YearMonth'])
    return df

data = load_data()

# Streamlit app configuration
st.title("Forecasted Demand Visualization")
st.write("Select a product to view its monthly forecasted demand for the year.")

# Extract unique product names
product_names = data['ProductName'].unique()

# Dropdown to select product
selected_product = st.selectbox("Select a Product:", product_names)

# Filter data based on selected product
filtered_data = data[data['ProductName'] == selected_product]
filtered_data = filtered_data.sort_values(by='YearMonth')

# Create a bar chart
chart = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.X('yearmonth(YearMonth):T', title='Month', axis=alt.Axis(format='%b %Y')),
    y=alt.Y('Forecasted Quantity', title='Forecasted Quantity'),
    tooltip=['YearMonth', 'Forecasted Quantity']
).properties(
    title=f"Forecasted Demand for {selected_product}",
    width=700,
    height=400
)

# Add text labels on bars
text = alt.Chart(filtered_data).mark_text(
    align='center',
    baseline='middle',
    dx=0,  # Horizontal adjustment
    dy=-10,  # Vertical adjustment
    angle=315  # Makes the text slant (equivalent to -45 degrees)
).encode(
    x=alt.X('yearmonth(YearMonth):T'),
    y=alt.Y('Forecasted Quantity'),
    text=alt.Text('Forecasted Quantity:Q', format='.0f')  # Round off the values
)

# Display the chart with text labels
st.altair_chart(chart + text, use_container_width=True)
