from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('api/', include('exam.urls'))
]

if settings.DEBUG:
    urlpatterns.append(path('rest-auth/', include('rest_framework.urls'))
                       )
