from django.contrib.auth import logout as log_out
from django.conf import settings
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import BlogsForm,ConsultationForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import smtplib
import requests


# BotScript
# Creating ChatBot Instance
chatbot = ChatBot(
    'CoronaBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand. I am still learning.',
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database.sqlite3-bot?check_same_thread=False'
) 

 # Training with Personal Ques & Ans 
# training_data_quesans = open('training_data/ques_ans.txt').read().splitlines()
# training_data_personal = open('training_data/personal_ques.txt').read().splitlines()

# training_data = training_data_quesans + training_data_personal

# trainer = ListTrainer(chatbot)
# trainer.train(training_data)

# # Training with English Corpus Data 
# trainer_corpus = ChatterBotCorpusTrainer(chatbot)
# trainer_corpus.train(
#     'chatterbot.corpus.english'
# ) 


#Homepage
def dashboard(request):
    news=News.objects.all()
    blogs=Blogs.objects.all()[:3:]
    return render(request, 'dashboard.html',{'news':news,'Blogs':blogs})

def news_single(request,news_id):
    blogs=Blogs.objects.all()
    news=get_object_or_404(News, pk = news_id)
    return render(request,'news_single.html',{'news':news,'Blogs':blogs})

# Auth0
def logout(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)


# Blogs
def all_blog(request):
	blogs=Blogs.objects.all()
	return render(request,'blog/all_blog.html',{'Blogs':blogs})
    
def details(request,blog_id):
    blogs=Blogs.objects.all()
    blog=get_object_or_404(Blogs, pk = blog_id)
    return render(request,'blog/blog-single.html',{'blog':blog,'Blogs':blogs})

@login_required
def createblog(request):
    blogs=Blogs.objects.all()
    if request.method=='GET':
        return render(request,'blog/createblog.html',{'form': BlogsForm(),'Blogs':blogs})
    else:
        form=BlogsForm(request.POST, request.FILES)
        if form.is_valid(): 
            newblog=form.save(commit=False)
            newblog.user=request.user
            newblog.save()
            return redirect('/blog/')
    return render(request,'blog/createblog.html',{'form': BlogsForm()})
    
# Bot
def get_bot_response(request):
    data = json.loads(request.body)
    message=data['msg']
    chat_response = chatbot.get_response(message).text
    return JsonResponse(f'{str(chat_response)}',safe=False)

# Fitness
def fitness(request):
    blogs=Blogs.objects.all()
    return render(request, 'fitness.html',{'Blogs':blogs})

# Diet
def diet(request):
    dietNews=DietNews.objects.all()
    blogs=Blogs.objects.all()
    return render(request, 'diet_nutrition.html',{'Blogs':blogs,'dietNews':dietNews})

def dietNews_single(request,news_id):
    blogs=Blogs.objects.all()
    news=get_object_or_404(DietNews, pk = news_id)
    return render(request,'news_single.html',{'news':news,'Blogs':blogs})

# departments
def departments(request):
    neurologyNews=NeurologyNews.objects.all()
    surgicalNews=SurgicalNews.objects.all()
    dentalNews=DentalNews.objects.all()
    ophthalmologyNews=OphthalmologyNews.objects.all()
    cardiologyNews=CardiologyNews.objects.all()
    blogs=Blogs.objects.all()
    return render(request, 'departments.html',{'Blogs':blogs,'neurologyNews':neurologyNews,'surgicalNews':surgicalNews,'dentalNews':dentalNews,'ophthalmologyNews':ophthalmologyNews,'cardiologyNews':cardiologyNews})

def neurologyNews_single(request,news_id):
    blogs=Blogs.objects.all()
    news=get_object_or_404(NeurologyNews, pk = news_id)
    return render(request,'news_single.html',{'news':news,'Blogs':blogs})

def surgicalNews_single(request,news_id):
    blogs=Blogs.objects.all()
    news=get_object_or_404(SurgicalNews, pk = news_id)
    return render(request,'news_single.html',{'news':news,'Blogs':blogs})

def dentalNews_single(request,news_id):
    blogs=Blogs.objects.all()
    news=get_object_or_404(DentalNews, pk = news_id)
    return render(request,'news_single.html',{'news':news,'Blogs':blogs})

def ophthalmologyNews_single(request,news_id):
    blogs=Blogs.objects.all()
    news=get_object_or_404(OphthalmologyNews, pk = news_id)
    return render(request,'news_single.html',{'news':news,'Blogs':blogs})

def cardiologyNews_single(request,news_id):
    blogs=Blogs.objects.all()
    news=get_object_or_404(CardiologyNews, pk = news_id)
    return render(request,'news_single.html',{'news':news,'Blogs':blogs})

# corona_updates
def corona_updates(request):
    blogs=Blogs.objects.all()
    url = "https://covid-193.p.rapidapi.com/statistics"
    querystring = {"country":"India"}
    headers = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': "804a107f73msh1d5c83ef1713700p153dcbjsnd92204077bac"
        }
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    d = response['response']
    s=d[0]
    context = {
        'all': s['cases']['total'],
        'recovered': s['cases']['recovered'],
        'deaths': s['deaths']['total'],
        'new': s['cases']['new'],
        'critical': s['cases']['critical'],
        'Blogs':blogs,
    }
    return render(request, 'corona_updates.html',context)

# hospital_medecine
def hospital_medecine(request):
    blogs=Blogs.objects.all()
    if request.method=='GET':
        return render(request, 'hospital_medecine.html',{'form': ConsultationForm(),'Blogs':blogs})
    else:
        server=smtplib.SMTP_SSL("smtp.gmail.com",465)
        server.login("drcareconsultation@gmail.com","Naman@123")
        server.sendmail("drcareconsultation@gmail.com","drcareconsultation@gmail.com",
        f"Name={request.POST['name']} \nEmail={request.POST['email']} \nPhone={request.POST['phone']} \nSymptoms={request.POST['symptoms']}")
        server.sendmail("drcareconsultation@gmail.com",f"{request.POST['email']}",
        f"Thank you for consulting with dr.care.Your query has been submitted successfully.We will contact you as soon as possible. \nName={request.POST['name']} \nEmail={request.POST['email']} \nPhone={request.POST['phone']} \nSymptoms={request.POST['symptoms']}")
        server.quit()
        form=ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/hospital_medecine/')
        return render(request, 'hospital_medecine.html',{'form': ConsultationForm()})


# eyeeartest
def eyeeartest(request):
    blogs=Blogs.objects.all()
    return render(request, 'eyeeartest.html',{'Blogs':blogs})

def eyeetest(request):
    blogs=Blogs.objects.all()
    return render(request, 'eyeetest.html',{'Blogs':blogs})

def eartest(request):
    blogs=Blogs.objects.all()
    return render(request, 'eartest.html',{'Blogs':blogs})



# def storefinder(request):
#     data = json.loads(request.body)
#     message=data['msg']
#     print(message)
#     API_KEY = 'AIzaSyBFwHoMoUlkAVQZPbts_D8bNpHIltS9DYA'
#     # print(message['lat'])
#     # Define the Client
#     gmaps = googlemaps.Client(key = API_KEY)
#     places_result  = gmaps.places_nearby(location=f"{message['lat']},{message['lng']}", radius = 5000, type = 'pharmacy')
#     # pprint.pprint(places_result)
#     time.sleep(2)
#     # place_result  = gmaps.places_nearby(page_token = places_result['next_page_token'])
#     # pprint.pprint(places_result)
#     lat=[]
#     lng=[]
#     names=[]      
#     for place in places_result['results']:
#         my_place_lat = place['geometry']['location']['lat']
#         my_place_lng = place['geometry']['location']['lng']
#         my_place_name = place['name']
#         lat.append(my_place_lat)
#         lng.append(my_place_lng)
#         names.append(my_place_name)
#     # print(*names)
#     context={'lat':lat,'lng':lng,'names':names}
#     return JsonResponse(str(context),safe=False)
