# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from .models import Client
from .models import SocialNetwork


'''
Constants
'''
ERROR_MESSAGE_USER = {'required' : 'El username es requerido', 'unique' : 'El username ya se encuentra registrado', 'invalid' : 'Ingresa un username válido'}
ERROR_MESSAGE_PASSWORD = {'required' : 'El password es requerido'}
ERROR_MESSAGE_EMAIL = {'required' : 'El email es requerido', 'invalid' : 'Ingresa un correo válido'}



'''
Functions
'''
def must_be_gt(value_password):
	if len(value_password) < 5:
		raise forms.ValidationError('El password debe contener al menos 5 caracteres')




'''
Class
'''

# Los formularios en Django hay que declararlos en una clase
class LoginUserForm(forms.Form):
	username = forms.CharField(max_length=20)
	password = forms.CharField(max_length=20, widget=forms.PasswordInput())

	# Constructor
	def __init__(self, *args, **kwargs):
		super(LoginUserForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update( {'id': 'username_login', 'class': 'input_login' } )
		self.fields['password'].widget.attrs.update( {'id': 'password_login', 'class': 'input_login' } )






# Formulario basado en Modelos
class CreateUserForm(forms.ModelForm):
	username = forms.CharField(max_length=20, error_messages = ERROR_MESSAGE_USER)
	password = forms.CharField(max_length=20, widget=forms.PasswordInput(), error_messages = ERROR_MESSAGE_PASSWORD)
	email = forms.CharField(error_messages = ERROR_MESSAGE_EMAIL)

	def __init__(self, *args, **kwargs):
		super(CreateUserForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update( {'id': 'username_create' } )
		self.fields['password'].widget.attrs.update( {'id': 'password_create' } )
		self.fields['email'].widget.attrs.update( {'id': 'email_create' } )

	# Validación de email
	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email = email).count():
			raise forms.ValidationError('El email ya existe')
		return email

	class Meta:
		model = User
		fields = ('username', 'password', 'email')





class EditUserForm(forms.ModelForm):
	username = forms.CharField(max_length=20, error_messages = ERROR_MESSAGE_USER)
	email = forms.CharField(error_messages = ERROR_MESSAGE_EMAIL)
	first_name = forms.CharField(label = 'Nombre(s)',required=False)
	last_name = forms.CharField(label='Apellidos',required=False)

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name')

	# Validación de email
	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email = email).exclude(pk=self.instance.id).count():
			raise forms.ValidationError('El email ya existe')
		return email




class EditPasswordForm(forms.Form):
	password = forms.CharField(max_length=20, widget=forms.PasswordInput())
	new_password = forms.CharField(max_length=20, widget=forms.PasswordInput(), validators=[must_be_gt])
	repeat_password = forms.CharField(max_length=20, widget=forms.PasswordInput(), validators=[must_be_gt])

	def clean(self):
		clean_data = super(EditPasswordForm,self).clean()
		password1 = clean_data.get('new_password')
		password2 = clean_data.get('repeat_password')

		if password1 != password2:
			raise forms.ValidationError('La contraseña no coincide')

	# def clean_new_password(self):
	# 	value_password = self.cleaned_data['new_password']
	# 	if len(value_password) < 5:
	# 		raise forms.ValidationError('El password debe contener al menos 5 caracteres')
	# 	value_password



class EditClientForm(forms.ModelForm):
	job = forms.CharField(label = "Trabajo actual", required=False)
	bio = forms.CharField(label = "Biografía", widget=forms.Textarea, required=False)
	class Meta:
		model = Client
		#fields = ('bio','job')
		exclude = ['user']



class EditClientSocial(forms.ModelForm):
	class Meta:
		model = SocialNetwork
		exclude = ['user']