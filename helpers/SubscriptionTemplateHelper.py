import os
from datetime import datetime
from models.SubscriptionTemplateIcon import SubscriptionTemplateIcon
from config import (FILES_TMP_PATH, S3_BUCKET, S3_DIRECTORY, s3_client)
from flask import abort, make_response

from config import db


class SubscriptionTemplateHelper:

    def updateIcon(icon, subscription_template):
        file_name = icon.filename.replace(' ', '-')
        fileTmpPath = "%s/%s" % (os.path.dirname(os.path.abspath(__file__)) +
                                 FILES_TMP_PATH, file_name)
        icon.save(fileTmpPath)
        file_name = "%s-%s" % (datetime.now().strftime('%Y-%m-%d-%H:%M:%S'),
                               file_name)

        key = "%s/icones-inscricoes/%s" % (S3_DIRECTORY, file_name)
        url = "https://s3-%s.amazonaws.com/%s/%s" % (
            s3_client.get_bucket_location(
                Bucket=S3_BUCKET)['LocationConstraint'], S3_BUCKET, key)
        try:
            s3_client.upload_file(fileTmpPath, S3_BUCKET, key)
            oldIcon = SubscriptionTemplateIcon.query.filter_by(
                subscription_template_id=subscription_template.id).first()
            if not oldIcon:
                icon = SubscriptionTemplateIcon(subscription_template.id, url, key)
                db.session.add(icon)
            else:
                oldKey = oldIcon.key
                oldIcon.key = key
                oldIcon.url = url
                db.session.merge(oldIcon)
                s3_client.delete_object(
                    Bucket=S3_BUCKET, Key=oldKey)  # old pic
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(make_response({'message': e}, 500))

        os.remove(fileTmpPath)
        return make_response(), 200

    def removeIcon(icon):
        try:
            s3_client.delete_object(Bucket=S3_BUCKET, Key=icon.key)
        except Exception as e:
            print(e)
            abort(make_response({'message': e}, 500))
