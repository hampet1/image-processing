# Flask Web App (Image processing): 
This app enable users to apply a kernel to their image and display the outcome transformation by choosing one of the color maps.


## Setup & Installtion

We assume that you have `git` and `virtualenv` and `virtualenvwrapper` installed.
```bash
Clone the code repository into ~/dev/my_app
mkdir -p ~/dev
cd ~/dev
git clone https://github.com/lingthio/Flask-User-starter-app.git my_app

Create the 'my_app' virtual environment
mkvirtualenv -p PATH/TO/PYTHON my_app

Install required Python packages
cd ~/dev/my_app
workon my_app
pip install -r requirements.txt

Create environment variable
set FLASK_ENV=development

```

## Config file


we have to set up DevelopmentConfig in config.py based on our own directory structure
example of configuration:


class DevelopmentConfig(Config):

    DEBUG = True
    UPLOADS = 'C:/Users/hamro/Desktop/app/app/static/images'
    SESSION_COOKIE_SECURE = False
    UPLOAD_FOLDER = "app/static/images/"
    PROCESSED_IMAGE = 'C:/Users/hamro/Desktop/app/app/static/images/'
    SEND_FILE_MAX_AGE_DEFAULT = 0

- [reference¶](http://flask.pocoo.org/docs/0.12/config/)


## Running The App

```bash
flask run
```
