import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_percentage_error
import seaborn as sns
from src.indicators import generate_graph
import src.get_data as get_data 

def _plot_trials(trials_df, hyperparam_1, hyperparam_2):
    from plotly import graph_objects as go
    fig = go.Figure(
        data=go.Contour(
            z=trials_df.loc[:, "loss"],
            x=trials_df.loc[:, hyperparam_1],
            y=trials_df.loc[:, hyperparam_2],
            contours=dict(
                showlabels=True,  # show labels on contours
                labelfont=dict(size=12, color="white",),  # label font properties
            ),
            colorbar=dict(title="loss", titleside="right",),
            colorscale='Hot',
            hovertemplate="loss: %{z}<br>"+hyperparam_1+": %{x}<br>"+hyperparam_2+": %{y}<extra></extra>",
        )
    )

    fig.update_layout(
        xaxis_title=hyperparam_1,
        yaxis_title=hyperparam_2,
        title={
            "text": f"{hyperparam_1} vs. {hyperparam_2} ",
            "xanchor": "center",
            "yanchor": "top",
            "x": 0.5,
        },
    )
    return fig
