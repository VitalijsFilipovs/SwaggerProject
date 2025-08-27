from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    ROLE_CHOICES = (('renter', 'Renter'), ('landlord', 'Landlord'))
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, initial='renter')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
            # сохранить роль в профиле
            role = self.cleaned_data["role"]
            profile = user.profile  # создан сигналом post_save
            profile.role = role
            profile.save()
        return user
