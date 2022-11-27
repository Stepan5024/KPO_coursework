from datetime import datetime


import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()
from django.urls import path
from app.views import home , login , signup , add_todo , signout , delete_todo, change_todo


urlpatterns = [
   path('' , home , name='home' ), 
   path('login/' ,login, name='login'), 
   path('signup/' , signup ), 
   path('add-todo/' , add_todo ), 
   path('delete-todo/<int:id>' , delete_todo ), 
   path('change-status/<int:id>/<str:status>' , change_todo ), 
   path('logout/' , signout ), 
]
