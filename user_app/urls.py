from django.contrib import admin
from django.urls import path
from .views import register,login_view
from . import views
from django.contrib.auth import views as auth_views
from user_app import views
#from django.urls import path,include
from django.views.generic import RedirectView
urlpatterns = [
    path('',views.home,name='home'),
    #path('',include('django.contrib.auth.urls')),
    #path('user_app/',include('user_app.urls')),
    path('favicon.ico',RedirectView.as_view(url='/static/favicon.ico')),
    path('register/', views.register,name='register'),
    path('login/',views.login_view,name='login'),
    path('profile/',views.profile,name='profile'),
    path('reset_password/',views.reset_password,name='reset_password'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset/confirm/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
    
]