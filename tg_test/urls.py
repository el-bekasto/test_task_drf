from django.urls import path
from . import views
from django.conf import settings

import requests

urlpatterns = [
    path('api/v1/register', views.RegisterAPIView.as_view(), name='register'),
    path('api/v1/token', views.GetTokenAPIView.as_view(), name='auth'),
    path('api/v1/sendMessage', views.SendMessageAPIView.as_view(), name='sendMessage'),
    path('webhook', views.BotAPIView.as_view(), name='webhook')
]

# r = requests.get(
#     f'{settings.TELEGRAM_API_URL}/setWebhook?url=https://8c40-85-117-100-67.ngrok-free.app/webhook'
# )
# print(r.text)

