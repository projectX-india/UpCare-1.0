# auth0login\urls.py
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    # Homepage
    path('', views.dashboard,name='dashboard'),
    path('news/<int:news_id>',views.news_single,name="news_single"),

    # Auth0
    path('logout', views.logout),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),

    # Blogs
    path('blog/',views.all_blog,name='all_blog'),
    path('blog/<int:blog_id>',views.details,name="details"),
    path('blog/create/',views.createblog,name='createblog'),

    #Bot
    path('get_bot_response/', views.get_bot_response,name='get_bot_response'),

    # Fitness
    path('fitness/',views.fitness,name='fitness'),

    # Diet
    path('diet/',views.diet,name='diet'),
    path('dietNews_single/<int:news_id>',views.dietNews_single,name="dietNews_single"),

    # departments
    path('departments/',views.departments,name='departments'),
    path('neurologyNews_single/<int:news_id>',views.neurologyNews_single,name="neurologyNews_single"),
    path('surgicalNews_single/<int:news_id>',views.surgicalNews_single,name="surgicalNews_single"),
    path('dentalNews_single/<int:news_id>',views.dentalNews_single,name="dentalNews_single"),
    path('ophthalmologyNews_single/<int:news_id>',views.ophthalmologyNews_single,name="ophthalmologyNews_single"),
    path('cardiologyNews_single/<int:news_id>',views.cardiologyNews_single,name="cardiologyNews_single"),

    # corona_updates
    path('corona_updates/',views.corona_updates,name='corona_updates'),

    # hospital_medecine
    path('hospital_medecine/',views.hospital_medecine,name='hospital_medecine'),

    # eyeeartest
    path('eyeeartest/',views.eyeeartest,name='eyeeartest'),
    path('eyeetest/',views.eyeetest,name='eyeetest'),
    path('eartest/',views.eartest,name='eartest'),
]