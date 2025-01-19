# VoyTrade

**VoyTrade** est un outil d'analyse de tendance et de prise de décision pour le trading de cryptomonnaies. Ce projet exploite des indicateurs techniques populaires tels que le RSI, le MACD et les volumes pour fournir des signaux d'achat ou de vente et évaluer les probabilités de retournement de tendance.

---

## Fonctionnalités

1. **Analyse des tendances**
   - Identification de la tendance actuelle (haussière, baissière, neutre).
   - Calcul de la probabilité de retournement de tendance (évaluée en pourcentage).

2. **Indicateurs techniques**
   - **RSI (Relative Strength Index)** : Mesure la force de la tendance actuelle et identifie les zones de surachat/survente.
   - **MACD (Moving Average Convergence Divergence)** : Fournit des signaux haussiers ou baissiers basés sur la convergence/divergence des moyennes mobiles exponentielles.
   - **Volumes** : Analyse les volumes de transactions pour détecter des anomalies ou des confirmations de tendance.

3. **Génération de signaux**
   - Émission de signaux d'achat ou de vente basés sur une combinaison des indicateurs ci-dessus.
   - Détection des niveaux de surchauffe ou d'épuisement de la tendance.

---

## Prérequis

Pour exécuter VoyTrade, assurez-vous d'avoir les éléments suivants installés sur votre système :

- **Python 3.7+**
- Bibliothèques Python suivantes :
  - `pandas`
  - `requests`
  - `numpy`

---

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/LeoLorquy/voytrade.git
   ```

2. Naviguez dans le répertoire du projet :
   ```bash
   cd voytrade
   ```

3. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

---

## Utilisation

1. **Configuration** :
   - Le script utilise l'API de Binance pour récupérer les données du marché.
   - Assurez-vous d'avoir une connexion Internet active pour accéder aux données.

2. **Exécution du script** :
   Modifiez la fonction `analyse_tendance()` pour spécifier l'actif à analyser (par exemple, `SOLUSDT`) et l'intervalle de temps (par exemple, `1d`). Ensuite, exécutez le script :
   ```bash
   python voytrade.py
   ```

3. **Sortie** :
   Le script renvoie un dictionnaire contenant :
   - Signal d'achat ou de vente.
   - Tendance actuelle.
   - Probabilité de retournement de tendance.
   - Valeurs des indicateurs (RSI, MACD, Histogramme, Volume).

---

## Exemple de sortie

```json
{
  "buy_signal": false,
  "sell_signal": false,
  "current_trend": "Neutre",
  "trend_reverse_prob": 15.0,
  "current_rsi": 69.8,
  "current_macd": 3.05,
  "current_signal": 0.56,
  "current_histogram": 2.49,
  "current_volume": 128777.18
}
```

---

## Améliorations futures

- Intégration de davantage d'indicateurs techniques (Bollinger Bands, Ichimoku Cloud, etc.).
- Interface graphique pour une visualisation plus intuitive des tendances.
- Optimisation des paramètres pour des analyses adaptées à différents actifs.
- Intégration d'un backtesting pour évaluer les performances passées des stratégies.

---

## Contribution

Les contributions sont les bienvenues ! Si vous avez des idées ou des améliorations à proposer :

1. Forkez ce dépôt.
2. Créez une branche pour votre fonctionnalité :
   ```bash
   git checkout -b feature-nouvelle-fonctionnalite
   ```
3. Faites un pull request une fois vos modifications terminées.
