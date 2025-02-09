from django.urls import path
from . import views
from templates import *
from .views import login_view, signup_view, logout_view, test, income_view, home_view,outcome_view

urlpatterns = [
      path('login/',login_view,name='login'),
      path('signup/',signup_view,name='signup'),
      path('logout/',logout_view,name='logout'),
      path('',login_view,name='default'),



      path('home/', home_view, name='home'),
      path('income/', income_view, name='income'),
      path('outcome/', outcome_view, name='outcome'),

]
