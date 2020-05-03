from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'title':'Broken Authentication and Section',
        'page' : 'Login Page',
     }

    return render(request, 'login_view.html', context)