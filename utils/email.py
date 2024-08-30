from django.core.mail import send_mail


def sendEmail(subject, message, html_message, to):
    send_mail(
        subject=subject,
        message=message,
        html_message=html_message,
        from_email=None,
        recipient_list=[to],
        fail_silently=False,
    )
