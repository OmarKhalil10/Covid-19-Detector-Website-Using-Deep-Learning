import os 

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
SECRET_KEY=os.environ.get('SECRET_KEY')
DEBUG = True
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'johnaziz269@gmail.com'
MAIL_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')