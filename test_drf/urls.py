
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('tg_test.urls')),
    path('admin/', admin.site.urls),
]
