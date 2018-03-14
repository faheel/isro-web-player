# ISRO web player

## Setup

1. Clone the repo and **`cd`** into it:
   ```bash
   git clone https://github.com/faheel/isro-web-player.git
   cd isro-web-player
   ```

2. Create a Python 3 virtual environment (named `venv`):
   ```bash
   virtualenv -p /usr/bin/python3 venv
   ```

3. Add Django's secret key as an environment variable. For ease, add it to your virtual environment's activate script:
   ```bash
   printf "\nexport SECRET_KEY='enter secret key here'\n" >> venv/bin/activate
   ```

4. Activate your virtual environment:
   ```bash
   . venv/bin/activate
   ```

5. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

6. Migrate the database schema:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Run

```bash
python manage.py runserver
```
