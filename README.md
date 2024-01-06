# MarketPlace

## Install and start the virtual environment

Before all, install the virtual environment. on the root folder, type the command bellow.

```shell
python -m venv .venv
```

To start the created venv:

```shell
. .venv/bin/activate
```

## Saving packages

Before any commit, save the packages installed, typing the command bellow:

```shell
python -m pip freeze > requirements.txt
```

## Install packages

```shell
python -m pip install -r requirements.txt
```
