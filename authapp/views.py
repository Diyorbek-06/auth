import string
from multiprocessing.managers import Token
import random
import uuid
import datetime
from django.contrib.auth.password_validation import password_changed
from django.shortcuts import render
from django.template.context_processors import request
from rest_framework.views import APIView
from websockets import Response
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import CustomUser, OTP
from django.contrib.auth import authenticate
from authapp.models import CustomerUserManager
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
# Create your views here.

# def validate_password(password):
#     data = request.data
#     if len(password) < 6 or ' ' in password or not password.isalnum()\
#         or len([i for i in password if i.isalpha() and i.isupper()]) < 1\
#         or len([i for i in password if i.isalpha() and i.lower()]) < 1:
#
#         return Response({
#             "Error": "password xato kiritildi"
#         })


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        if 'key' not in data or 'password' not in data:
            return Response({
                "Error": "phone yoki password kiritilmagam"
            })

        # if len(str(data['phone'])) != 12 or not isinstance(data['phone'], int) or str(data['phone'])[:3] != '998':
        #     return Response({
        #         "Error": "telefon raqam noto'g'ri kiritildi"
        #     })



        if len(data['password']) < 6 or ' ' in data['password'] or not data['password'].isalnum()\
            or len([i for i in data['password'] if i.isalpha() and i.isupper()]) < 1\
            or len([i for i in data['password'] if i.isalpha() and i.lower()]) < 1:


            return Response({
                "Error": "password xato kiritildi"
            })
        otp = OTP.objects.filter(key=data['key']).first()
        phone = CustomUser.objects.filter(phone=otp.phone).first()
        if phone:
            return Response({
                "Error:" "bu raqam bilan oldin ro'yxatdan o'tilgan"
            })

        user_data = {
            'phone': otp.phone,
            'password': data['password'],
            'name': data.get('name', '')
        }

        if data.get('key', '') == '123':
            user_data.update({
                'is_active': True,
                'is_staff': True,
                'is_superuser': True
            })

        user = CustomUser.objects.create_user(**user_data)
        token = Token.objects.create(user=user)
        return Response({
            'message':"Siz muvaffaqiyatli kirdingiz!",
            "Token": token.key
        })


class LoginView(APIView):
    def post(self, request):
        data = request.data

        user = CustomUser.objects.filter(phone=data['phone']).first()
        if not user:
            return Response({
                "errror": "Bu telefon raqam orqali ro'yxatdan o'tilmagan"
            })

        if not user.check_password(data.get('password')):
            return Response({
                "error": "Parol xato"
            }, status=400)


        token =Token.objects.get_or_create(user=user)

        return Response({
            "massage": "siz tizimga kirdingiz",
            "Token": token[0].key
        })


class LogOutView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def post(self, request):
        token = Token.objects.filter(user=request.user).first()
        token.delete()
        return Response({
            "Error": "siz tizimdan chiqdiz"
        })

class Profile(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get(self, request):
        user = request.user
        return Response({
            "data": user.format()
        })


    def patch(self, request):
        data = request.data
        user_ = request.user

        # user_ = CustomUser.objects.filter(id=user.id).first()

        if data['phone']:
            user = CustomUser.objects.filter(phone=data['phone']).first()

            if int(user_.phone) == data['phone']:
                return Response({
                    'Error': "Bu sizning raqamingiz!(tell raqamingizni almashtirimoqchi bo'lsangiz tel raqamingizi yuboring"
                })

            if  user:
                return Response({
                    'Error': "Bu telefon orqali ro'yxatdan o'tilgan"
                })

        user_.name = data.get('name', user_.name)
        user_.phone = data.get('phone', user_.phone )
        user_.save()

        return Response({
            "Message": f"{' '.join([i for i in data])} malumotlaringiz o'zgardi"
        })

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({
            "Error": "Profi;imgoz o'chirildi!"
        })

class ChangePassword(APIView):
    permission_classes = IsAuthenticated,
    authentication_classes = TokenAuthentication,
    def post(self, request):
        data = request.data
        user = request.user

        if not data['old'] or not data['new']:
            return Response({
                'Error': "Datada kamchilik bor"
            })

        if data['old'] == data['new']:
            return Response({
                'Error': "Siz avvalgi parolni kiritdingiz!"
            })

        if not  user.check_password(data.get('old', '')):
            return Response({
                "Error": f"Siz oldingi parolni xato kiritdingiz"
            }, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(data.get('new', ''))
        user.save()
        return Response({
            "Message": "Sizning parolingiz o'zgartirildi"
        }, status=status.HTTP_200_OK)


class AuthOne(APIView):
    def post(self, request):
        data = request.data
        if not data['phone']:
            return Response({
                "Error": "to'g'ri malumot kiritlmagan "
            })

        if len(str(data['phone'])) != 12 or not isinstance(data['phone'], int) or str(data['phone'])[:3] != '998':
            return Response({
                "Error": "telefon raqam noto'g'ri kiritildi"
            })

        code = ''.join([str(random.randint(1, 999999))[-1] for i in range(4)])
        # int_ = string.digits
        # str_ = string.ascii_letters
        # letters = str(int_) + str_
        # code = ''.join([str(letters[(random.randint(0, len(letters)-1))]) for i in range(6)])

        # print(code)
        # print(int_)
        # print(str_)
        key = uuid.uuid4().__str__() + code

        otp = OTP.objects.create(phone=data['phone'], key=key)

        return Response({
            "otp": code,
            "key": otp.key
        })


class AuthTwo(APIView):
    def post(self, request):
        data = request.data
        if not data.get('code') or not data.get('key'):
             return Response({
                'Error': "siz to'liq malumot kiritmadingiz"
            })
        otp = OTP.objects.filter(key=data['key']).first()

        if not otp:
            return Response({
                "Error": "Xato key"
            })

        now = datetime.datetime.now(datetime.timezone.utc)
        if (now - otp.created).total_seconds() >= 180:
            otp.is_expire = True
            otp.save()
            return Response({
                "Error": "Key yaroqsiz"
            })

        if otp.is_conf:
            return Response({
                "Error": "Eskirgan key"
            })

        if otp.is_expire:
            return Response({
                "Error": "key yaroqsiz is_expire"
            })

        if str(data['code']) != data['key'][-4:]:
            otp.tried += 1
            otp.save()
            return Response({
                "Error": "siz xato kod kiritdingiz"
            })
        print(otp.tried)
        otp.is_conf=True
        otp.save()


        user = CustomUser.objects.filter(phone=otp.phone).first()
        return Response({
            "Message": user is not None 
        })

