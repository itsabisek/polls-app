from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(min_length=8, max_length=16, widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    username = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(label="Password", min_length=8, max_length=16, widget=forms.PasswordInput)


class NewPollForm(forms.Form):
    question = forms.CharField(label="Question", max_length=10000)
    choice_one = forms.CharField(label="Choice 1", max_length=100)
    choice_two = forms.CharField(label="Choice 2", max_length=100)
