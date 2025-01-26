import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
from datetime import datetime
import io
from models.black_scholes_model import BlackScholes, BlackScholesAnalyzer
import streamlit as st
import plotly.express as px
import pandas as pd

def validate_csv_structure(df):
    '''
    Validate if the csv file if it has all the required columns and correct data types.
    Returns tuple (is_valid, error_message)
    '''

    required_columns = {
        'Date':str,
        'Stock_Price':float,
        'Volatility':float,
        'Risk_Free_Rate':float,
        'Strike': float,
        'Days_To_Maturity': int,
        'Time_To_Maturity': float
    }

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"

    # Verify data types can be converted properly
    try:
        for col, dtype in required_columns.items():
            if col == 'Date':
                pd.to_datetime(df[col])
            else:
                df[col] = df[col].astype(dtype)
        return True, "Data Structure is Valid"
    except Exception as e:
        return False, f"Error converting data types: {str(e)}"

def create_price_distribution_plot(data):
    """
    Create an overlaid histrogram of call and put prices
    """
    fig = go.Figure()

    # Call options distribution
    fig.add_trace(go.Histogram(
        x=data['Call_Price'],
        name='Call Options',
        opacity=0.75,
        nbinsx=30,
        histnorm='probability'
    ))

    # put options distribution
    fig.add_trace(go.Histogram(
        x=data['Call_Price'],
        name='Call Options',
        opacity=0.75,
        nbinsx=30,
        histnorm='probability'
    ))

    fig.update_layout(
        title='Distribution of Option Prices',
        xaxis_title='Option Price',
        yaxis_title='Probabilty',
        barmode='overlay'
    )

    return fig

def create_greeks_scatter_plot(data,greek_col):
    """Create greeks scatter plot with the stock price"""
    fig = px.scatter(
        data,
        x='Stock_Price',
        y=greek_col,
        color="Days_To_Maturity",
        title=f'{greek_col} vs Stock Price',
        labels={'Stock_Price':'Stock Price',greek_col:greek_col},
        trendline="lowess"
    )

    fig.update_layout(
        showlegend=True,
        coloraxis_colorbar_title="Days to Maturity"
    )

    return fig

def create_moneyness_plot(data):
    """Create a visualization of option prices vs moneyess ratio"""
    data["Moneyess"] = data['Stock_Price']/data['Strike']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['Moneyess'],
        y=data['Call_Price'],
        mode='markers',
        name='Call Option',
        marker=dict(
            size = 6,
            color=data['Days_To_maturity'],
            colorscale='Virdis',
            showscale=True
        )
    ))
    fig.add_trace(go.Scatter(
        x=data['Moneyess'],
        y=data['Call_Price'],
        mode='markers',
        name='Call Option',
        marker=dict(size=6)
    ))

    fig.update_layout(
        title='Options Prices vs Moneyess (S/K)',
        xaxis_title = 'Moneyess Ratio',
        yaxis_title = 'Option Price',
        showlegend=True
    )

    return fig

def main():
    st.set_page_config(
        page_title="Options Data Analytics",
        page_icon="📈",
        layout="wide"
    )

    st.title("Black-Scholes Options Data Analysis")

    st.markdown("""
    Upload your options data to analyze it using the Black-Scholes model. This tool will help you:
    - Calculate theoretical option prices
    - Analyze the Greeks (sensitivity measures)
    - Visualize price distributions and relationships
    - Generate comprehensive statistics
    """)

    # File upload section with requirements
    st.subheader("Data Upload")
    st.markdown("""
    Your CSV file should contain the following columns:
    - Date: The observation date
    - Stock_Price: Current price of the underlying stock
    - Volatility: Implied or historical volatility (as decimal)
    - Risk_Free_Rate: Risk-free interest rate (as decimal)
    - Strike: Option strike price
    - Days_To_Maturity: Number of days until expiration
    - Time_To_Maturity: Time to expiration in years (Days_To_Maturity/365)
    """)

    uploaded_file = st.file_uploader("Upload your options data (CSV)", type="csv")

    if uploaded_file:
        try:
            # Read and validate the uploaded file
            preview_df = pd.read_csv(uploaded_file)
            is_valid, error_message = validate_csv_structure(preview_df)

            if not is_valid:
                st.error(error_message)
                return

            # Process the file if valid
            analyzer = BlackScholesAnalyzer(preview_df)
            data = analyzer.calculate_all()

            # Create tabs for different analyses
            tab1, tab2, tab3, tab4 = st.tabs([
                "Overview",
                "Option Prices",
                "Greeks Analysis",
                "Data Explorer"
            ])

            with tab1:
                st.header("Dataset Overview")

                # Key metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Options", len(data))
                with col2:
                    st.metric("Average Call Price", f"${data['Call_Price'].mean():.2f}")
                with col3:
                    st.metric("Average Put Price", f"${data['Put_Price'].mean():.2f}")

                # Summary statistics
                st.subheader("Summary Statistics")
                st.dataframe(data.describe())

                # Date range information
                st.subheader("Data Coverage")
                st.write(f"Date Range: {data['Date'].min()} to {data['Date'].max()}")

            with tab2:
                st.header("Option Prices Analysis")

                # Price distribution plot
                st.plotly_chart(create_price_distribution_plot(data))

                # Moneyness analysis
                st.subheader("Moneyness Analysis")
                st.plotly_chart(create_moneyness_plot(data))

                # Time decay analysis
                st.subheader("Time Decay Effects")
                time_scatter = px.scatter(
                    data,
                    x='Time_To_Maturity',
                    y=['Call_Price', 'Put_Price'],
                    title='Option Prices vs Time to Maturity'
                )
                st.plotly_chart(time_scatter)

            with tab3:
                st.header("Greeks Analysis")

                # Greek selector
                greek_option = st.selectbox(
                    "Select Greek to Analyze",
                    ["Call_Delta", "Put_Delta", "Gamma", "Vega", "Call_Theta", "Put_Theta"]
                )

                # Create and display the selected Greek's plot
                st.plotly_chart(create_greeks_scatter_plot(data, greek_option))

                # Add explanatory text
                greek_explanations = {
                    "Call_Delta": "Delta measures the rate of change of the option price with respect to the underlying asset price. For calls, it ranges from 0 to 1.",
                    "Put_Delta": "Put Delta ranges from -1 to 0, showing how put options move inversely to the underlying asset.",
                    "Gamma": "Gamma measures the rate of change of Delta, indicating the stability of an option's Delta.",
                    "Vega": "Vega shows the option's sensitivity to changes in volatility.",
                    "Call_Theta": "Call Theta represents the rate of time decay for call options.",
                    "Put_Theta": "Put Theta shows how put options lose value due to time decay."
                }

                st.markdown(greek_explanations.get(greek_option, ""))

            with tab4:
                st.header("Data Explorer")

                # Column selector
                cols_to_show = st.multiselect(
                    "Select columns to display",
                    data.columns.tolist(),
                    default=['Date', 'Stock_Price', 'Strike', 'Call_Price', 'Put_Price']
                )

                if cols_to_show:
                    st.dataframe(data[cols_to_show])

                # Add download button
                st.download_button(
                    label="Download Complete Analysis as CSV",
                    data=data.to_csv(index=False).encode('utf-8'),
                    file_name="black_scholes_analysis_results.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"An error occurred while processing the file: {str(e)}")
            st.write("Please check your file format and try again.")

if __name__ == "__main__":
    main()

