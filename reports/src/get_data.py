import pandas as pd
import numpy as np
import config
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import geopandas as gpd
import pyproj
import json

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
        where
            resultado_covid in ('Sim')
    """
    df_casos_positivos = pd.DataFrame(run_query(query))
    # Criando tabela para verificar apenas pesquisas onde os resultados foram iguais a Sim
    # df_casos_positivos = df[df['resultado_covid'] == 'Sim']

    # Agregar e contar casos positivos por estado
    casos_positivos_por_estado = df_casos_positivos['uf'].value_counts().reset_index()
    casos_positivos_por_estado.columns = ['uf', 'Casos Positivos']

    shapefile_path = './reports/shapefile'
    mapa = gpd.read_file(shapefile_path).to_crs("WGS84").set_index('NM_UF')
    # return mapa
    # Junte o DataFrame `casos_positivos_por_estado` com o mapa usando a sigla dos estados
    # mapa = mapa.merge(casos_positivos_por_estado, left_on='NM_UF', right_on='uf', how='left')

    return mapa, casos_positivos_por_estado

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

@st.cache_data
def _get_sintomas_clinicos():
    query = """
      SELECT
        'teve_febre' questao,
        teve_febre resp,
        COUNT(teve_febre) total
      FROM
        `fiap-tech-challenge-3.trusted_pnad.tb_f_covid_2020`
      WHERE
        resultado_covid = 'Sim'
      GROUP BY
        teve_febre
      UNION ALL
      SELECT
        'teve_dificuldade_respirar' questao,
        teve_dificuldade_respirar resp,
        COUNT(teve_dificuldade_respirar) total
      FROM
        `fiap-tech-challenge-3.trusted_pnad.tb_f_covid_2020`
      WHERE
        resultado_covid = 'Sim'
      GROUP BY
        teve_dificuldade_respirar
      UNION ALL
      SELECT
        'teve_dor_cabeca' questao,
        teve_dor_cabeca resp,
        COUNT(teve_dor_cabeca) total
      FROM
        `fiap-tech-challenge-3.trusted_pnad.tb_f_covid_2020`
      WHERE
        resultado_covid = 'Sim'
      GROUP BY
        teve_dor_cabeca
      UNION ALL
      SELECT
        'teve_fadiga' questao,
        teve_fadiga resp,
        COUNT(teve_fadiga) total
      FROM
        `fiap-tech-challenge-3.trusted_pnad.tb_f_covid_2020`
      WHERE
        resultado_covid = 'Sim'
      GROUP BY
        teve_fadiga
      UNION ALL
      SELECT
        'teve_perda_cheiro' questao,
        teve_perda_cheiro resp,
        COUNT(teve_perda_cheiro) total
      FROM
      `fiap-tech-challenge-3.trusted_pnad.tb_f_covid_2020`
      WHERE
        resultado_covid = 'Sim'
      GROUP BY
        teve_perda_cheiro
    """
    df = run_query(query)
    return pd.DataFrame(df)#.dropna()

@st.cache_data
def _get_sintomas_clinicos_all():
    query = """
      SELECT
        'teve_febre' questao,
        teve_febre resp,
        resultado_covid,
        COUNT(teve_febre) total
      FROM
        `fiap-tech-challenge-3.trusted_pnad.tb_f_covid_2020`
      GROUP BY
        teve_febre,
        resultado_covid
      UNION ALL
      SELECT
        'teve_dificuldade_respirar' questao,
        teve_dificuldade_respirar resp,
        resultado_covid,
        COUNT(teve_dificuldade_respirar) total
      FROM
        `fiap-tech-challenge-3.trusted_pnad.tb_f_covid_2020`
      GROUP BY
        teve_dificuldade_respirar,
        resultado_covid
      UNION ALL
      SELECT
        'teve_dor_cabeca' questao,
        teve_dor_cabeca resp,
        resultado_covid,
        COUNT(teve_dor_cabeca) total
      FROM
        `fiap-tech-challenge-3.trusted_pnad.tb_f_covid_2020`
      GROUP BY
        teve_dor_cabeca,
        resultado_covid
      UNION ALL
      SELECT
        'teve_fadiga' questao,
        teve_fadiga resp,
        resultado_covid,
        COUNT(teve_fadiga) total
      FROM
        `fiap-tech-challenge-3.trusted_pnad.tb_f_covid_2020`
      GROUP BY
        teve_fadiga,
        resultado_covid
      UNION ALL
      SELECT
        'teve_perda_cheiro' questao,
        teve_perda_cheiro resp,
        resultado_covid,
        COUNT(teve_perda_cheiro) total
      FROM
      `fiap-tech-challenge-3.trusted_pnad.tb_f_covid_2020`
      GROUP BY
        teve_perda_cheiro,
        resultado_covid
    """
    df = run_query(query)
    return pd.DataFrame(df)#.dropna()