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

```python
python main.py matches --coupon <MIDWEEK|SATURDAY|SUNDAY> --days <DAYS_OF_THE_MONTH_FOR_THE_COUPON>
```

```python
python main.py predictions --filename <DATA_FILE_PATH>
```

```python
python main.py bets --filename <DATA_FILE_PATH> --balance <STARTING_BALANCE>
```