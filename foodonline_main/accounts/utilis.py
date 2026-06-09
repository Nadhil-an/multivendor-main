from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
import ssl
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

ssl._create_default_https_context = ssl._create_unverified_context


def detectUser(user):
    if user.role == 1:   # Vendor
        return 'vendorhome'
    elif user.role == 2:  # Customer
        return 'home'
    else:
        return 'loginUser'

def send_verification_email(request, user, email_template, mail_subject):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)

    context = {
        'user': user,
        'domain': current_site.domain,  # IMPORTANT
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }

    html_message = render_to_string(email_template, context)
    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject=mail_subject,
        body=plain_message,
        from_email=from_email,
        to=[user.email],
    )

    email.attach_alternative(html_message, "text/html")
    email.send()

def send_approve_mail(mail_template,context,mail_subject):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template,context)
    to_email = context['user'].email
    mail = EmailMessage(mail_subject,message,from_email,to=[to_email])
    mail.content_subtype = 'html'
    mail.send()

def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL

    # Render template properly so {% for %} works
    message = render_to_string(mail_template, context)

    # Get receiver email
    if isinstance(context['to_email'], str):
        to_email = [context['to_email']]
    else:
        to_email = [context['to_email'].email]

    # Send email
    mail = EmailMessage(
        subject=mail_subject,
        body=message,
        from_email=from_email,
        to=to_email     # <-- correct
    )
    
    mail.content_subtype = 'html'
    mail.send()



