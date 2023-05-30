import os
import boto3
from flask_sqlalchemy import SQLAlchemy
from flask_seeder import FlaskSeeder


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get("PRODUCTION_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("PRODUCTION_DATABASE_URL")
    # DEVELOPMENT is false by default
    # DEBUG is false by default


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = os.environ.get("DEVELOPMENT_SECRET_KEY")
    OAUTHLIB_INSECURE_TRANSPORT = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEVELOPMENT_DATABASE_URL")


# S3 config
S3_KEY = os.environ.get('S3_KEY')
S3_SECRET = os.environ.get('S3_SECRET')
S3_BUCKET = os.environ.get('S3_BUCKET')
S3_DIRECTORY = os.environ.get('S3_DIRECTORY')
S3_REGION = os.environ.get('S3_REGION')

# SES config
SES_REGION = os.environ.get('SES_REGION')
SES_KEY = os.environ.get('SES_KEY')
SES_ACCESS_KEY = os.environ.get('SES_ACCESS_KEY')

FILES_TMP_PATH = os.environ.get('FILES_TMP_PATH')

SECRET_KEY = os.environ.get('DEVELOPMENT_SECRET_KEY') if os.environ.get(
    'CONFIGURATION_FILE') == "config.DevelopmentConfig" else os.environ.get(
        'PRODUCTION_SECRET_KEY')

db = SQLAlchemy()
seeder = FlaskSeeder()

s3_client = boto3.client('s3',
                         aws_access_key_id=S3_KEY,
                         aws_secret_access_key=S3_SECRET,
                         region_name='sa-east-1')
s3_resource = boto3.resource('s3',
                             aws_access_key_id=S3_KEY,
                             aws_secret_access_key=S3_SECRET,
                             region_name='sa-east-1')
ses_client = boto3.client('ses',
                          aws_access_key_id=SES_KEY,
                          aws_secret_access_key=SES_ACCESS_KEY,
                          region_name='sa-east-1')
