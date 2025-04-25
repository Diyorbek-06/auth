from pyexpat.errors import messages
from rest_framework.authtoken.models import Token

from authapp.models import CustomUser
from methodism import custom_response, error_messages, MESSAGE
# from django.contrib import r

def regis(request, params):
    return {
        "bu regis": "regis"
    }
def login(request, params):

    if 'phone' not in params:
        return custom_response(False, error_messages.error_params_unfilled('phone'))


    if 'password' not in params:
        return custom_response(False, error_messages.error_params_unfilled('password'))

    user = CustomUser.objects.filter(phone=params['phone']).first()


    if not user:
        return custom_response(False, message=MESSAGE['Unauthenticated'])

    if not user.check_password(params.get('password')):
        return custom_response(False, message=MESSAGE['PasswordError'])


    token = Token.objects.get_or_create(user=user)

    return custom_response(True, data={"token": token[0].key}, message={"success": "Tizimga kirdingiz"})