from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', asosiy, name='asosiy'),
    path('fan/<int:fan_id>/', Fan_talabasi, name='Fan_talabasi'),
    path('talaba/<int:talaba_id>/', Talaba_haqida, name='Talaba'),
    path('add_fan/', add_fan, name='add_fan'),
    path('add_talaba/', add_talaba, name='add_talaba'),
    path('fan/<int:fan_id>/delete/', del_fan, name='del_fan'),
    path('talaba/<int:pk>/delete/', del_talaba, name='del_talaba'),
    path('talaba/<int:talaba_id>/pdf/', download_talaba_pdf, name='download_talaba_pdf'),
    path('talaba/<int:talaba_id>/update/', upd_talaba, name='upd_talaba'),
    path('fan/<int:fan_id>/update/', upd_fan, name='upd_fan'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)