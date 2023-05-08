import os 

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') # the secret key is used to protect against modifying cookies and cross-site request forgery attacks
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') 

    MAIL_SERVER = 'smtp.googlemail.com'  # smtp server for gmail
    MAIL_PORT = 587  # port for gmail
    MAIL_USE_TLS = True  # encryption
    MAIL_USERNAME = os.environ.get("EMAIL_USER")  # email username
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")  # email password
