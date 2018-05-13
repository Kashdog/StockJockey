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
from .models import Contest, Profile, Stock, StockEntry, Request, HeadToHeadMatch
import json
import sys
import requests
import time, datetime
import csv
import re

@ensure_csrf_cookie



# disabling csrf (cross site request forgery)
@csrf_exempt
def index(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Contest")
    table = cursor.fetchall()
    context = {
        #'engquery': engquery,
    }

    if request.user.is_authenticated:
        return render(request, 'mainpage.html', {'user': request.user})
    else:
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
def decidewin(request):
    decidewinreturn = []
    for match in HeadToHeadMatch.objects.filter():

        apiEndpoint = "https://query1.finance.yahoo.com/v7/finance/quote"
        fields = [
            'symbol',
            'regularMarketVolume',
            'regularMarketPrice',
            'regularMarketDayHigh',
            'regularMarketDayLow',
            'regularMarketTime',
            'regularMarketChangePercent']
        fields = ','.join(fields)
        symbols = match.user1.stocks.all()[0].name
        payload = {
            'lang': 'en-US',
            'region': 'US',
            'corsDomain': 'finance.yahoo.com',
            'fields': fields,
            'symbols': symbols}
        r = requests.get(apiEndpoint, params=payload)

        symbol = match.user1.stocks.all()[0].name
        #print("--------------------------------------------------")
        #print("Downloading %s to %s.csv" % (symbol, symbol))
        download_quotes(symbol)
        for i in r.json()['quoteResponse']['result']:
            print(i['regularMarketPrice'])
            user1endingstockprice = float(i['regularMarketPrice'])

        user1startingstockprice = float(stockarray[len(stockarray)-1][0].split(",")[1])
        user1profit = user1endingstockprice - user1startingstockprice
        print(user1startingstockprice)
        print(user1endingstockprice)
        print(user1profit)
    

        #print("--------------------------------------------------")
        #print("Downloading %s to %s.csv" % (symbol, symbol))

        apiEndpoint = "https://query1.finance.yahoo.com/v7/finance/quote"
        fields = [
            'symbol',
            'regularMarketVolume',
            'regularMarketPrice',
            'regularMarketDayHigh',
            'regularMarketDayLow',
            'regularMarketTime',
            'regularMarketChangePercent']
        fields = ','.join(fields)
        symbols = match.user2.stocks.all()[0].name
        payload = {
            'lang': 'en-US',
            'region': 'US',
            'corsDomain': 'finance.yahoo.com',
            'fields': fields,
            'symbols': symbols
        }
        r = requests.get(apiEndpoint, params=payload)
        for i in r.json()['quoteResponse']['result']:
            user2endingstockprice = float(i['regularMarketPrice'])

            
        symbol = match.user2.stocks.all()[0].name
        download_quotes(symbol)
        

        user2startingstockprice = float(stockarray[len(stockarray)-1][0].split(",")[1])
        user2profit = user2endingstockprice - user2startingstockprice
        print(user2startingstockprice)
        print(user2endingstockprice)
        print(user2profit)


        
        endtime = time.strftime("%H:%M:%S", time.localtime())

        if str(match.user1) == str(request.user.username) and user1profit > user2profit:
            decidewinreturn.append([match.user1.entryfee * 1.9, endtime])
        elif str(match.user1) == str(request.user.username) and user1profit < user2profit:
            decidewinreturn.append([0, endtime])
        elif str(match.user2) == str(request.user.username) and user1profit > user2profit:
            decidewinreturn.append([0, endtime])
        elif str(match.user2) == str(request.user.username) and user1profit < user2profit:
            decidewinreturn.append([match.user2.entryfee * 1.9, endtime])
    return decidewinreturn     

def headtoheadmatches(request):
    table = HeadToHeadMatch.objects.filter()
    whowon = decidewin(request)
    return render(request, 'headtohead_matches.html', {'data': table, 'results': whowon})

def match(request):
    if(Request.objects.filter(user=request.user.username, matched=False).count() > 0):
        userRequest = Request.objects.filter(user=request.user.username, matched=False)[0]
        userRequest.matched=True
        userRequest.save()
        while(Request.objects.exclude(user=request.user.username).filter(entryfee=userRequest.entryfee, length=userRequest.length, matched=False).count() < 1):
            pass
        opponentRequest = Request.objects.exclude(user=request.user.username).filter(entryfee=userRequest.entryfee, length=userRequest.length, matched=False)[0]
        opponentRequest.matched=True
        opponentRequest.save()
        m = HeadToHeadMatch(user1=userRequest, user2=opponentRequest)
        m.save()

def h2hrequest(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        q = Request(user=request.user.username)
        q.save()
        q.entryfee = body[0]['entryfee'] 
        q.length = body[0]['length']
        q.save()
        for x in range(1, len(body)):
            s = StockEntry(sector=body[x]['sector'], name=body[x]['name'], shares=body[x]['shares'])
            s.save() 
            q.stocks.add(s) 
        q.save()
        match(request)
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
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Stock ORDER BY sector")
    table = cursor.fetchall()

    

    prices = []
    counter = 0
    for x in table:
        download_quotes(table[counter][2])
        prices.append(round(float(stockarray[len(stockarray)-1][0].split(",")[1]), 2))
        counter = counter + 1
    
    return render(request, 'headtohead_lineup.html', {'data': table, "prices": prices})



stockarray = []

def get_cookie_value(r):
    return {'B': r.cookies['B']}

def get_page_data(symbol):
    url = "https://finance.yahoo.com/quote/%s/?p=%s" % (symbol, symbol)
    r = requests.get(url)
    cookie = get_cookie_value(r)
    lines = r.content.decode('unicode-escape').strip(). replace('}', '\n')
    return cookie, lines.split('\n')

def find_crumb_store(lines):
    # Looking for
    # ,"CrumbStore":{"crumb":"9q.A4D1c.b9
    for l in lines:
        if re.findall(r'CrumbStore', l):
            return l
    print("Did not find CrumbStore")

def split_crumb_store(v):
    return v.split(':')[2].strip('"')

def get_cookie_crumb(symbol):
    cookie, lines = get_page_data(symbol)
    crumb = split_crumb_store(find_crumb_store(lines))
    return cookie, crumb

def get_data(symbol, start_date, end_date, cookie, crumb):
    filename = '%s.csv' % (symbol)
    url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events=history&crumb=%s" % (symbol, start_date, end_date, crumb)
    response = requests.get(url, cookies=cookie)
    with open (filename, 'wb') as handle:
        for block in response.iter_content(1024):
            handle.write(block)
    with open('%s.csv' % (symbol), 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            stockarray.append(row)

def get_now_epoch():
    # @see https://www.linuxquestions.org/questions/programming-9/python-datetime-to-epoch-4175520007/#post5244109
    return int(time.time())

def download_quotes(symbol):
    start_date = get_now_epoch()
    end_date = get_now_epoch()
    if datetime.datetime.today().weekday() == 5:
        start_date = start_date - 60*60*24
        end_date = end_date - 60*60*24
    if datetime.datetime.today().weekday() == 6:
        start_date = start_date - 60*60*24*2
        end_date = end_date - 60*60*24*2
    cookie, crumb = get_cookie_crumb(symbol)
    get_data(symbol, start_date, end_date, cookie, crumb)
