# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from .models import Client
from .models import SocialNetwork

from django.shortcuts import render
from django.shortcuts import redirect
#from django.http import HttpResponse

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

from forms import LoginUserForm
from forms import CreateUserForm
from forms import EditUserForm
from forms import EditPasswordForm
from forms import EditClientForm
from forms import EditClientSocial

from django.views.generic import View
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.

'''
	Class
'''

class ShowClass(DetailView):
	model = User
	template_name = 'client/show.html'
	slug_field = 'username' # Campo de la base de datos por el cuál se va a filtrar
	slug_url_kwarg = 'username_url' # Que de la url

# Siempre que se asocie una funcion a una url, debe recibir como parametro un request
'''
def show(request):
	return HttpResponse("Hola desde el cliente")
'''





# ----- Autenticación de Usuario ----- #
class LoginClass(View):
	form = LoginUserForm()
	message = None
	template = 'client/login.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return redirect('client:dashboard')
		return render(request, self.template,self.get_context())

	def post(self, request, *args, **kwargs):
		username = request.POST['username']
		password = request.POST['password']
		# authenticate regresa un objeto del tipo User
		user = authenticate(username = username, password = password)
		if user is not None:
			# Con esto ya podemos usar el "user" dentro de las plataformas
			login_django(request, user)
			return redirect('client:dashboard')
		else:
			self.message = "Usuario o Contraseña incorrectos"

		return render(request, self.template,self.get_context())

	def get_context(self):
		return {'form':self.form, 'message':self.message}

'''
def login(request):
	if request.user.is_authenticated():
		return redirect('client:dashboard')

	message = None
	if request.method == 'POST': # Si esta recibiendo el formulario
		username = request.POST['username']
		password = request.POST['password']

		# authenticate regresa un objeto del tipo User
		user = authenticate(username = username, password = password)
		if user is not None:
			# Con esto ya podemos usar el "user" dentro de las plataformas
			login_django(request, user)
			return redirect('client:dashboard')
		else:
			message = "Usuario o Contraseña incorrectos"

	# Instanciamos el formulario
	form = LoginForm()

	context = {
		'form' : form,
		'message' : message
	}
	return render(request, 'login.html', context)
	'''





class DashboardClass(LoginRequiredMixin, View):
	# En caso de que no esté autenticado
	login_url = 'client:login'

	def get(self, request, *args, **kwargs):
		return render(request, 'client/dashboard.html', {})

'''
@login_required(login_url = 'client:login')
def dashboard(request):
	return render(request, 'dashboard.html', {})
'''








class CreateClass(CreateView):
	success_url = reverse_lazy('client:login') # reverse_lazy retorna la url completa
	template_name = 'client/create.html'
	model = User
	# Con fields, CreateView hace un formulario para renderizar en nustro html
	# fields = ('username','email')
	form_class = CreateUserForm

	# Encriptar password
	# El método form_valid regresa el objeto
	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.object.set_password(self.object.password) # Encriptar password
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())

'''def create(request):
	form = CreateUserForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			# commit = False Va a impedir que se almacence en la base de datos
			user = form.save(commit = False)
			user.set_password(user.password) # Encriptar password
			user.save()
			return redirect('client:login')

	context = {
		'form' : form
	}
	return render(request, 'create.html', context)
	'''




class EditSocialClass(LoginRequiredMixin,UpdateView,SuccessMessageMixin):
	login_url = 'client:login'
	model = SocialNetwork
	template_name = 'client/edit_social.html'
	success_url = reverse_lazy('client:edit_social')
	form_class = EditClientSocial
	success_message = "Tu usuario ha sido actualizado exitósamente"

	def get_object(self, queryset = None):
		return self.get_social_instance()

	def get_social_instance(self):
		try:
			return self.request.user.socialnetwork
		except:
			return SocialNetwork(user = self.request.user)





'''
	Functions
'''

@login_required(login_url = 'client:login')
def edit_password(request):
	form = EditPasswordForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			current_password = form.cleaned_data['password']
			new_password = form.cleaned_data['new_password']

			if authenticate(username = request.user.username, password = current_password):
				request.user.set_password(new_password)
				request.user.save()
				# Para que Django no nos saque de la sesión
				update_session_auth_hash(request, request.user)

				messages.success(request, 'Contraseña actualizada')
			else:
				messages.error(request, 'No es posible actualizar la contraseña')


	context = {'form' : form}
	return render(request, 'client/edit_password.html', context)



# ----- Cerrar Sesión de Usuario ----- #
@login_required(login_url = 'client:login')
def logout(request):
	logout_django(request)
	return redirect('client:login')





@login_required(login_url = 'client:login')
def edit(request):
	form_client = EditClientForm(request.POST or None, instance = client_instance(request.user))
	form_user = EditUserForm(request.POST or None, instance = request.user)
	if request.method == 'POST':
		if form_client.is_valid() and form_user.is_valid():
			form_user.save()
			form_client.save()
			messages.success(request, 'Datos actualizados correctamente')

	context = {
		'form_client' : form_client,
		'form_user' : form_user
	}

	return render(request, 'client/edit.html', context)




#----- Responder al cliente mediante un JSON -----#
# Forma 1
# from django.core import serializers	
# 	users = User.objects.filter(username__startswith=username) #Select * from users where username like '%username'
# 	# Serializar es tomar un objeto y convertirlo en un formato que se pueda enviar en http
# 	users = serializers.serialize('json',users)

# 	return HttpResponse(users,content_type='application/json')


# Forma 2
import json #Libreria nativa de Python


def user_filter(request):
	username = request.GET.get('username', '') #
	
	users = User.objects.filter(username__startswith=username) #Select * from users where username like '%username'
	users = [ user_serializer(user) for user in users ]

	
	
	return HttpResponse( json.dumps(users),
												content_type='application/json' )

def user_serializer(user):
	return {'id' : user.id, 'username' : user.username}







def client_instance(user):
	try:
		return user.client
	except:
		return Client(user = user)