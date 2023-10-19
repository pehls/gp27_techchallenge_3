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
