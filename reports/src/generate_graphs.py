import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_percentage_error
import seaborn as sns
import src.get_data as get_data 

def _plot_data(df2):
    from plotly import graph_objects as go
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
    import plotly.express as px

    _features = list(set(df.columns) - set('resultado_covid'))

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