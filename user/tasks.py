from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.html import strip_tags
from huey.contrib.djhuey import task


@task()
def send_otp_to_number(code, number) -> None:
    from django.conf import settings
    from requests import post
    SMS_API_URL = "http://alertbox.in/pushsms.php"
    DOMAIN = 'https://biocrest.com'

    template = """<#> {otp} is the OTP for your Amrita Biocrest registration. @{domain} #{otp}"""
    message = template.format(otp=code, domain=DOMAIN)
    data = {
        "username": settings.ALERTBOX_USERNAME,
        "api_password": settings.ALERTBOX_PASSWORD,
        "sender": settings.ALERTBOX_SENDER_ID,
        "to": number,
        "message": message,
        "priority": 4
    }
    r = post(SMS_API_URL, data=data)
    print(r.content)


@task()
def send_email_confirmation_email(user, code) -> None:
    data = {
        "name": user.username,
        "code": code,
    }
    htmly = get_template('./emails/email-verification.html')
    html_content = htmly.render(data)
    send_mail(
        subject='Biocrest: Verify Your Email',
        message=strip_tags(html_content),
        from_email='biocrest@amritauniversity.info',
        recipient_list=[user.email],
        html_message=html_content,
        fail_silently=False,
    )


__all__ = [
    'send_otp_to_number',
    'send_email_confirmation_email'
]
