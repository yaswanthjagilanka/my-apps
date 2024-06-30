from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), {'template_name': 'login.html', 'next_page': 'home'}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'template_name': 'logged_out.html', 'next_page': 'login'},
         name='logout'),
    path('signup/', views.signup, name='signup'),
    path('instructions/', views.instructions, name='instructions'),
    path('start_exam/', views.start_exam, name='start_exam'),

]
