## Getting Started

### 1. Install Python (Mac)

Install pyenv:

```bash
brew install pyenv
```

Install xz (if using M1 or M2 Mac):

```bash
brew install xz
```

Install Python:

```bash
pyenv install 3.13.5     
```

Switch to Python version:

```bash
pyenv local 3.13.5     
```

Verify Python version
```bash
python --version  
```

### 2. Set Up the Virtual Environment

In the root folder of the project. Start by creating a virtual environment for managing dependencies:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
source env/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```
