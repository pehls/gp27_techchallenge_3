import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_percentage_error
import seaborn as sns
import plotly.express as px
from plotly import graph_objects as go
import src.get_data as get_data 
import json

def _plot_data(df2):
    fig = go.Figure(
        data=go.Bar()
    )

    return fig


def _plot_modelo_completo(df):
    from sklearn.inspection import permutation_importance
    from sklearn.preprocessing import OneHotEncoder
    from imblearn.pipeline import Pipeline
    from imblearn.under_sampling import RandomUnderSampler
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    

    _features = list(set(df.columns) - set(['resultado_covid']))

    transform_pipeline = Pipeline(
        steps = [
            ('under', RandomUnderSampler(sampling_strategy='majority')),
            ('one-hot', OneHotEncoder(handle_unknown='infrequent_if_exist'))
        ]
    )

    pipeline = Pipeline(
        steps = [
            ('under', RandomUnderSampler(sampling_strategy='majority')),
            ('one-hot', OneHotEncoder(handle_unknown='infrequent_if_exist')),
            ('model', RandomForestClassifier(random_state=42))
        ]
    )

    X = df[_features]
    y = df[['resultado_covid']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)
    pipeline.fit(X_train, y_train)

    model = pipeline['model']
    y_pred = pipeline.predict(X_test)

    _y_test = [int(x.replace('Não','0').replace('Sim','1')) for x in y_test['resultado_covid'].to_list()]
    _y_pred = [int(x.replace('Não','0').replace('Sim','1')) for x in y_pred]

    result = permutation_importance(
        pipeline, X_test, y_test, n_repeats=10, random_state=42, n_jobs=2
    )
    forest_importances = pd.DataFrame([result.importances_mean, X.columns], index=['importance','feature']).T


    fig = px.bar(
        forest_importances.sort_values('importance'),
        x='importance', y='feature', orientation='h'
    )
    fig.update_layout(
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True
        ),
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True
        )
    )
    return fig

def _plot_inicial(crosstab):
    # Criando um gráfico empilhado.
    fig = px.bar(
        crosstab,
        x=crosstab.index, y=crosstab.columns,
        title="Distribuição dos Resultados de COVID-19 Empilhados por Mês (Excluindo 'NA')",
        color_discrete_map={
              'Ignorado':'purple'
            , 'Não' : 'red'
            , "Não sabe" : 'goldenrod'
            , 'Sim':'blue'
            }, text_auto=True
    )
    fig.update_layout(
        yaxis=dict(
            title='Número de Casos',
            showgrid=False,
            showline=False,
            showticklabels=True
        ),
        xaxis=dict(
            title='Mês',
            showgrid=False,
            showline=False,
            showticklabels=True
        )
    )
    return fig

def _plot_inicial_porcentagens(percentuais_por_mes):
    fig = px.line( 
        percentuais_por_mes,
        x='mes', y='value', 
        color='resultado_covid',  text='value',
        color_discrete_map={
              'Ignorado':'purple'
            , 'Não' : 'red'
            , "Não sabe" : 'goldenrod'
            , 'Sim':'blue'
            }
    )
    fig.update_traces(textposition="top right")
    fig.update_layout(
        yaxis=dict(
            title='% de Casos',
            showgrid=False,
            showline=False,
            showticklabels=True
        ),
        xaxis=dict(
            title='Mês',
            showgrid=False,
            showline=False,
            showticklabels=True
        )
    )
    return fig

def _map_plot(geodf, mapa):
    # Plot
    fig = go.Figure(
        go.Choroplethmapbox(geojson=json.loads(geodf.to_json()),
                            locations=geodf.index,
                            z=mapa["Casos Positivos"],)
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox=dict(center=dict(lat=-13.0918, lon=-53.2350),zoom=2)
        )
    # fig.update_geos(fitbounds="locations", visible=False)
    # fig = go.Figure(
    #     go.Choroplethmapbox(geojson=mapa.geometry, 
    #                         locations=mapa.uf, z=mapa["Casos Positivos"],
    #                         colorscale="Viridis", zmin=0, zmax=12,
    #                         marker_opacity=0.5, marker_line_width=0)
    # )
    # fig.update_layout(mapbox_style="carto-positron",
    #                   mapbox_zoom=3, 
    #                   mapbox_center = {"lat": 37.0902, "lon": -95.7129})
    return fig

def _plot_sintomas(questao_selecionada, df):
    questao_selecionada = 'teve_'+questao_selecionada.replace('?','').replace(' ','_').lower()
    df = df.loc[df.questao==questao_selecionada]
    fig = px.bar(
        df,
        x='resp', y='total',
        color='resultado_covid',
        title="Distribuição dos Resultados de COVID-19 Empilhados por Mês (Excluindo 'NA')",
        color_discrete_map={
              'Ignorado':'purple'
            , 'Não' : 'red'
            , "Não sabe" : 'goldenrod'
            , 'Sim':'blue'
            }, text_auto=True
    )
    fig.update_layout(
        yaxis=dict(
            title='Número de Casos',
            showgrid=False,
            showline=False,
            showticklabels=True
        ),
        xaxis=dict(
            title='Resposta',
            showgrid=False,
            showline=False,
            showticklabels=True
        )
    )
    return fig
