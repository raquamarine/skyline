# Skyline

A Discord bot with lua scripting

## Requirements

-   `python 3.8+`
-   `discord​.py`
- `lupa`

## Installation

**you will need git for both of them**

 Linux

```bash
# clone repo
git clone https://github.com/raquamarine/skyline.git
cd skyline
# create venv
python3 -m venv .venv

# activate venv
source .venv/bin/activate

# installs dependencies
pip install -r requirements.txt

#run
python -m bot
```

### Windows

```cmd
#clone repo
git clone https://github.com/raquamarine/skyline.git
cd skyline
# create venv
python -m venv .venv

# activate venv
.venv\Scripts\activate

# installs dependencies
pip install -r requirements.txt

#run
python -m bot
```

## Configuration

1.  create a `config.yaml` file in the parent directory (or use the example config provided):

```yaml
discord:
  token: "YOUR_BOT_TOKEN_HERE"

```
