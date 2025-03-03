from django import forms
from .models import *

class FanForm(forms.ModelForm):
    class Meta:
        model = Fan
        fields = ['nom']
        widget = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fan nomini kiriting'}),
        }

class TalabaForm(forms.ModelForm):
    class Meta:
        model = Talaba
        fields = ['ism_fam', 'sharf', 'tel_raqam', 'manzil', 'fan']
        widgets = {
            'ism_fam': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ism va Familiyani kiriting'}),
            'sharf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sharfni kiriting'}),
            'tel_raqam': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon raqamni kiriting'}),
            'manzil': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manzilni kiriting'}),
            'fan': forms.Select(attrs={'class': 'form-control'}),
        }