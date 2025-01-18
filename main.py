import pandas as pd
import requests
import numpy as np

period = 15

def closing_bougies(symbol, interval, limit):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    return [float(candle[4]) for candle in data]  # Récupère uniquement les prix de clôture

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

# Analyse de la tendance
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

    # Détection des signaux d'achat ou de vente
    if current_rsi < 30 and current_macd > current_signal:
        buy_signal = True
        trend = "Haussière"
        trend_reverse_prob = 20  # Faible probabilité de retournement

    elif current_rsi > 70 and current_macd < current_signal:
        sell_signal = True
        trend = "Baissière"
        trend_reverse_prob = 40  # Probabilité modérée de retournement

    # Analyse des volumes
    if current_volume > average_volume * 1.5:
        if trend == "Neutre":
            trend_reverse_prob += 10
        elif trend in ["Haussière", "Baissière"]:
            trend_reverse_prob -= 10

    # Ajustement selon les indicateurs de surchauffe
    if current_rsi > 85 or current_histogram > 4:
        trend_reverse_prob += 20

    # Limitation de la probabilité
    trend_reverse_prob = max(0, min(trend_reverse_prob, 100))

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

# Test
result = analyse_tendance('SOLUSDT', '1d', 26)
print(result)
