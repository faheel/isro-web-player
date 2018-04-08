# ISRO web player

A web player for customized animation of satellite images, developed for ISRO as part of Smart India Hackathon 2018.

## Screenshots

Login | Upload | Config | Player
------|--------|--------|-------
![Login][screen-login] | ![Upload][screen-upload] | ![Config][screen-config] | ![Player][screen-player]

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

6. Create Django super-user:
   ```bash
   python manage.py createsuperuser
   ```

7. Migrate the database schema:
   ```bash
   python manage.py makemigrations
   python manage.py migrate --run-syncdb
   ```

## Run

```bash
python manage.py runserver
```

## Team

### Startroopers

* [Abdul Mohsin Siddiqi](https://github.com/mohsincl)
* [Gaurav Arora](https://github.com/gaurav61)
* [Kashan Uddin Zaigham Khan](https://github.com/kz-khan)
* [Mohd Huzaifa Faruqi](https://github.com/huzaifafaruqui)
* [Sahiba Khan](https://github.com/sahibakhan1006)
* [Syed Faheel Ahmad](https://github.com/faheel)

[screen-login]: screenshots/login.png
[screen-upload]: screenshots/upload.png
[screen-config]: screenshots/config.png
[screen-player]: screenshots/player.png

## License

This project is licensed under the terms of the [MIT license](LICENSE).
