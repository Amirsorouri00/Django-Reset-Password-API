from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from commons.permission_controllers import general_permission_controller as PERM_CONT
# Create your views here.

def test(request):
    return HttpResponse('In common/views/test.')

def permission_controller_test(request):
    permissions = {'healthrecords':'change_testrecord', 'healthstandards' : 'view_standardexamfieldmapping'
    , 'healthstandards' : 'add_standardexamfieldmapping'}
    
    user1 = User.objects.get(id = 1)
    print(user1)
    PERM_CONT(user1, **permissions)
    print('--------------------------------------------------------------')
    superuser = User.objects.get(username = 'amir')
    print(superuser)
    PERM_CONT(superuser, **permissions)
    return HttpResponse('in permission_controller_test: I Did It.')



from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse

@receiver(reset_password_token_created)
def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender:
    :param reset_password_token:
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        _("Password Reset for {title}".format(title="Some website title")),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()