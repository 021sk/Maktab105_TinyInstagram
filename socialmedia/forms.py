from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=250, required=True, label="username or phone",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=250, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
                               label='password')
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
                                label='password confirmation')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            }),
            'last_name': forms.TextInput(attrs={
                'class': "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            }),
            'phone_number': forms.TextInput(attrs={
                'class': "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            }),

        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('passwords do not match')
        return cd['password2']

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError('this phone number already exists')
        return phone


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'bio', 'photo',
                  'job']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            }),
            'first_name': forms.TextInput(attrs={
                'class': "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            }),
            'last_name': forms.TextInput(attrs={
                'class': "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            }),
            'phone': forms.TextInput(attrs={
                'class': "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            }),
            'email': forms.EmailInput(attrs={
                'class': "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            }),
            'bio': forms.TextInput(attrs={
                'class': "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            }),
            'photo': forms.FileInput(attrs={
                'class': "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            }),
            'job': forms.TextInput(attrs={
                'class': "w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            }),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if User.objects.exclude(id=self.instance.id).filter(phone_number=phone).exists():
            raise forms.ValidationError('this phone number already exists')
        return phone

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError('this username already exists')
        return username
