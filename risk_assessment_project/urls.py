from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('risk_app.urls')),  # подключаем urls приложения
]
