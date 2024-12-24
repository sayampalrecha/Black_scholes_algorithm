# Black-Scholes Option Pricing Model Explorer

## Overview

This interactive web application provides a comprehensive platform for understanding, calculating, and analyzing option prices using the Black-Scholes model. Whether you're a student learning about options pricing, a trader analyzing market data, or a researcher exploring option characteristics, this tool offers intuitive visualizations and powerful analysis capabilities.

<div align="center">
  <img src="path_to_your_app_screenshot.png" alt="Black-Scholes Explorer Interface" width="800"/>
</div>

## Features

### 1. Model Introduction 📚
The introduction page serves as an educational resource, helping users understand the theoretical foundations of the Black-Scholes model through:

- Interactive visualizations of option payoff patterns
- Detailed explanations of model assumptions and limitations
- Step-by-step breakdown of the Black-Scholes formula
- Dynamic demonstrations of how different parameters affect option prices

### 2. Option Calculator 🧮
This section provides a practical tool for option pricing:

- Real-time calculation of option prices and Greeks
- Sensitivity analysis for all input parameters
- Visualization of how changes in parameters affect option values
- Clear display of all relevant pricing metrics

### 3. Data Analysis Dashboard 📊
The analysis dashboard enables users to process and visualize their own options data:

- Upload and analyze CSV files containing options data
- Calculate theoretical prices and Greeks for large datasets
- Generate interactive visualizations of price distributions and relationships
- Export processed results for further analysis

## Dataset
Synthetic data made using python which has 6300 rows and 12 columns <br>
Check the Data_generator file for the code to generating the data or else the my_options_data.csv file for the project 

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/black-scholes-explorer.git
cd black-scholes-explorer
```

2. Create and activate a virtual environment (optional but recommended):
```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

1. Start the application:
```bash
streamlit run Home.py
```

2. Open your web browser and navigate to: http://localhost:8501

3. Explore the different pages using the sidebar navigation:
   - Begin with "Model Introduction" to understand the fundamentals
   - Use "Calculator" to price individual options
   - Try "Data Analysis" to process multiple options simultaneously

## Data Format Requirements

For the data analysis feature, prepare your CSV file with the following structure:

```csv
Date,Stock_Price,Volatility,Risk_Free_Rate,Strike,Days_To_Maturity,Time_To_Maturity
2024-01-01,100.75,0.2,0.059,90.68,30,0.119
```

Required columns:
- `Date`: Date of the option data
- `Stock_Price`: Current price of the underlying stock
- `Volatility`: Implied or historical volatility (as decimal)
- `Risk_Free_Rate`: Risk-free interest rate (as decimal)
- `Strike`: Option strike price
- `Days_To_Maturity`: Number of days until expiration
- `Time_To_Maturity`: Time to expiration in years (Days_To_Maturity/365)

## Project Structure

```
black-scholes-explorer/
├── pages/
│   ├── 1_Model_Introduction.py   # Educational content and interactive demos
│   ├── 2_Calculator.py           # Option pricing calculator
│   └── 3_Data_Analysis.py        # Data upload and analysis dashboard
├── models/
│   └── black_scholes.py          # Core Black-Scholes implementation
├── Home.py                       # Main application page
├── requirements.txt              # Project dependencies
└── README.md                     # Documentation
```

## Dependencies

The project relies on the following Python packages:
```txt
streamlit>=1.24.0
pandas>=1.5.0
numpy>=1.23.0
scipy>=1.9.0
plotly>=5.13.0
```

## Contact 

- **Email**: sayam.palrecha@gwu.edu
- **Website**: sayam.me

---
<div align="center">
  Made by Sayam Palrecha
</div>
