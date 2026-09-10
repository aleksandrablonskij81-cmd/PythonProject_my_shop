from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user_email, username):
    subject = 'Добро пожаловать в наш магазин!'
    message = f'''
    Здравствуйте, {username}!

    Благодарим вас за регистрацию в нашем интернет-магазине.
    Теперь вы можете просматривать товары и управлять ими.

    С уважением,
    Команда MyShop
    '''
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )