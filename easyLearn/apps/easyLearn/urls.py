from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin


from . import views
urlpatterns = [
    url(r'^easylearn$', views.index),
    url(r'^process$', views.process),
    url(r'^trainings$', views.showDashboard),
    url(r'^home$', views.home),
    url(r'^trainings/(?P<training_id>\d+)$', views.showTrainingDetail),
    url(r'^trainings/(?P<training_id>\d+)/sections/(?P<section_id>\d+)$', views.startSection),
    url(r'^trainings/(?P<training_id>\d+)/sections/(?P<section_id>\d+)/activities/(?P<activity_id>\d+)$', views.startActivity),     
    url(r'^update/trainings/(?P<training_id>\d+)/sections/(?P<section_id>\d+)/activities/(?P<activity_id>\d+)$', views.updateActivity),   
    url(r'^update/trainings/(?P<training_id>\d+)/sections/(?P<section_id>\d+)/activities/(?P<nextActivity>\d+)$', views.updateActivity),    
    url(r'^completed/trainings/(?P<training_id>\d+)/sections/(?P<section_id>\d+)/activities/(?P<activity_id>\d+)$', views.completion),
    url(r'^logout$', views.logout),
    path('admin/', admin.site.urls),
]


