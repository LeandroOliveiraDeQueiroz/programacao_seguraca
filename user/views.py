from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as user_login, password_validation as validator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import UserForm
from user.models import QRCode

#2FA Two Factor Authentication
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile

from urllib.parse import urlparse, parse_qs
import qrcode
import base64
import io

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
            totp_token = context['totp_token'] = form.cleaned_data['totp_token']
            user = authenticate(request=request, username=username, password=password)

            if user is not None:
                device = get_user_totp_device(user, confirmed=True)

                if device != None and device.verify_token(totp_token):                  
                    user_login(request, user)
                    return HttpResponseRedirect('/loged/')
                else:
                    context['status'] = 'authenticate_fail'
            else:
                context['status'] = 'authenticate_fail'

    return render(request, 'login.html', context)

def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device

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
                        device = user.totpdevice_set.create(name="IPG_" + username, confirmed=True)

                        request.session["username"] = username
                        request.session["user_id"] = user.id
                        request.session["device_config_url"] = device.config_url
                        request.session["device_id"] = device.id
                        request.session["device_key_type"] = "Baseada no horário"

                        return HttpResponseRedirect('/show-totpdevice/')
                    except:
                        context['status'] = "username_already_exists"
                else :
                    context['status'] = "different_passwords"

            except validator.ValidationError as e:
                    context['status'] = "validation_error"
                    for error in e.error_list:
                        context[error.code] = True

    return render(request, 'sign_up.html', context)

@login_required(login_url='/forbidden/')
def loged(request):
    return render(request, 'index.html')

def forbidden(request):
    return render(request, 'forbidden.html')


def show_totpdevice(request):
    
    if(request.session and request.session.get("device_config_url") and 
        request.session.get("device_key_type") and request.session.get("user_id")):

        url = urlparse(request.session["device_config_url"])
        query = parse_qs(url.query)

        qr = qrcode.make(request.session["device_config_url"])
        qrcode_image = QRCode.objects.create(user_id=request.session["user_id"], 
            url= request.session["device_config_url"], qrcode= convert_to_file(qr))

        context = {
            'title':'Broken Authentication and Session Management',
            'page' : 'TOTP Device',
            'username': request.session["username"],
            'device_config_url': request.session["device_config_url"],
            'device_name': url.path[1:],
            'device_key': query['secret'][0],
            'device_key_type': request.session["device_key_type"],
            'device_id': request.session["device_id"],
            'qr': qrcode_image.qrcode.url
        }

        request.session.clear()

        return render(request, 'show_totpdevice.html', context)
    else:
        return HttpResponseRedirect('/forbidden/')

def convert_to_file(qr):
    qr_io = io.BytesIO()
    qr.save(qr_io, format='JPEG')
    qr_io.seek(0)
    qr_file = InMemoryUploadedFile(qr_io, None, 'qr.jpg', 'image/jpeg',qr_io.getbuffer().nbytes, None)

    return qr_file