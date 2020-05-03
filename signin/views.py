from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'title':'Broken Authentication and Section',
        'page' : 'Sign Up Page',
     }

    return render(request, 'sign_in_view.html', context)