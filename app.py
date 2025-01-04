from flask import Flask, render_template, request
import pandas as pd
import altair as alt
import io

app = Flask(__name__)

# Load the data
def load_data():
    file_path = r'C:\Users\varsh\OneDrive\Desktop\anusha\forecasted_output\forecasted_demand_monthly_linear_regression.xlsx'
    df = pd.read_excel(file_path)
    df['YearMonth'] = pd.to_datetime(df['YearMonth'])
    return df

data = load_data()

@app.route('/', methods=['GET', 'POST'])
def index():
    product_names = data['ProductName'].unique()
    selected_product = product_names[0]  # Default selection

    if request.method == 'POST':
        selected_product = request.form.get('product')

    # Filter data based on selected product
    filtered_data = data[data['ProductName'] == selected_product]
    filtered_data = filtered_data.sort_values(by='YearMonth')

    # Create the Altair chart
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

    # Combine the chart and text
    chart_with_text = chart + text

    # Save chart as HTML
    chart_html = chart_with_text.to_html()

    return render_template('index.html', product_names=product_names, selected_product=selected_product, chart_html=chart_html)

if __name__ == '__main__':
    app.run(debug=True)
