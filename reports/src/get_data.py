import pandas as pd
import numpy as np
import config
import streamlit as st

@st.cache_data
def _df_ibovespa():
    # deixar data como indice
    df = pd\
        .read_csv(f'{config.BASE_PATH}/raw/dados_ibovespa.csv')\
        .rename(columns={
            'Data':'Date'
            , 'Último':'Close'
            , 'Abertura':'Open'
            , 'Máxima':'High'
            , 'Mínima':'Low'
            , 'Vol.':'Volume'
        })
    df['Adj Close'] =  df['Close']
    df.Date = pd.to_datetime(df['Date']).dt.date
    df = df.sort_values(['Date'])
    df['Datetime'] = pd.to_datetime(df['Date'])
    df.Open = df.Open.astype(float)
    df.Close = df.Close.astype(float)
    df.High = df.High.astype(float)
    df.Low = df.Low.astype(float)
    df.Volume = df.Volume.str.replace('M','000000').str.replace(',','').str.replace('K','000')
    df.Volume = df.Volume.astype(float)
    df['Base Volume'] = df.Volume.astype(float)
    df = df.sort_values(['Datetime'])

    return df