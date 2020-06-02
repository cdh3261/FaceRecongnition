from .models import Info, Menu
from django import forms


class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ('uName', 'uPhone', 'uBirthDay',)
        widgets = {
            'uBirthDay': forms.TextInput(attrs={'maxlength': 8, 'size': 20, 'placeholder': '예시: 19990101'}),
            'uPhone': forms.TextInput(attrs={'maxlength': 11, 'size': 20, 'placeholder': '예시: 01012349876'})
        }


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('americano', 'latte', 'smoothy', 'total')
        widgets = {
            'americano': forms.TextInput(attrs={'size': 2, 'value': 0, 'id': 'id_americano', 'style': "border: none; background: transparent; text-align:right;", 'readonly': True, 'onclick': 'change1();'}),
            'latte': forms.TextInput(attrs={'size': 2, 'value': 0, 'id': 'id_latte', 'readonly': True, 'style': "border: none; background: transparent; text-align:right;", 'onclick': 'change2();'}),
            'smoothy': forms.TextInput(attrs={'size': 2, 'value': 0, 'id': 'id_smoothy', 'readonly': True, 'style': "border: none; background: transparent; text-align:right;", 'onclick': 'change3();'}),
            'total': forms.TextInput(attrs={'size': 3, 'value': 0, 'id': 'id_total', 'readonly': True, 'style': "border: none; background: transparent; text-align:right; padding-right:3px;"}),
        }
