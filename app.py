from config import db, seeder
from module_imports import *
from flask_cors import CORS
from flask_migrate import Migrate
from flask import Flask
import os
from dotenv import load_dotenv, find_dotenv
from flask_crontab import Crontab

load_dotenv(find_dotenv())


app = Flask(__name__)
crontab = Crontab(app)
CORS(app)

app.config.from_object(os.environ.get('CONFIGURATION_FILE'))

db.init_app(app)
migrate = Migrate(app, db, compare_type=True)
seeder.init_app(app, db)

############## Scheduled jobs ###############

crontab.init_app(app)
crontab.job(minute="0", hour="0")(notificationsJob)
crontab.job(minute="0", hour="0")(updateBillingDateJob)

############## Middlewares ###############

app.before_request_funcs = {
    'admin_admin_bp': [User.verify_token, User.verify_role],
    'admin_subscriptiontemplate_bp': [User.verify_token, User.verify_role],
    'client_subscription_bp': [User.verify_token, User.verify_role],
    'client_notification_bp': [User.verify_token, User.verify_role],
    'client_client_bp': [User.verify_token, User.verify_role],
}

############## Routes ###############

# General Routes
app.register_blueprint(session_bp, url_prefix='/sessions')
app.register_blueprint(client_bp, url_prefix='/clients')

# Admin routes
app.register_blueprint(admin_admin_bp, url_prefix='/admin/admins')
app.register_blueprint(admin_subscriptiontemplate_bp,
                       url_prefix='/admin/subscription-templates')

# Client User routes
app.register_blueprint(client_client_bp, url_prefix='/client/clients')
app.register_blueprint(client_subscription_bp,
                       url_prefix='/client/subscriptions')
app.register_blueprint(client_notification_bp,
                       url_prefix='/client/notifications')


@app.route('/')
def index():
    return {'Hello': 'World'}


if __name__ == '__main__':
    app.debug = True
    app.run(port=3399)
