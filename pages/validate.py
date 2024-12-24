import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
from models.black_scholes_model import BlackScholesAnalyzer

def validate_csv_structure(df):
    """
    Validates if the uploaded CSV has the required columns and data types.
    Returns a tuple of (is_valid, error_message).
    """
    required_columns = {
        'Date': str,
        'Stock_Price': float,
        'Volatility': float,
        'Risk_Free_Rate': float,
        'Strike': float,
        'Days_To_Maturity': int,
        'Time_To_Maturity': float
    }

    # Check if all required columns are present
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"

    # Attempt to convert columns to required types
    try:
        for col, dtype in required_columns.items():
            if col == 'Date':
                pd.to_datetime(df[col])
            else:
                df[col] = df[col].astype(dtype)
        return True, "Data structure is valid"
    except Exception as e:
        return False, f"Error converting data types: {str(e)}"

def process_uploaded_file(uploaded_file):
    """
    Process the uploaded CSV file and return the analyzed data.
    """
    try:
        # Read the CSV into a temporary file
        temp_file = io.BytesIO(uploaded_file.getvalue())
        temp_file_path = "temp_options_data.csv"
        with open(temp_file_path, 'wb') as f:
            f.write(temp_file.getvalue())

        # Initialize analyzer with temporary file
        analyzer = BlackScholesAnalyzer(temp_file_path)

        # Load and process data
        analyzer.load_data()
        analyzer.calculate_option_prices()
        analyzer.calculate_greeks()

        return analyzer.data

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

def create_price_distribution_plot(data):
    """Create a distribution plot for option prices."""
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=data['Call_Price'],
        name='Call Options',
        opacity=0.75,
        nbinsx=30
    ))

    fig.add_trace(go.Histogram(
        x=data['Put_Price'],
        name='Put Options',
        opacity=0.75,
        nbinsx=30
    ))

    fig.update_layout(
        title='Distribution of Option Prices',
        xaxis_title='Option Price',
        yaxis_title='Count',
        barmode='overlay'
    )

    return fig

def create_greeks_scatter_plot(data, greek_col, stock_price_col='Stock_Price'):
    """Create a scatter plot for analyzing Greeks against stock price."""
    fig = px.scatter(
        data,
        x=stock_price_col,
        y=greek_col,
        color='Days_To_Maturity',
        title=f'{greek_col} vs Stock Price',
        labels={stock_price_col: 'Stock Price', greek_col: greek_col}
    )
    return fig

def create_moneyness_plot(data):
    """Create a scatter plot showing option prices vs moneyness."""
    data['Moneyness'] = data['Stock_Price'] / data['Strike']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['Moneyness'],
        y=data['Call_Price'],
        mode='markers',
        name='Call Options',
        marker=dict(size=6)
    ))

    fig.add_trace(go.Scatter(
        x=data['Moneyness'],
        y=data['Put_Price'],
        mode='markers',
        name='Put Options',
        marker=dict(size=6)
    ))

    fig.update_layout(
        title='Option Prices vs Moneyness',
        xaxis_title='Moneyness (S/K)',
        yaxis_title='Option Price'
    )

    return fig

def display_data_requirements():
    """Display the requirements for the CSV file format."""
    st.info("CSV File Requirements:")
    st.write("""
    Your CSV file should contain the following columns:
    - Date: Date of the option data
    - Stock_Price: Current price of the underlying stock
    - Volatility: Volatility of the underlying asset
    - Risk_Free_Rate: Risk-free interest rate (as a decimal)
    - Strike: Strike price of the option
    - Days_To_Maturity: Number of days until option expiration
    - Time_To_Maturity: Time to maturity in years (days/365)

    Example format:
    ```
    Date,Stock_Price,Volatility,Risk_Free_Rate,Strike,Days_To_Maturity,Time_To_Maturity
    2024-01-01,100.75,0.2,0.059,90.68,30,0.119
    ```
    """)

def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(
        page_title="Black-Scholes Analysis Dashboard",
        page_icon="📈",
        layout="wide"
    )

    st.title("Black-Scholes Option Analysis Dashboard")
    st.write("Upload your options data CSV file to analyze it using the Black-Scholes model.")

    # File upload section
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is None:
        display_data_requirements()
        return

    # Read and validate the uploaded file
    try:
        preview_df = pd.read_csv(uploaded_file)
        is_valid, error_message = validate_csv_structure(preview_df)

        if not is_valid:
            st.error(error_message)
            display_data_requirements()
            return

        # Process the file if valid
        data = process_uploaded_file(uploaded_file)

        if data is None:
            return

        # Create tabs for different visualizations
        tab1, tab2, tab3, tab4 = st.tabs([
            "Overview",
            "Option Prices",
            "Greeks Analysis",
            "Data Explorer"
        ])

        with tab1:
            st.header("Dataset Overview")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Options", len(data))
            with col2:
                st.metric("Avg Call Price", f"${data['Call_Price'].mean():.2f}")
            with col3:
                st.metric("Avg Put Price", f"${data['Put_Price'].mean():.2f}")

            st.subheader("Summary Statistics")
            st.dataframe(data.describe())

        with tab2:
            st.header("Option Prices Analysis")

            # Price distribution plot
            st.plotly_chart(create_price_distribution_plot(data))

            # Moneyness plot
            st.plotly_chart(create_moneyness_plot(data))

        with tab3:
            st.header("Greeks Analysis")

            # Select which Greek to analyze
            greek_option = st.selectbox(
                "Select Greek to Analyze",
                ["Call_Delta", "Put_Delta", "Gamma", "Vega", "Call_Theta", "Put_Theta"]
            )

            # Create and display the selected Greek's plot
            st.plotly_chart(create_greeks_scatter_plot(data, greek_option))

            # Add explanatory text based on selected Greek
            greek_explanations = {
                "Call_Delta": "Delta measures the rate of change of the option price with respect to the underlying asset price. For call options, delta is positive and ranges from 0 to 1.",
                "Put_Delta": "Put option delta is negative and ranges from -1 to 0, representing the rate of change of the put option price with respect to the underlying asset price.",
                "Gamma": "Gamma measures the rate of change of delta with respect to the underlying asset price. It represents the curvature of the value function.",
                "Vega": "Vega measures the sensitivity of the option price to changes in volatility. Both calls and puts have positive vega.",
                "Call_Theta": "Theta measures the sensitivity of the call option price to changes in time to expiration (time decay).",
                "Put_Theta": "Theta for put options, measuring the rate of change of the put option price with respect to time."
            }

            st.write(greek_explanations.get(greek_option, ""))

        with tab4:
            st.header("Data Explorer")
            st.write("Explore the raw data and calculated values:")

            # Add column filters
            cols_to_show = st.multiselect(
                "Select columns to display",
                data.columns.tolist(),
                default=['Date', 'Stock_Price', 'Strike', 'Call_Price', 'Put_Price']
            )

            # Display filtered dataframe
            if cols_to_show:
                st.dataframe(data[cols_to_show])

            # Add download button
            st.download_button(
                label="Download Analysis Results as CSV",
                data=data.to_csv(index=False).encode('utf-8'),
                file_name="black_scholes_analysis_results.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        display_data_requirements()

if __name__ == "__main__":
    main()
