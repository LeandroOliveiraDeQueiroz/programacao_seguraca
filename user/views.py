from django.shortcuts import render

# Create your views here.
def login(request):
    context = {
        'title':'Broken Authentication and Section',
        'page' : 'Login Page',
     }

    return render(request, 'login.html', context)

def sign_up(request):
    context = {
        'title':'Broken Authentication and Section',
        'page' : 'Sign Up Page',
     }

    return render(request, 'sign_up.html', context)