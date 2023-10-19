import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, SeasonalNaive, SeasonalWindowAverage
from sklearn.metrics import mean_absolute_percentage_error
import seaborn as sns
from src.indicators import generate_graph
import src.get_data as get_data 


def _grafico_historico(df, crossovers):
    return generate_graph(df, crossovers, just_candles=False, just_return=True)

def _seasonal_decompose(series, period=5):
    result = seasonal_decompose(series, model='additive', period=period)
    return result.plot()

def _adf(df):
    df_ts = pd.DataFrame(df['Close'].to_list(), columns=['close'], index=df.index)
    df_ts.index = pd.to_datetime(df['Date'], dayfirst=True)
    ma = df_ts.rolling(12).mean()

    fig, ax = plt.subplots()
    df_ts.plot(ax=ax, legend=False)
    ma.plot(ax=ax, legend=False)

    return fig, df_ts.close.values

def _adf_diff(df):
    df_ts = pd.DataFrame(df['Close'].to_list(), columns=['close'])
    df_ts.index = pd.to_datetime(df['Date'], dayfirst=True)

    df_ts = df_ts.diff(1)

    ma = df_ts.rolling(12).mean()
    std = df_ts.rolling(12).std()

    fig, ax = plt.subplots()
    df_ts.plot(ax=ax, legend=False)
    ma.plot(ax=ax, legend=False)
    std.plot(ax=ax, legend=False)

    return fig, df_ts.dropna()['close'].values

def _models_ts():
    train, test, h = get_data._get_data_for_models_ts()
    
    model_all = StatsForecast(models=[
        SeasonalNaive(season_length=7),
        SeasonalWindowAverage(season_length=7, window_size=2),
        AutoARIMA(season_length=7)], freq='D', n_jobs=-1)
    
    model_all.fit(train)

    forecast_all = model_all.predict(h=h)
    forecast_all = forecast_all.reset_index().merge(test, on=['ds', 'unique_id'], how='left')
    forecast_all.dropna(inplace=True)

    mape_seas_naive = mean_absolute_percentage_error(forecast_all['y'].values, forecast_all['SeasonalNaive'].values)
    mape_seas_wa = mean_absolute_percentage_error(forecast_all['y'].values, forecast_all['SeasWA'].values)
    mape_arima = mean_absolute_percentage_error(forecast_all['y'].values, forecast_all['AutoARIMA'].values)
    graph = model_all.plot(train, forecast_all, unique_ids=['IBOV'], engine='plotly') 

    return graph, mape_seas_naive, mape_seas_wa, mape_arima

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

def _grafico_bb(df):
    # filtro para contemplar somente o ano de 2022
    df['Date'] = pd.to_datetime(df['Date'])
    df_2022 = df[(df['Date'] >= '2022-01-01') & (df['Date'] <= '2022-12-31')]

    # Configurações do Seaborn
    sns.set(style="whitegrid")

    # Plotando as Bandas de Bollinger para o ano de 2022 usando Seaborn
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_2022, x='Date', y='Upper_Band', label='Upper Band')
    sns.lineplot(data=df_2022, x='Date', y='Lower_Band', label='Lower Band')
    sns.lineplot(data=df_2022, x='Date', y='Close', label='Close Price', linestyle='dashed', color='black')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Bollinger Bands for 2022')
    plt.legend()
    plt.xticks(rotation=45)
    
    return plt

def _grafico_rsi(df):
    # filtro para contemplar somente o ano de 2022
    df['Date'] = pd.to_datetime(df['Date'])
    df_2022 = df[(df['Date'] >= '2022-01-01') & (df['Date'] <= '2022-12-31')]

    # Configurações do Seaborn
    sns.set(style="whitegrid")

    # Criando a figura com os dois gráficos
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plotando o gráfico de linha para o fechamento (Close) em 2022
    sns.lineplot(data=df_2022, x='Date', y='Close', color='blue', label='Close Price')

    # Configurações para o eixo do RSI
    ax2 = ax1.twinx()
    sns.lineplot(data=df_2022, x='Date', y='RSI', color='red', linestyle='dashed', ax=ax2)
    ax2.set_ylabel('RSI', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Adicionando as linhas horizontais para os níveis de sobrecompra e sobrevenda no eixo do RSI
    ax2.axhline(y=70, color='gray', linestyle='--', label='Overbought (70)')
    ax2.axhline(y=30, color='green', linestyle='--', label='Oversold (30)')

    # Configurações gerais
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Close Price', color='blue')
    ax2.legend(loc='upper right')  # Posiciona a legenda no canto superior direito
    ax1.legend(loc='upper left')
    ax1.set_title('Close Price and RSI Variation in 2022')
    ax1.grid(True)
    plt.xticks(rotation=45)

    return plt

def _grafico_macd(df):
    # filtro para contemplar somente o ano de 2022
    df['Date'] = pd.to_datetime(df['Date'])
    df_2022 = df[(df['Date'] >= '2022-01-01') & (df['Date'] <= '2022-12-31')]

    # Configurações do Seaborn
    sns.set(style="whitegrid")

    # Criando a figura
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plotando o Close no eixo esquerdo
    sns.lineplot(data=df_2022, x='Date', y='Close', ax=ax1, label='Close', color='black')
    ax1.set_ylabel('Close Price', color='black')
    ax1.tick_params(axis='y', labelcolor='black')

    # Criando um segundo eixo Y para o MACD e Signal Line
    ax2 = ax1.twinx()

    # Plotando o MACD e a linha de sinal no eixo direito
    sns.lineplot(data=df_2022, x='Date', y='MACD', ax=ax2, label='MACD', color='blue')
    sns.lineplot(data=df_2022, x='Date', y='Signal_Line', ax=ax2, label='Signal Line', color='red')
    ax2.set_ylabel('MACD and Signal Line', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    # Configurando limite do eixo direito
    ax2.set_ylim([-3000, 15000])

    # Configurando rótulos e título
    plt.title('Close Price, MACD, and Signal Line for 2022')
    plt.xlabel('Date')

    # Adicionando legenda
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    return plt