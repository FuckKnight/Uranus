from django import forms

class LoginMassage(forms.Form):
    usrName = forms.CharField(max_length=20)
    usrPassword = forms.CharField(max_length=20)

class RegisterForm(forms.Form):
    #nickName = forms.CharField(max_length=20)
    usrName = forms.CharField(max_length=20)
    usrPassword = forms.CharField(max_length=20)
    subPassword = forms.CharField(max_length=20)
    email = forms.EmailField()
    
