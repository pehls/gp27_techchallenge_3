import pandas as pd
import numpy as np
import config
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

@st.cache_data
def _get_importance_data_sintomas():
    query = """
    select 
          resultado_covid
        , idade
        , sexo
        , tem_plano_saude
        , teve_febre
        , teve_dificuldade_respirar
        , teve_dor_cabeca
        , teve_fadiga
        , teve_perda_cheiro
    from
        fiap-tech-challenge-3.trusted_pnad.tb_f_covid_2020
    where
        resultado_covid in ('Sim','Não')
        and idade is not null
        and sexo is not null
        and tem_plano_saude is not null
        and teve_febre is not null
        and teve_dificuldade_respirar is not null
        and teve_dor_cabeca is not null
        and teve_fadiga is not null
        and teve_perda_cheiro is not null
    """
    df = run_query(query)
    return pd.DataFrame(df).dropna()

@st.cache_data
def _get_importance_data_allfeatures():
    query = """
    select 
          resultado_covid
        , uf
        , area_domicilio
        , idade
        , sexo
        , cor_raca
        , escolaridade
        , tem_plano_saude
        , situacao_domicilio
        , teve_febre
        , teve_dificuldade_respirar
        , teve_dor_cabeca
        , teve_fadiga
        , teve_perda_cheiro
    from
        fiap-tech-challenge-3.trusted_pnad.tb_f_covid_2020
    where
        resultado_covid in ('Sim','Não')
        and uf is not null
        and area_domicilio is not null
        and idade is not null
        and sexo is not null
        and cor_raca is not null
        and escolaridade is not null
        and tem_plano_saude is not null
        and situacao_domicilio is not null
        and teve_febre is not null
        and teve_dificuldade_respirar is not null
        and teve_dor_cabeca is not null
        and teve_fadiga is not null
        and teve_perda_cheiro is not null
    """
    df = run_query(query)
    return pd.DataFrame(df).dropna()