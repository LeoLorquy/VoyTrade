import pandas as pd
import requests
import numpy as np

period = 15

def closing_bougies(symbol, interval, limit):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    return [float(candle[4]) for candle in data] # cloture

# RSI
def calculate_rsi(data, period=period):
    prices = pd.Series(data)
    delta = prices.diff()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)
    avg_gain = gains.ewm(span=period, adjust=False).mean()
    avg_loss = losses.ewm(span=period, adjust=False).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# MACD
def calculate_macd(symbol, interval, limit):
    closing_prices = closing_bougies(symbol, interval, limit)
    df = pd.DataFrame(closing_prices, columns=['close'])
    df['EMA12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['Histogram'] = df['MACD'] - df['Signal']
    return df[['MACD', 'Signal', 'Histogram']]

# Volume
def get_volumes(symbol, interval, limit):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    volumes = [float(candle[5]) for candle in data]
    average_volume = sum(volumes) / len(volumes)
    return volumes, average_volume

# RVOL
def calculate_rvol(prices):
    log_returns = np.log(np.array(prices[1:]) / np.array(prices[:-1]))
    variance = np.mean(log_returns ** 2)
    rvol = np.sqrt(variance)
    return rvol

def analyse_tendance(symbol, interval, limit):
    data = closing_bougies(symbol, interval, limit)
    volumes, average_volume = get_volumes(symbol, interval, limit)
    rvol = calculate_rvol(data) * 100
    rsi = calculate_rsi(data, period=period)
    macd = calculate_macd(symbol, interval, limit)

    # Dernières valeurs des indicateurs
    current_rsi = rsi.iloc[-1]
    current_macd = macd['MACD'].iloc[-1]
    current_signal = macd['Signal'].iloc[-1]
    current_histogram = macd['Histogram'].iloc[-1]
    current_volume = volumes[-1]

    # Initialisation des variables
    buy_signal = False
    sell_signal = False
    trend = "Neutre"
    trend_reverse_prob = 0.0

    # Analyse des indicateurs
    rsi_prob = 0
    macd_prob = 0
    volume_prob = 0

    # RSI
    # if current_rsi < 30:  # Surachat
    #     rsi_prob += 10
    #     trend = "Haussière"
    # elif current_rsi > 70:  # Survente
    #     rsi_prob += 20
    #     trend = "Baissière"

    if current_rsi > 70 and current_macd > current_signal:
        rsi_prob += 20
        trend = "Haussière"
    elif current_rsi < 30 and current_macd < current_signal:
        rsi_prob += 10
        trend = "Baissière"
    else:
        trend = "Neutre"


    # MACD
    if current_macd > current_signal:  # Tendance haussière
        macd_prob += 10
        if trend == "Haussière":
            macd_prob += 10  # Convergence haussière
    elif current_macd < current_signal:  # Tendance baissière
        macd_prob += 20
        if trend == "Baissière":
            macd_prob += 10  # Convergence baissière

    # Volume
    if current_volume > average_volume * 1.5:  # Activité inhabituelle
        volume_prob += 15
    elif current_volume < average_volume * 0.5:  # Faible activité
        volume_prob -= 10

    # Histogramme MACD
    if abs(current_histogram) > 4:
        macd_prob += 15

    # Calcul de la probabilité totale (normalisée)
    trend_reverse_prob = rsi_prob + macd_prob + volume_prob
    trend_reverse_prob = max(0, min(trend_reverse_prob, 100))  # Contraindre à [0, 100]

    # Détection des signaux avec conditions plus flexibles
    if trend == "Haussière":
        # Si la tendance est haussière et RSI indique surachat mais MACD reste fort
        if current_rsi > 70 and current_macd > current_signal:
            # On pourrait ajuster ici pour une possible correction avant d'acheter
            buy_signal = False
        elif current_rsi < 30 and current_macd > current_signal:
            # Un RSI bas dans une tendance haussière peut signaler une opportunité d'achat
            buy_signal = True
        else:
            buy_signal = False

    elif trend == "Baissière":
        # Si la tendance est baissière et RSI indique survente mais MACD reste faible
        if current_rsi > 70 and current_macd < current_signal:
            # On pourrait ajuster ici pour une vente dans une tendance baissière
            sell_signal = True
        elif current_rsi < 30 and current_macd < current_signal:
            # RSI bas dans une tendance baissière, indique plutôt un renforcement de la tendance
            sell_signal = False
        else:
            sell_signal = False


    # Retour des résultats
    return {
        "buy_signal": buy_signal,
        "sell_signal": sell_signal,
        "current_trend": trend,
        "trend_reverse_prob": trend_reverse_prob,
        "current_rsi": current_rsi,
        "current_macd": current_macd,
        "current_signal": current_signal,
        "current_histogram": current_histogram,
        "current_volume": current_volume,
    }

result = analyse_tendance('SOLUSDT', '1d', 26)
print(result)
