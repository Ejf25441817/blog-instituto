from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroUsuarioForm,PerfilUsuarioForm
from .models import Usuario

#registro de usuario
class RegistroUsuarioView(View):
    form_class = RegistroUsuarioForm
    template_name = 'usuarios/registro.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.Post)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f"Bienvenido {usuario.username}! Tu cuenta ha sido creada exitosamente.")
            return redirect('index')
        return render(request, self.template_name, {'form': form})
    
class LoginUsuarioView(View):
    template_name = 'usuarios/login.html'

    def get(self, request):
        form = AuthenticationForm()
        form.fields['username'].label = "Usuario"
        form.fields['username'].widget.attrs.update({'class': 'input-text', 'id': 'id_username','placeholder': 'Usuario'})
        form.fields['password'].widget.attrs.update({'class': 'input-text', 'id': 'id_password','placeholder': 'Contraseña'})
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        form.fields['username'].label = "Usuario"
        form.fields['username'].widget.attrs.update({'class': 'input-text', 'id': 'id_username','placeholder': 'Usuario'})
        form.fields['password'].widget.attrs.update({'class': 'input-text', 'id': 'id_password','placeholder': 'Contraseña'})

        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, f"Bienvenido {usuario.username}.")
            return redirect('index')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
        
        return render(request, self.template_name, {'form': form})
    
class PerfilDetalleView(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/perfil.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context
    
class PerfilUsuarioView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = PerfilUsuarioForm
    template_name = 'usuarios/editar_perfil.html'
    success_url = reverse_lazy('usuarios:perfil')

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Tu perfil ha sido actualizado exitosamente.")
        return super().form_valid(form)
    
class EliminarUsuarioView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'usuarios/eliminar_perfil.html')
    
    def post(self, request):
        usuario = request.user
        logout(request)
        usuario.delete()
        messages.success(request, "Tu cuenta ha sido eliminada exitosamente.")
        return redirect('index')
    
class LogoutUsuarioView(View):
    template_name = 'usuarios/logout.html'

    def post(self, request):
        logout(request)
        messages.success(request, "Has cerrado sesión exitosamente.")
        return redirect('index')