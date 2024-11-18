# -*- coding: utf-8 -*-
"""FrontEnd Dashboard"""

import sys
import os
import streamlit as st
import pandas as pd

# Clone the GitHub repo if not already cloned
if not os.path.exists('DS-440---Group-2'):
    os.system('git clone https://github.com/AmaanRai1/DS-440---Group-2.git')

# Convert Jupyter notebook to Python script if not already converted
if not os.path.exists('DS-440---Group-2/mainV2.py'):
    os.system('jupyter nbconvert --to script DS-440---Group-2/mainV2.ipynb')

# Add repo directory to system path
sys.path.append('DS-440---Group-2')

# Import everything from mainV2.py
from mainV2 import *
from mainV2 import main

# Page configuration
st.set_page_config(
    page_title="Technical Indicator Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar for user input
with st.sidebar:
    st.title('Technical Indicator Dashboard')

    # Stock ticker selection
    stock_ticker_lst = ['DJI', 'GDAXI', 'IBEX']
    selected_stock_ticker = st.selectbox('Select a stock', stock_ticker_lst)

    # Start and end date selections
    start_date = st.date_input("Select a start date")
    end_date = st.date_input("Select an end date")

    # Add an "Execute" button to pull the data
    execute = st.button('Fetch Data and Analyze')

# Logic for fetching and displaying data
if execute:
    try:
        # Load data from the backend using the main() function
        df = main(selected_stock_ticker)
        
        # Filter the data based on the selected date range
        filtered_df = df[(df.index >= pd.Timestamp(start_date)) & (df.index <= pd.Timestamp(end_date))]
        
        if not filtered_df.empty:
            st.write(filtered_df)  # Display the filtered stock data
            st.success(f"Successfully fetched data for {selected_stock_ticker} from {start_date} to {end_date}.")

            # Display any further analysis, e.g., plots or calculations
            st.markdown("## Analysis and Visualization")
            st.line_chart(filtered_df['Close'])  # Example visualization

        else:
            st.warning("No data available for the selected date range. Please choose different dates.")

    except ValueError as e:
        st.error(f"An error occurred while fetching data: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

    # Technical indicators selection
    st.markdown("### Select Technical Indicators:")
    selected_technical_indicator = st.radio(
        'Choose a technical indicator',
        ('RSI (Relative Strength Index)', 'MACD (Moving Average Convergence Divergence)', 'TEMA (Triple Exponential Moving Average)')
    )
    
    # Selectbox to decide whether to pair indicator with ML model
    st.markdown("### Pair with Machine Learning Model?")
    pair_option = st.selectbox(
        "Would you like to pair the selected technical indicator with the chosen ML model?",
        ("No", "Yes")
    )

    # Conditional display of ML model selection and hybrid strategy
    if pair_option == "Yes":
        st.markdown("### Select Machine Learning Model:")
        selected_model = st.radio(
            'Choose a model to pair with indicators',
            ('Linear Regression', 'LSTM', 'ANN')
        )
        st.markdown("### Select Hybrid Strategy:")
        selected_strategy = st.radio(
            'Choose a hybrid strategy to run the machine learning',
            ('Emphasize Technical Indicators', 'Emphasize Machine Learning'),
            index=0  # Default to "Emphasize Technical Indicators"
        )
    else:
        selected_model = "Not Using Pair"
        selected_strategy = "Not Using Strategy"

# Add the "Execute Hybrid Model" Button Below the Sidebar Section
execute = st.sidebar.button('Execute Hybrid Model', key='execute_button')

# Logic for Button Execution
if execute:
    st.write(f"Fetching data for {selected_stock_ticker} from {start_date} to {end_date}...")

    # Load data from Yahoo Finance
    try:
        stock_data = yf.download(selected_stock_ticker, start=start_date, end=end_date)
        
        if stock_data.empty:
            st.warning("No data found for the selected date range. Please try a different range.")
        else:
            st.write(stock_data)  # Display the stock data



            # Pair with Machine Learning Model if selected
            if pair_option == "Yes":
                st.write(f"Running {selected_technical_indicator} with {selected_model} using {selected_strategy}...")
                # Implement your ML model logic here
            else:
                st.write(f"Running {selected_technical_indicator} without pairing...")
                # Add logic if using just the technical indicator

    except Exception as e:
        st.error(f"An error occurred while fetching the data: {e}")
