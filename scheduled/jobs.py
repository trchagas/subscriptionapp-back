from datetime import datetime, timedelta
from sqlalchemy import text

from config import db
from models.Notification import Notification


def notificationsJob():  #runs every day 00:00
    #cria notificação de que uma contínua chegou na data de pagamento
    #cria notificação de que uma não contínua terminou (muda o texto)
    raw = "SELECT id, client_id, name, next_bill, is_continuous FROM subscriptions WHERE DATE(next_bill) = DATE(NOW())"
    result = db.session.execute(raw).mappings().all()

    try:
        for subscription in result:
            if subscription.is_continuous:
                notificationTitle = "A inscrição de %s se renovará hoje."
            else:
                notificationTitle = "A inscrição de %s expira hoje."
            notification = Notification({
                "client_id":
                subscription.client_id,
                "title":
                notificationTitle % (subscription.name)
            })
            db.session.add(notification)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

def updateBillingDateJob():  #runs every day 00:00
    #verifica hoje
    #se for contínuo, atualiza, se não for, is_active=False
    raw = "SELECT id, client_id, name, next_bill, billing_cycle, is_continuous, is_active FROM subscriptions WHERE DATE(next_bill) = DATE(NOW())"
    result = db.session.execute(raw).mappings().all()

    try:
        for subscription in result:
            if subscription.is_continuous:
                subscription['next_bill'] = datetime.strptime(subscription['next_bill'], "%y-%m-%d") + timedelta(months=subscription['billing_cycle'])
            else:
                subscription['is_active'] = False
           
            subscription.update(subscription)
        db.session.commit()
    except Exception as e:
        print(e)

