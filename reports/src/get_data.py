import pandas as pd
import numpy as np
import config
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import geopandas as gpd
import pyproj

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
def _get_initial_data():
    query = """
        select
              resultado_covid
            , mes
        from
            fiap-tech-challenge-3.trusted_pnad.tb_f_covid_2020
    """
    df = pd.DataFrame(run_query(query))
    # Criando tabela para verificar apenas pesquisas onde os resultados foram diferentes de 'NA'
    df_filtrado = df[df['resultado_covid'] != 'NA']

    # Criando uma tabela cruzada para contar os resultados por mês.
    crosstab = pd.crosstab(df_filtrado['mes'], df_filtrado['resultado_covid'])
    return crosstab

@st.cache_data
def _get_initial_data_percentage(crosstab = _get_initial_data()):
    percentuais_por_mes = crosstab.apply(lambda row: (row / row.sum()) * 100, axis=1).T.reset_index()
    percentuais_por_mes = percentuais_por_mes.round(2)
    return percentuais_por_mes.melt(id_vars=['resultado_covid'], value_vars=percentuais_por_mes.columns)

@st.cache_data
def _get_localizacao():
    query = """
        select
              resultado_covid
            , uf
        from
            fiap-tech-challenge-3.trusted_pnad.tb_f_covid_2020
    """
    df = pd.DataFrame(run_query(query))
    # Criando tabela para verificar apenas pesquisas onde os resultados foram iguais a Sim
    df_casos_positivos = df[df['resultado_covid'] == 'Sim']

    # Agregar e contar casos positivos por estado
    casos_positivos_por_estado = df_casos_positivos['uf'].value_counts().reset_index()
    casos_positivos_por_estado.columns = ['uf', 'Casos Positivos']

    shapefile_path = './reports/shapefile/bcim_2016_21_11_2018.gpkg'
    mapa = gpd.read_file(shapefile_path)
    return mapa
    mapa.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
    # Junte o DataFrame `casos_positivos_por_estado` com o mapa usando a sigla dos estados
    mapa = mapa.merge(casos_positivos_por_estado, left_on='nomeabrev', right_on='uf', how='left')

    return mapa


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