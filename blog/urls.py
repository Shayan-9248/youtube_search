from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('youtube.urls', namespace='youtube')),
    path('', include('accounts.urls', namespace='account')),
    path('captcha/', include('captcha.urls')),
]
