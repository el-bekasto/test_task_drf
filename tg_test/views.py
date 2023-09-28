from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.conf import settings
from .bot import Bot, Message
from . import serializers
from . import models


bot = Bot(settings.TOKEN)


class GetTokenAPIView(APIView):
    def get(self, request: Request):
        username = request.data.get('username')
        passwd = request.data.get('password')

        try:
            user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            user = None

        if not user:
            user = authenticate(username=username, password=passwd)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials!'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterAPIView(APIView):
    def post(self, request: Request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        user = models.User.objects.get(pk=Token.objects.get(key__exact=request.auth).user_id)
        if user.telegram_id:
            bot.notify_user(user, request.data['message'])
            return Response({'result': 'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'result': 'You did not link telegram bot to your token.'})


class BotAPIView(APIView):
    def post(self, request: Request):
        print('incoming telegram update...')
        if 'message' in request.data:
            msg = Message(request.data['message'])
            try:
                user = models.TgUser.objects.get(telegram_id=msg.from_user.id)
                if user.token is None:
                    try:
                        token = Token.objects.get(key__exact=msg.text)
                        user_obj = models.User.objects.get(pk=token.user_id)
                        user_obj.telegram_id = user.telegram_id
                        user.token = token.key
                        user_obj.save()
                        user.save()
                        bot.tokenregistered(msg.from_user, user_obj)
                    except Token.DoesNotExist:
                        bot.doesnotexist(msg.from_user)
            except models.TgUser.DoesNotExist:
                user = models.TgUser(
                    telegram_id=msg.from_user.id,
                    name=msg.from_user.first_name,
                    username=msg.from_user.username
                )
                user.save()
                bot.require_token(msg.from_user)
        return Response(status=status.HTTP_200_OK)
