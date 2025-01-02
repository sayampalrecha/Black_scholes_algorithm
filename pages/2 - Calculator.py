import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Add the project root to Python path

from models.black_scholes_model import BlackScholes

def create_sensitivity_plot(param_range, base_params, param_name):
    """Create sensitivity analysis plot for a parameter."""
    call_prices = []
    put_prices = []

    for value in param_range:
        params = base_params.copy()
        params[param_name] = value
        bs = BlackScholes(**params)
        call_prices.append(bs.call_price())
        put_prices.append(bs.put_price())

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=param_range, y=call_prices, name='Call Option'))
    fig.add_trace(go.Scatter(x=param_range, y=put_prices, name='Put Option'))

    param_labels = {
        'S': 'Stock Price',
        'K': 'Strike Price',
        'T': 'Time to Maturity',
        'r': 'Risk-free Rate',
        'sigma': 'Volatility'
    }

    fig.update_layout(
        title=f'Option Price Sensitivity to {param_labels[param_name]}',
        xaxis_title=param_labels[param_name],
        yaxis_title='Option Price',
        showlegend=True
    )
    return fig

def main():
    st.set_page_config(page_title="Option Calculator", page_icon="🧮", layout="wide")

    st.title("Black-Scholes Option Calculator")

    # Input parameters section
    st.subheader("Input Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        S = st.number_input("Stock Price ($)", min_value=1.0, max_value=1000.0, value=100.0, step=5.0)
        K = st.number_input("Strike Price ($)", min_value=1.0, max_value=1000.0, value=100.0, step=5.0)

    with col2:
        T = st.number_input("Time to Maturity (years)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
        r = st.number_input("Risk-free Rate (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.5) / 100

    with col3:
        sigma = st.number_input("Volatility (%)", min_value=1.0, max_value=100.0, value=20.0, step=1.0) / 100

    # Calculate option prices and Greeks
    bs = BlackScholes(S=S, K=K, T=T, r=r, sigma=sigma)

    # Results section
    st.header("Results")

    # Option Prices
    price_col1, price_col2 = st.columns(2)
    with price_col1:
        st.metric("Call Option Price", f"${bs.call_price():.2f}")
    with price_col2:
        st.metric("Put Option Price", f"${bs.put_price():.2f}")

    # Greeks
    st.subheader("Greeks")
    greek_col1, greek_col2, greek_col3, greek_col4 = st.columns(4)

    with greek_col1:
        st.metric("Call Delta", f"{bs.call_delta():.4f}")
        st.metric("Put Delta", f"{bs.put_delta():.4f}")

    with greek_col2:
        st.metric("Gamma", f"{bs.gamma():.4f}")

    with greek_col3:
        st.metric("Vega", f"{bs.vega():.4f}")

    with greek_col4:
        st.metric("Call Theta", f"{bs.theta_call():.4f}")
        st.metric("Put Theta", f"{bs.theta_put():.4f}")

    # Sensitivity Analysis section
    st.header("Sensitivity Analysis")

    # Parameter selection for sensitivity analysis
    param_to_analyze = st.selectbox(
        "Select parameter for sensitivity analysis",
        ["Stock Price", "Strike Price", "Time to Maturity", "Risk-free Rate", "Volatility"]
    )

    # Define parameter ranges for sensitivity analysis
    param_ranges = {
        "Stock Price": np.linspace(max(1, S-50), S+50, 100),
        "Strike Price": np.linspace(max(1, K-50), K+50, 100),
        "Time to Maturity": np.linspace(0.1, 2.0, 100),
        "Risk-free Rate": np.linspace(0.01, 0.15, 100),
        "Volatility": np.linspace(0.1, 0.5, 100)
    }

    param_map = {
        "Stock Price": "S",
        "Strike Price": "K",
        "Time to Maturity": "T",
        "Risk-free Rate": "r",
        "Volatility": "sigma"
    }

    base_params = {"S": S, "K": K, "T": T, "r": r, "sigma": sigma}

    # Create and display sensitivity plot
    sensitivity_plot = create_sensitivity_plot(
        param_ranges[param_to_analyze],
        base_params,
        param_map[param_to_analyze]
    )
    st.plotly_chart(sensitivity_plot)

    # Add explanatory text for Greeks
    st.header("Understanding the Greeks")
    st.markdown("""
    The Greeks measure different aspects of option price sensitivity:

    - **Delta**: Measures the rate of change in option price with respect to the underlying asset price
    - **Gamma**: Measures the rate of change in Delta with respect to the underlying asset price
    - **Vega**: Measures sensitivity to changes in volatility
    - **Theta**: Measures the rate of time decay in option value
    """)

if __name__ == "__main__":
    main()
