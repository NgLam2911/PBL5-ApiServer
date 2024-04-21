# SETUP
**REQUIRE Python 3.11 and lower**

## Create python virtual environment
### Windows
```bat
py -m venv venv
```
### Linux
```bash
python3 -m venv venv
```

## Activate venv
### Windows
```bat
venv\Scripts\activate
```
### Linux
```bash
source venv/bin/activate
```

## Install dependencies
```bash
pip install -r reqs.txt
```
* NOTE: If you failed to install all dependencies, try again with `--no-cache-dir` argument added.

## Run the server
### Windows
```bat
py main.py
```
### Linux
```bash
python3 main.py
```



