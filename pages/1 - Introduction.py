import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import norm
from models.black_scholes_model import BlackScholes, BlackScholesAnalyzer
import sys
import os




def plot_normal_distribution(mean,std_dev):
    """Create a plot of normal distribution to explain returns assumption."""
    x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 200)
    y = norm.pdf(x,mean,std_dev)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x,y=y,name='Normal Distribution'))
    fig.update_layout(
        title = "Normal Distribution of Returns",
        xaxis_title = "Returns",
        yaxis_title = "Probability Density",
        showlegend = False
    )
    return fig

def plot_option_payoff(S,K,option_type='call'):
    '''Create an interactive plot showing option payoff at expiration'''
    stock_prices = np.linspace(max(0,K-50),K+50,100)
    if option_type == 'call':
        payoff = np.maximum(stock_prices - K,0)
        title =f'Call Option Payoff (Strike = ${K})'
    else:
        payoff = np.maximum(K - stock_prices,0)
        title = f'Put Option Payoff (Strike = ${K})'

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_prices,y=payoff,name='Option Payoff'))
    fig.add_trace(go.Scatter(
        x=[K,K],
        y=[0,max(payoff)],
        mode='lines',
        line = dict(dash='dash',color='red'),
        name='Strike Price'
    ))

    fig.update_layout(
        title=title,
        xaxis_title='Stock Price',
        yaxis_title='Payoff',
        showlegend=True
    )
    return fig

def main():
    st.set_page_config(
        page_title="Model Introduction",
        page_icon="📚",
        layout="wide"
    )
    st.title("Understanding the Black-Scholes Option Pricing Model.")

    # Introuction

    st.markdown(
        '''
        The Black-Scholes model represents one of the most significant breakthroughs in financial
        theory. Let's explore how this elegant mathematical framework helps us understand and
        price options contracts.
        '''
    )

    # Create tabs for organised learning

    tab1, tab2, tab3, tab4 = st.tabs([
        "Fundamentals",
        "Key Assumptions",
        "The Formula",
        "Interactive Examples"
        ])

    with tab1:
        st.header("Option Fundamentals")
        st.markdown("""
        Before diving into the Black-Scholes model, let's understand what options are and
        how they work. An option is a contract that gives its holder the right, but not
        the obligation, to buy (call option) or sell (put option) an asset at a specified
        price (strike price) on or before a specific date (expiration date).
        """)
        # Interactive option payoff demonstration

        st.subheader("Option Payoff Patterns")
        col1, col2 = st.columns(2)
        with col1:
            K = st.slider("Strike Price ($)",50,150,100,5,key="strike_payoff")
            st.markdown("""
            The strike price is the predetermined price at which the option holder can
            exercise their right to buy (call) or sell (put) the underlying asset.
            """)

        # Display both call and put payoffs
        st.plotly_chart(plot_option_payoff(100,K,'call'))
        st.plotly_chart(plot_option_payoff(100,K,'put'))

        st.markdown("""
        These payoff diagrams show the profit or loss at expiration. Notice how:
        - Call options become profitable when the stock price exceeds the strike price
        - Put options become profitable when the stock price falls below the strike price
        - The maximum loss for both is limited to the premium paid
        """)

    with tab2:
        st.header("Model Assumptions")
        st.markdown("""
        The Black-Scholes model makes several key assumptions about market behavior and
        conditions. Understanding these assumptions helps us appreciate both the model's
        power and its limitations.
        """)

        col1,col2 = st.columns(2)
        with col1:
            st.subheader("Core Assumptions")
            st.markdown("""
            1. **Stock Price Movement**
               - Follows a geometric Brownian motion
               - Returns are normally distributed
               - No sudden jumps in price

            2. **Market Conditions**
               - No arbitrage opportunities
               - Risk-free rate is constant
               - No transaction costs
               - Continuous trading is possible

            3. **Option Characteristics**
               - European-style options only
               - No dividends during option life
            """)

        with col2:
            st.subheader("Return Distribution")
            # Interactive normal distribution plot
            mean = st.slider("Expected Returns (%)",-10.0, 10.0, 0.0, 0.5)
            volatility = st.slider("Volatility (%)", 5.0, 50.0, 20.0, 5.0)

            st.plotly_chart(plot_normal_distribution(mean/100, volatility/100))

            st.markdown("""
            This plot shows the assumed normal distribution of returns. In reality:
            - Returns might have "fat tails" (more extreme events)
            - Distributions can be skewed
            - Volatility may not be constant
            """)

        with tab3:
            st.header("The Black-Scholes Formula")

            st.markdown("""
            The Black-Scholes formula elegantly combines several variables to determine
            option prices. Let's break down each component:
            """)

            st.latex(r'''
            C = S_0N(d_1) - Ke^{-rT}N(d_2)
            ''')

            st.markdown("""
            Where:
            - C = Call option price
            - S₀ = Current stock price
            - K = Strike price
            - r = Risk-free interest rate
            - T = Time to maturity
            - N() = Cumulative standard normal distribution
            """)

            st.latex(r'''
            d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}
            ''')

            st.latex(r'''
            d_2 = d_1 - \sigma\sqrt{T}
            ''')

            st.markdown("""
            The formula might look complex, but each term has an economic interpretation:
            - S₀N(d₁) represents the expected benefit from acquiring the stock
            - Ke^(-rT)N(d₂) represents the present value of the strike price
            - The difference gives us the call option's value
            """)

            st.markdown("""
            For put options, we use the put-call parity relationship:
            """)

            st.latex(r'''
            P = Ke^{-rT}N(-d_2) - S_0N(-d_1)
            ''')

    with tab4:
        st.header("Interactive Learning")

        st.markdown("""
        Experiment with different parameters to see how they affect option prices. This
        hands-on approach helps build intuition about option pricing.
        """)

        col1, col2 = st.columns(2)

        with col1:
            S = st.number_input("Stock Price ($)", 50.0, 150.0, 100.0, 5.0)
            K = st.number_input("Strike Price ($)", 50.0, 150.0, 100.0, 5.0)
            T = st.slider("Time to Maturity (years)", 0.1, 2.0, 1.0, 0.1)

        with col2:
            r = st.slider("Risk-free Rate (%)", 0.0, 10.0, 5.0, 0.5) / 100
            sigma = st.slider("Volatility (%)", 10.0, 50.0, 20.0, 5.0) / 100

        # Calculate option prices using imported BlackScholes class

        bs = BlackScholes(S, K, T, r, sigma)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Call Option Price", f"${bs.call_price():.2f}")
            st.markdown("""
            The call option price increases with:
            - Higher stock price
            - Lower strike price
            - More time to expiration
            - Higher volatility
            - Higher interest rates
            """)

        with col2:
            st.metric("Put Option Price", f"${bs.put_price():.2f}")
            st.markdown("""
            The put option price increases with:
            - Lower stock price
            - Higher strike price
            - More time to expiration
            - Higher volatility
            - Lower interest rates
            """)

if __name__ == "__main__":
    main()
