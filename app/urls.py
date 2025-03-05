from django.urls import path
from .views import *

urlpatterns = [
    path('', asosiy.as_view(), name='asosiy'),
    path('fan/<int:fan_id>/', Fan_talabasi.as_view(), name='Fan_talabasi'),
    path('talaba/<int:talaba_id>/', Talaba_haqida.as_view(), name='Talaba'),
    path('add_fan/', add_fan, name='add_fan'),
    path('add_talaba/', add_talaba, name='add_talaba'),
    path('fan/<int:fan_id>/delete/', del_fan, name='del_fan'),
    path('talaba/<int:talaba_id>/delete/', del_talaba, name='del_talaba'),
    path('talaba/<int:talaba_id>/pdf/', download_talaba_pdf, name='download_talaba_pdf'),
    path('talaba/<int:talaba_id>/update/', upd_talaba, name='upd_talaba'),
    path('fan/<int:fan_id>/update/', upd_fan, name='upd_fan'),
]