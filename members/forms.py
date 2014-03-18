from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext, ugettext_lazy as _
from members.models import *
import hashlib
import base64

def sha1(email):

    m = hashlib.sha1()
    m.update(email)

    return base64.b64encode(m.digest())

class AuthForm(forms.Form):

    username = forms.CharField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)

class SettingsForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ['email', 'first_name', 'last_name', 'rin']

class MemberChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75, label='Email address')
    rin = forms.IntegerField(max_value=999999999, required=False)

    class Meta:
        model = Member

    def clean_password(self):
        return self.initial["password"]

    def save(self, commit=True):
        member = super(MemberChangeForm, self).save(commit=False)
        member.username = sha1(member.email)
        member.save()
        return member

class MemberCreationForm(forms.ModelForm):

    email = forms.EmailField(max_length=75, label='Email address')
    first_name = forms.CharField(max_length=30)
    last_name= forms.CharField(max_length=30)
    rin = forms.IntegerField(max_value=999999999, required=False)
    password1 = forms.CharField(label=_('Password'),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password (again)'),
        widget=forms.PasswordInput,
        help_text=_('Enter the same password as above, for verification.'))

    class Meta:
        model = Member
        fields = ('email', 'first_name', 'last_name', 'rin',)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Member._default_manager.get(email=email)
        except Member.DoesNotExist:
            return email
        raise forms.ValidationError('A user with that email already exists.')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        member = super(MemberCreationForm, self).save(commit=False)
        member.username = sha1(member.email)
        member.set_password(self.cleaned_data['password1'])
        if commit:
            member.save()
        return member
