import streamlit as st
import pandas as pd
import sys
import os
import subprocess

# Step 1: Clone the GitHub repository if it doesn't already exist
repo_url = "https://github.com/AmaanRai1/DS-440---Group-2.git"
repo_dir = "DS-440---Group-2"

if not os.path.exists(repo_dir):
    subprocess.run(["git", "clone", repo_url], check=True)

# Step 2: Add the directory containing mainV2.py to the system path
sys.path.append(os.path.abspath(repo_dir))

# Step 3: Import the main and split_data functions from mainV2
try:
    from mainV2_saiem.py import *
except ImportError:
    st.error("Unable to import mainV2. Please ensure the repository was cloned correctly.")

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

    # Technical indicators selection
    st.markdown("### Select Technical Indicators:")
    selected_technical_indicator = st.radio(
        'Choose a technical indicator',
        ('RSI (Relative Strength Index)', 'MACD (Moving Average Convergence Divergence)', 'TEMA (Triple Exponential Moving Average)')
    )

    # If TEMA is selected, ask for parameters
    if selected_technical_indicator == 'TEMA (Triple Exponential Moving Average)':
        st.markdown("### TEMA Parameters:")
        short_period = st.number_input("Short Period (e.g., 5)", min_value=1, value=5)
        mid_period = st.number_input("Mid Period (e.g., 20)", min_value=1, value=20)
        long_period = st.number_input("Long Period (e.g., 50)", min_value=1, value=50)

    # Add the "Execute Hybrid Model" Button Below the Sidebar Section
    execute_hybrid = st.button('Execute Hybrid Model', key='execute_hybrid')

# Main logic to handle data loading and analysis
if execute_hybrid:
    try:
        # Load data using the main function from mainV2.py with selected stock ticker
        df = main(selected_stock_ticker)

        # Display the loaded data
        st.write(f"Displaying data for {selected_stock_ticker}:")
        st.write(df.head())  # Display the first few rows of data

        # Split the data into training, validation, and test sets
        train_data, validation_data, test_data = split_data(df)

        # Proceed with selected analysis or machine learning model
        st.markdown("## Analysis and Visualization")
        st.line_chart(df['Close'])  # Plotting the closing prices over time

        if selected_technical_indicator == 'TEMA (Triple Exponential Moving Average)':
            st.write(f"Running TEMA strategy for {selected_stock_ticker}...")

            # Call tema_strategy() with the appropriate arguments
            tema_results = tema_strategy(
                test_data, 'Close', short_period, mid_period, long_period
            )

            # Display the result of the TEMA strategy
            st.write("TEMA Strategy Results:")
            st.write(tema_results.head())

        else:
            st.write(f"Running {selected_technical_indicator} without pairing with ML model...")

    except ValueError as e:
        st.error(f"An error occurred while fetching data: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


