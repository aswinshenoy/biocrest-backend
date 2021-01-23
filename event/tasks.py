from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.html import strip_tags
from huey.contrib.djhuey import task


@task()
def send_email_confirming_registration(user, participant) -> None:
    data = {
        "name": user.title + ' ' + user.name,
        "eventName": participant.event.name
    }
    htmly = get_template('./emails/reg-approval.html')
    html_content = htmly.render(data)
    send_mail(
        subject='Amrita Biocrest: Registration Approved',
        message=strip_tags(html_content),
        from_email='biocrest@amritauniversity.info',
        recipient_list=[user.email],
        html_message=html_content,
        fail_silently=False,
    )


@task()
def send_email_requesting_correction(user, participant, editURL=None) -> None:
    data = {
        "remarks": participant.remarks,
        "eventName": participant.event.name,
        "editURL": editURL if editURL else 'https://events.amritauniversity.info/edit-profile',
    }
    htmly = get_template('./emails/verify-remarks.html')
    html_content = htmly.render(data)
    send_mail(
        subject='Amrita Biocrest: Corrections Requested',
        message=strip_tags(html_content),
        from_email='biocrest@amritauniversity.info',
        recipient_list=[user.email],
        html_message=html_content,
        fail_silently=False,
    )


__all__ = [
    'send_email_confirming_registration',
    'send_email_requesting_correction'
]
