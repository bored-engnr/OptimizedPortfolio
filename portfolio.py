import os
if not os.path.isdir('data'):
    os.system('git clone https://github.com/robertmartin8/PyPortfolioOpt.git')
    os.chdir('PyPortfolioOpt/cookbook')

# Instalando demais biliotecas

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#import urllib3
import urllib.request
import json
import yfinance as yf
import streamlit as st
import plotly.express as px
import pypfopt

#from pypfopt import risk_models
#from pypfopt import plotting

try:
    plt.style.use("seaborn-deep")
    plt.style.use("seaborn-v0_8-deep")
except Exception:  # pragma: no cover
    pass
# Create selectors
st.title('Otimizador de Portfólio')
st.divider()

st.header("Entre com sua carteira")
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)
col7, col8 = st.columns(2)

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

with col1:
    stock1 = st.selectbox(
        "Selecione um ativo",
        ("IWDA.L", "EIMI.L", "EMVL.L", "USSC.L", "IWVL.L"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        #index=None,
        placeholder="IWDA.L ou EMVL.L ...",
        key='stock_1'
    )

with col2:
    percent_stock_1 = st.number_input(
        "Participação (%)", 
        value=0, 
        placeholder="Digite um número...",
        key='stock_percentage_1')

with col3:
    stock2 = st.selectbox(
        "Selecione um ativo",
        ("IWDA.L", "EIMI.L", "EMVL.L", "USSC.L", "IWVL.L"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        #index=None,
        placeholder="IWDA.L ou EMVL.L ...",
        key='stock_2'
    )

with col4:
    percent_stock_2 = st.number_input(
        "Participação (%)", 
        value=0, 
        placeholder="Digite um número...",
        key='stock_percentage_2')

#tickers = ["IWDA.L", "EIMI.L", "EMVL.L", "USSC.L", "IWVL.L"]
tickers = [stock1,stock2]
ratios = [percent_stock_1,percent_stock_2]


def get_yahoo_shortname(symbol):
    response = urllib.request.urlopen(f'https://query2.finance.yahoo.com/v1/finance/search?q={symbol}')
    content = response.read()
    data = json.loads(content.decode('utf8'))['quotes'][0]['shortname']
    return data

def get_yahoo_profile(symbol):
    response = urllib.request.urlopen(f'https://query2.finance.yahoo.com/v1/finance/search?q={symbol}')
    content = response.read()
    #data = json.loads(content.decode('utf8'))#['quotes'][0]['shortname'] ver todas as info
    market = json.loads(content.decode('utf8'))['quotes'][0]['exchDisp']
    return market

# Verifica se tickers foram preenchidos
if tickers:
    ohlc = yf.download(tickers, period="max")

    shortname =[]
    bolsa = []
    for symbol in tickers:
        shortname.append(get_yahoo_shortname(symbol))
        bolsa.append(get_yahoo_profile(symbol))

    df = pd.DataFrame({"Código": tickers, "Nomes": shortname, "Bolsa": bolsa, "%": ratios})
    st.subheader("Carteira")
    df

    prices = ohlc["Adj Close"].dropna(how="all")
    st.subheader("Últimos preços")
    st.write(prices.tail())

    col9 = st.columns(1)
    df_prices = pd.DataFrame(prices[prices.index >= "2005-01-01"])
    #df_prices
    st.line_chart(df_prices)
