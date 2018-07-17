# Utility functions

from django.core.mail import send_mail


def send_reset_password_email(email, from_email, full_name, reset_link, app_name):
    """
    Send password reset email
    :param email:
    :param from_email:
    :param full_name: 
    :param reset_link: 
    :param app_name: 
    :return: 
    """
    tpl = """

Hello {full_name},

Someone has requested a link to change your password. You can do this through the link below:

{reset_link}

If you didn't request this, please ignore this email.

Your password won't change until you access the link above and create a new one.

-- {app_name}
"""
    subject = '[' + app_name + '] Password reset instructions'
    msg_map = { 'full_name': full_name, 'reset_link': reset_link, 'app_name': app_name }
    message = tpl.format_map(msg_map)

    send_mail(subject, message, from_email, [email])
