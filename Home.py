import streamlit as st

def main():
    st.set_page_config(
        page_title="Black-Scholes Model Explorer",
        page_icon="📊",
        layout="wide"
    )

    # Main title with custom styling
    st.markdown("""
    <h1 style='text-align: center;'>Black-Scholes Option Pricing Model Explorer</h1>
    """, unsafe_allow_html=True)

    # Introduction section
    st.markdown("""
    Welcome to the Black-Scholes Model Explorer! This interactive application helps you understand
    and work with the Black-Scholes option pricing model, a cornerstone of modern financial theory.

    ### What You Can Do Here:

    1. **Learn About the Model** 📚
       - Explore the theoretical foundations
       - Understand key assumptions and limitations
       - See how different parameters affect option prices

    2. **Use the Calculator** 🧮
       - Calculate option prices and Greeks
       - Visualize relationships between parameters
       - Experiment with different scenarios

    3. **Analyze Your Data** 📈
       - Upload your own options data
       - Get comprehensive analysis and visualizations
       - Download processed results
    """)

    # Featured content section
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Getting Started Guide

        If you're new to options trading and the Black-Scholes model:
        1. Start with the "Model Introduction" page to learn the basics
        2. Try the interactive calculator to understand how parameters affect prices
        3. When you're ready, use the data analyzer with your own options data

        The model helps determine fair prices for European-style stock options by considering:
        - Current stock price
        - Strike price
        - Time to expiration
        - Risk-free interest rate
        - Stock price volatility
        """)

    with col2:
        st.markdown("""
        ### Why Black-Scholes Matters

        The Black-Scholes model revolutionized options trading by providing:
        - A theoretical framework for option pricing
        - Risk management tools through "Greeks"
        - A foundation for modern derivatives trading

        While the model has limitations, it remains fundamental to understanding
        options pricing and risk management in financial markets.
        """)

    # Additional resources
    st.markdown("---")
    st.markdown("""
    ### Historical Background

    The Black-Scholes model was developed by Fischer Black, Myron Scholes, and Robert Merton
    in 1973. Their groundbreaking work:
    - Solved a fundamental problem in options pricing
    - Introduced mathematical rigor to financial economics
    - Led to the 1997 Nobel Prize in Economics (awarded to Scholes and Merton)

    The model continues to influence how we think about risk, pricing, and financial markets.
    """)

    st.markdown("---")
    st.markdown("""
    ### More resources to understand the model

    - Video by Veritasium https://youtu.be/A5w-dEgIU1M?si=pN8_EKAFZUD0J64C
    - Video by https://www.youtube.com/watch?v=SL8HDfYYk8Y&t=134s
    - Wikipedia article https://en.wikipedia.org/wiki/Black–Scholes_model
    """
                )

    # Footer with navigation help
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center;'>
    Navigate through the pages using the sidebar menu ←<br>
    </div>
    """, unsafe_allow_html=True)



if __name__ == "__main__":
    main()
