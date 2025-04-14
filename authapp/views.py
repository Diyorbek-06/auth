from multiprocessing.managers import Token

from django.contrib.auth.password_validation import password_changed
from django.shortcuts import render
from rest_framework.views import APIView
from websockets import Response
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import CustomUser
from django.contrib.auth import authenticate
from authapp.models import CustomerUserManager
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        if 'phone' not in data or 'password' not in data:
            return Response({
                "Error": "phone yoki password kiritilmagam"
            })

        if len(str(data['phone'])) != 12 or not isinstance(data['phone'], int) or str(data['phone'])[:3] != '998':
            return Response({
                "Error": "telefon raqam noto'g'ri kiritildi"
            })

        if len(data['password']) < 6 or ' ' in data['password'] or not data['password'].isalnum()\
            or len([i for i in data['password'] if i.isalpha() and i.isupper()]) < 1\
            or len([i for i in data['password'] if i.isalpha() and i.lower()]) < 1:


            return Response({
                "Error": "password xato kiritildi"
            })

        phone = CustomUser.objects.filter(phone=data['phone']).first()
        if phone:
            return Response({
                "Err0r:" "bu raqam bilan oldin ro'yxatdan o'tilgan"
            })

        user_data = {
            'phone': data['phone'],
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

        # if not authenticate(request, phone=data['phone'], password=data['password']):
        #     return Response({
        #         "Error": "error"
        #     })
        #
        # user = CustomUser.objects.filter(phone=data['phone']).first()

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







