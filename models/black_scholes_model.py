import numpy as np
import scipy 
from scipy.stats import norm
import pandas as pd

"""
The code provides various variables used for black scholes model in order to calculate the call and put price for options
"""



class BlackScholes:
    """
    A class implementing the Black-Scholes option pricing model.

    The Black-Scholes model is used to calculate the theoretical price of European-style options.
    It assumes that the underlying asset follows geometric Brownian motion with constant volatility
    and that the risk-free rate is constant.
    """

    def __init__(self, S, K, T, r, sigma):
        """
        Initialize Black-Scholes pricing model with option parameters.

        Parameters:
        -----------
        S : float
            Current stock price
        K : float
            Strike price
        T : float
            Time to maturity (in years)
        r : float
            Risk-free interest rate (annual rate, expressed as decimal)
        sigma : float
            Volatility of the underlying asset (annual, expressed as decimal)
        """
        # Convert inputs to float to ensure mathematical operations work correctly
        self.S = float(S)
        self.K = float(K)
        self.T = float(T)
        self.r = float(r)
        self.sigma = float(sigma)

        # Calculate d1 and d2 parameters used in the Black-Scholes formula
        # These are calculated once during initialization for efficiency
        self._d1 = self._calculate_d1()
        self._d2 = self._calculate_d2()

    def _calculate_d1(self):
        """
        Calculate d1 parameter of the Black-Scholes formula.
        d1 represents the normalized distance to strike, adjusted for drift.
        """
        numerator = (np.log(self.S / self.K) +
                    (self.r + 0.5 * self.sigma ** 2) * self.T)
        denominator = self.sigma * np.sqrt(self.T)
        return numerator / denominator

    def _calculate_d2(self):
        """
        Calculate d2 parameter of the Black-Scholes formula.
        d2 is related to d1 and represents a drift-adjusted probability measure.
        """
        return self._d1 - self.sigma * np.sqrt(self.T)

    def call_price(self):
        """
        Calculate the price of a European call option.

        Returns:
        --------
        float
            Theoretical price of the call option
        """
        # The call option price has two terms:
        # 1. Current stock price times probability it will be exercised
        term1 = self.S * norm.cdf(self._d1)
        # 2. Present value of strike price times probability of exercise
        term2 = self.K * np.exp(-self.r * self.T) * norm.cdf(self._d2)
        return term1 - term2

    def put_price(self):
        """
        Calculate the price of a European put option.

        Returns:
        --------
        float
            Theoretical price of the put option
        """
        # The put option price has two terms:
        # 1. Present value of strike price times probability of exercise
        term1 = self.K * np.exp(-self.r * self.T) * norm.cdf(-self._d2)
        # 2. Current stock price times probability it will be exercised
        term2 = self.S * norm.cdf(-self._d1)
        return term1 - term2

    def call_delta(self):
        """
        Calculate the delta of a call option.
        Delta measures the rate of change of option value with respect to the underlying asset price.
        """
        return norm.cdf(self._d1)

    def put_delta(self):
        """
        Calculate the delta of a put option.
        Delta measures the rate of change of option value with respect to the underlying asset price.
        """
        return -norm.cdf(-self._d1)

    def gamma(self):
        """
        Calculate the gamma of the option.
        Gamma measures the rate of change of delta with respect to the underlying asset price.
        """
        return norm.pdf(self._d1) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self):
        """
        Calculate the vega of the option.
        Vega measures sensitivity of option value to changes in volatility.
        """
        return self.S * np.sqrt(self.T) * norm.pdf(self._d1)

    def theta_call(self):
        """
        Calculate the theta of a call option.
        Theta measures the sensitivity of option value to time decay.
        """
        term1 = -(self.S * norm.pdf(self._d1) * self.sigma) / (2 * np.sqrt(self.T))
        term2 = -self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self._d2)
        return term1 + term2

    def theta_put(self):
        """
        Calculate the theta of a put option.
        Theta measures the sensitivity of option value to time decay.
        """
        term1 = -(self.S * norm.pdf(self._d1) * self.sigma) / (2 * np.sqrt(self.T))
        term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self._d2)
        return term1 + term2

# Example usage demonstrating how to use the BlackScholes class


import pandas as pd
import numpy as np
from scipy.stats import norm
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class BlackScholesAnalyzer:
    """
    A class for analyzing options data using the Black-Scholes model.
    Includes data processing, analysis, and visualization capabilities.
    """

    def __init__(self, csv_path):
        """
        Initialize the analyzer with the path to the CSV file.

        Parameters:
        -----------
        csv_path : str
            Path to the CSV file containing options data
        """
        self.csv_path = "/Users/sayam_palrecha/my_project/my_option_data.csv"
        self.data = None
        self.results = None

    def load_data(self):
        """Load and preprocess the options data from CSV."""
        # Read the CSV file
        self.data = pd.read_csv(self.csv_path)

        # Convert date column to datetime
        self.data['Date'] = pd.to_datetime(self.data['Date'])

        # Ensure all numeric columns are float
        numeric_columns = ['Stock_Price', 'Volatility', 'Risk_Free_Rate',
                         'Strike', 'Time_To_Maturity']
        self.data[numeric_columns] = self.data[numeric_columns].astype(float)

        return self.data

    def calculate_option_prices(self):
        """Calculate call and put prices for all options in the dataset."""
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # Create arrays to store results
        call_prices = np.zeros(len(self.data))
        put_prices = np.zeros(len(self.data))

        # Calculate option prices for each row
        for idx, row in self.data.iterrows():
            bs = BlackScholes(
                S=row['Stock_Price'],
                K=row['Strike'],
                T=row['Time_To_Maturity'],
                r=row['Risk_Free_Rate'],
                sigma=row['Volatility']
            )
            call_prices[idx] = bs.call_price()
            put_prices[idx] = bs.put_price()

        # Add results to the dataframe
        self.data['Call_Price'] = call_prices
        self.data['Put_Price'] = put_prices

        return self.data

    def calculate_greeks(self):
        """Calculate option Greeks for all options in the dataset."""
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # Arrays for Greeks
        call_deltas = np.zeros(len(self.data))
        put_deltas = np.zeros(len(self.data))
        gammas = np.zeros(len(self.data))
        vegas = np.zeros(len(self.data))
        call_thetas = np.zeros(len(self.data))
        put_thetas = np.zeros(len(self.data))

        # Calculate Greeks for each row
        for idx, row in self.data.iterrows():
            bs = BlackScholes(
                S=row['Stock_Price'],
                K=row['Strike'],
                T=row['Time_To_Maturity'],
                r=row['Risk_Free_Rate'],
                sigma=row['Volatility']
            )
            call_deltas[idx] = bs.call_delta()
            put_deltas[idx] = bs.put_delta()
            gammas[idx] = bs.gamma()
            vegas[idx] = bs.vega()
            call_thetas[idx] = bs.theta_call()
            put_thetas[idx] = bs.theta_put()

        # Add Greeks to the dataframe
        self.data['Call_Delta'] = call_deltas
        self.data['Put_Delta'] = put_deltas
        self.data['Gamma'] = gammas
        self.data['Vega'] = vegas
        self.data['Call_Theta'] = call_thetas
        self.data['Put_Theta'] = put_thetas

        return self.data

    def analyze_results(self):
        """Perform statistical analysis on the calculated option prices and Greeks."""
        if 'Call_Price' not in self.data.columns:
            raise ValueError("Option prices not calculated. Run calculate_option_prices() first.")

        # Calculate summary statistics
        self.results = {
            'summary': self.data[[
                'Call_Price', 'Put_Price', 'Call_Delta', 'Put_Delta',
                'Gamma', 'Vega', 'Call_Theta', 'Put_Theta'
            ]].describe(),

            'moneyness': self.data['Stock_Price'] / self.data['Strike'],

            'avg_by_maturity': self.data.groupby('Days_To_Maturity')[[
                'Call_Price', 'Put_Price'
            ]].mean()
        }

        return self.results

    def save_results(self, output_path):
        """Save the analyzed data to a CSV file."""
        if self.data is None:
            raise ValueError("No data to save. Perform analysis first.")

        self.data.to_csv(output_path, index=False)
        print(f"Results saved to {output_path}")

# Main execution code
if __name__ == "__main__":
    # Create analyzer instance
    analyzer = BlackScholesAnalyzer('my_option_data.csv')

    # Load and process data
    analyzer.load_data()

    # Calculate option prices and Greeks
    analyzer.calculate_option_prices()
    analyzer.calculate_greeks()

    # Analyze results
    results = analyzer.analyze_results()

    # Print summary statistics
    print("\nSummary Statistics:")
    print(results['summary'])

    # Save results
    analyzer.save_results('black_scholes_results.csv')
