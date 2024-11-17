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

# Page configuration
st.set_page_config(
    page_title="Technical Indicator Dashboard",
    layout="wide",
    initial_sidebar_state="expanded")

# Sidebar for user input
with st.sidebar:
    st.title('Technical Indicator Dashboard')

    # Stock ticker selection
    stock_ticker_lst = ['dji', 'gdaxi', 'ibex']
    selected_stock_ticker = st.selectbox('Select a stock', stock_ticker_lst)

    # Start and end date selections
    start_date = st.date_input("Select a start date")
    end_date = st.date_input("Select an end date")

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

# **Add the "Execute Hybrid Model" Button Below the Sidebar Section**
execute = st.sidebar.button('Execute Hybrid Model', key='execute_button')

# **Logic for Button Execution**
if execute:
    # Load data based on selected stock ticker
    st.write(f"Loading data for {selected_stock_ticker} from {start_date} to {end_date}...")
    df = load_data(selected_stock_ticker, start_date, end_date)

    # Apply the selected technical indicator
    if selected_technical_indicator == 'RSI (Relative Strength Index)':
        st.write(f"Applying RSI indicator on data...")
        df = apply_indicator(df, indicator='RSI')
    elif selected_technical_indicator == 'MACD (Moving Average Convergence Divergence)':
        st.write(f"Applying MACD indicator on data...")
        df = apply_indicator(df, indicator='MACD')
    elif selected_technical_indicator == 'TEMA (Triple Exponential Moving Average)':
        st.write(f"Applying TEMA indicator on data...")
        df = apply_indicator(df, indicator='TEMA')

    # Pair with Machine Learning Model if selected
    if pair_option == "Yes":
        st.write(f"Running {selected_technical_indicator} with {selected_model} using {selected_strategy}...")
        if selected_model == 'Linear Regression':
            result = run_model(df, model='Linear Regression', strategy=selected_strategy)
        elif selected_model == 'LSTM':
            result = run_model(df, model='LSTM', strategy=selected_strategy)
        elif selected_model == 'ANN':
            result = run_model(df, model='ANN', strategy=selected_strategy)
        st.write(result)
    else:
        st.write(f"Running {selected_technical_indicator} without pairing...")
        result = run_indicator_only(df)
        st.write(result)
