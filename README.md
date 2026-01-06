# Bettor

## Getting Started

### 1. Install Python (Mac)

Install pyenv:

```bash
brew install pyenv
```

Install Python:

```bash
pyenv install 3.13.5     
```

Switch to Python version:

```bash
pyenv local 3.13.5     
```

Verify Python and version

```bash
which python
python --version  
```

### 2. Set Up the Virtual Environment

In the root folder of the project. Start by creating a virtual environment for managing dependencies:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

### 3. Install Playwright

```bash
playwright install
```

## Usage

### Matches
```python
python main.py matches --coupon <MIDWEEK | SATURDAY | SUNDAY> --days <DAYS_OF_THE_MONTH_FOR_THE_COUPON>
```

#### Example
```python
python main.py matches --coupon MIDWEEK --days 7
```

### Predictions
```python
python main.py predictions --filename <DATA_FILE_PATH>
```

#### Example
```python
python main.py predictions --filename data/matches_2_2026_MIDWEEK.json
```

### Bets
```python
python main.py bets --filename <DATA_FILE_PATH> --balance <STARTING_BALANCE>
```

#### Example
```python
python main.py bets --filename data/matches_2_2026_MIDWEEK.json --balance 1000 
```

## About

The application uses statistical models to identify value bets and determine optimal stake sizes.

### True Probability

The "True Probability" ($P$) is the probability of a specific outcome (Home Win, Tie, or Away Win).

### Odds

The "Odds" ($O$) refer to the decimal odds offered by the bookmaker. 

### Expected Value (EV)

The Expected Value measures the profitability of a bet. It is calculated as the difference between the expected return
and the stake.

$$EV = (P \times O) - 1$$

Where:

- $P$ is the true probability (as a decimal between 0 and 1).
- $O$ is the decimal odds.

A positive EV indicates a value bet, meaning that over the long run, the bet is expected to be profitable.

### Kelly Criterion

The Kelly Criterion is a formula used to determine the optimal size of a series of bets. It balances risk and reward to
maximize the logarithm of wealth.

The optimal fraction of the bankroll to bet ($f^*$) is given by:

$$f^* = \frac{EV}{O - 1}$$

Where:

- $EV$ is the expected value.
- $O - 1$ is the net odds (odds minus the stake).

### Betting Configuration

The application uses a configuration file (`config.ini`) to set parameters for the betting strategy:

- **min_expected_value**: The minimum EV required to place a bet. Bets with EV below this threshold are ignored.
- **max_odds**: The maximum allowable odds. Bets with odds higher than this value are skipped (often to avoid high
  variance).
- **kelly_fraction**: A multiplier applied to the Kelly fraction ($f^*$). It is common to use a "Half Kelly" (0.5) or
  other fraction to reduce volatility.
