from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm
from django.contrib.auth.models import User
'''from django import forms'''
from django.contrib.auth import authenticate, password_validation as validator


# Create your views here.
def login(request):
    context = {
        'title':'Broken Authentication and Session Management',
        'page' : 'Login',
        'status': 'OK',
        'username' : '',
        'password' : '',
     }

    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            username = context['username'] = form.cleaned_data['username']
            password = context['password'] = form.cleaned_data['password']
            user = authenticate(request=request, username=username, password=password)

            if user is not None:
                # context['status'] = 'Logged'
                return HttpResponseRedirect('/loged/')
            else:
                context['status'] = 'authenticate_fail'

    return render(request, 'login.html', context)

def sign_up(request):
    context = {
                'title':'Broken Authentication and Session Management',
                'page' : 'Sign Up',
                'status': 'OK',
                'password_too_short' : False,
                'password_too_common': False,
                'password_entirely_numeric': False,
                'username' : '',
                'password' : '',
                'password_confirm' : '',
            }
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            username = context['username'] = form.cleaned_data['username']
            password = context['password'] = form.cleaned_data['password']
            password_confirm = context['password_confirm'] = form.cleaned_data['password_confirm']

            try:
                validator.validate_password(password)
            
                if password == password_confirm:
                    try:
                        user = User.objects.create_user(username=username, email='', password=password, first_name='', last_name='')
                        return HttpResponseRedirect('/login/')
                    except:
                        context['status'] = "username_already_exists"
                else :
                    context['status'] = "different_passwords"

            except validator.ValidationError as e:
                    context['status'] = "validation_error"
                    for error in e.error_list:
                        context[error.code] = True

    return render(request, 'sign_up.html', context)

def loged(request):
    return(HttpResponse("BATATA"))