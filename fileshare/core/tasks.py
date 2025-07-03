from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_verification_email(email, verification_link):
    send_mail(
        subject='Verify your Email',
        message=f'Click to verify: {verification_link}',
        from_email='noreply@fileshare.com',
        recipient_list=[email],
        fail_silently=False,
    )
