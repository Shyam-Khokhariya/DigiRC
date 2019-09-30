from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('root.urls')),
    path('', include('users.urls')),
    path('manufacturer/', include('manufacturer.urls')),
    path('dealer/', include('dealer.urls')),
    path('buyer/', include('buyer.urls')),
    path('rto/', include('rto.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
