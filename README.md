# NERP

Nerp is an open source manufacturing ERP Application which companies can use to manage and monitor their businesses with flexible and easy-to-learn design.

###### Since this project is not ready for production yet, every function and module will not be shared. #######


## Installation 

Clone the project

```bash
git clone https://github.com/egebeyaztas/nerp.git
```

Install the requirements

```bash 
  pip install -r requirements.txt
  cd nerp
```

Configure the database with your Postgres Credentials

```bash
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
# This is the postgresql configuration if you want to 
# switch it from default SQLite configuration.
```

Make migrations and migrate to db

```bash
  python manage.py makemigrations
  python manage.py migrate
```

You can dump some dummy data to test the api at the moment

```bash
  python manage.py createsuperuser
  python manage.py runserver
```
## App Screenshots

##### This is the accountance module ######
![Screenshot](https://user-images.githubusercontent.com/77864932/230104903-256de0f1-0d5c-4927-8515-7c5864f79c60.jpg)

![Screenshot](https://user-images.githubusercontent.com/77864932/230105079-a95230d7-b5f4-4a46-b99e-ed3e00c3efb4.jpg)

  
### Where am I?

You can contact me if you want to contribute to this project and make ERP systems available in other business areas for free.

[Contact Me](https://www.linkedin.com/in/egebeyaztas/)

  
##



[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

  
