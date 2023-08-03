# signals.py
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ReviveUser
from .models import CrisisManage
from django.conf import settings

# @receiver(post_save, sender=CrisisManage)
# def send_crisis_added_email(sender, instance, created, **kwargs):
#     if created:  # Only send the email for new instances, not updates
#         users = ReviveUser.objects.all()
#         subject = 'New Crisis Added'
#         message = f'A new crisis has been added: {instance.title}. Check it out!'
#         from_email = settings.DEFAULT_FROM_EMAIL  # Replace this with your desired sender email
#         recipient_list = [user.email for user in users]
#         send_mail(subject, message, from_email, recipient_list)





@receiver(post_save, sender=CrisisManage)
def send_crisis_added_email(sender, instance, created, **kwargs):
    if created and instance.is_active:  # Send email only for new instances with is_active as True
        users = ReviveUser.objects.all()
        subject = 'New Crisis Added'
        message = f'A new crisis has been added: {instance.title}. Check it out!'
        from_email = settings.DEFAULT_FROM_EMAIL  # Replace this with your desired sender email
        recipient_list = [user.email for user in users]
        send_mail(subject, message, from_email, recipient_list)

@receiver(post_save, sender=CrisisManage)
def send_crisis_activated_email(sender, instance, **kwargs):
    if instance.is_active:  # Send email only when the crisis is activated (is_active changed to True)
        users = ReviveUser.objects.all()
        subject = 'Crisis Activated'
        message = f'The crisis has been activated: {instance.title}. Check it out!'
        from_email = settings.DEFAULT_FROM_EMAIL  # Replace this with your desired sender email
        recipient_list = [user.email for user in users]
        send_mail(subject, message, from_email, recipient_list)
