from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from .forms import UserLoginForm, UserRegisterForm

# login view with authenticate aut from django
def login_view(request):
	next = request.GET.get('next')
	title = 'Login'
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		user = form.cleaned_data.get('user')
		password = form.cleaned_data.get('password')
		user = authenticate(username=user, password=password)
		login(request, user)
		if next:
			return redirect(next)
		return redirect('/posts')
	return render(request, 'user_login.html', { 'form': form, 'title':title })

# register_view register a new user with authenticate from django
def register_view(request):
	title = 'Registrar'
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username, password=password)
		login(request,new_user)
		return redirect('/posts')
	context = {
		'title':title,
		'form':form
		}
	return render(request, 'user_login.html', context)

# logout_view logout from app
def logout_view(request):
	logout(request)
	return redirect('/posts')
	return render(request, 'user_login.html',{})