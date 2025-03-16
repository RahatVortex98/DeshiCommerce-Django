from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from core.views import product

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',include('category.urls')),
    
    path('', product, name='home'),
    path('store/',include('store.urls')),
    path('cart/',include('carts.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
