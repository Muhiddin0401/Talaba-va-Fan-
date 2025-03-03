from django.urls import path
from .views import *

urlpatterns = [
    path('', asosiy, name='asosiy'),
    path('fan/<int:fan_id>/', Fan_talabasi, name='Fan_talabasi'),
    path('talaba/<int:talaba_id>/', Talaba_haqida, name='Talaba'),
    path('add_fan/', add_fan, name='add_fan'),
    path('add_talaba/', add_talaba, name='add_talaba'),
path('talaba/<int:talaba_id>/pdf/', download_talaba_pdf, name='download_talaba_pdf'),
]