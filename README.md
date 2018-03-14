# ISRO web player

## Setup

```bash
virtualenv -p /usr/bin/python3 venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

## Run

```bash
python manage.py runserver
```
