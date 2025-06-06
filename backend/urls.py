from django.contrib import admin
from django.urls import path, include
from tiffin.views import home

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('tiffin.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)