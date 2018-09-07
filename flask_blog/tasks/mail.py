from flask_mail import Message
from app import celery
from extensions import mail
@celery.task()
def send_mail(subject,html,recipients,**kwargs):
    msg=Message(subject=subject,recipients=recipients,html=html)
    mail.send(msg)
