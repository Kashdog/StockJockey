# importing required packages
from __future__ import print_function
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, transaction
from itertools import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.views.decorators.csrf import ensure_csrf_cookie
import json
@ensure_csrf_cookie



# disabling csrf (cross site request forgery)
@csrf_exempt
def index(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Contest")
    table = cursor.fetchall()
    propertyNames = [col[0] for col in cursor.description]
    print(table[0][1])
    print(propertyNames)
    context = {
        #'engquery': engquery,
    }

    if request.user.is_authenticated:
        return render(request, 'mainpage.html', {'user': request.user})
    else:
        template = loader.get_template('index.html')
        return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Stockjockey account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')    
    else:
        return HttpResponse('Activation link is invalid!')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'index.html', {'error': "Incorrect username or password"})
def h2hrequest(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        from .models import Contest, Profile, Stock
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Stock ORDER BY sector")
        table = cursor.fetchall()
        return render(request, 'headtohead_lineup.html', {'data': table})
def signout(request):
    logout(request)
    return redirect('home')  
def mainpage(request):
    return redirect('home') 
def headtoheadlineup(request):
    from .models import Contest, Profile, Stock
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Stock ORDER BY sector")
    table = cursor.fetchall()
    return render(request, 'headtohead_lineup.html', {'data': table})   
