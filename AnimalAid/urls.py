"""AnimalAid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from core import forms

from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', core_views.home, name="home"),
    path('', core_views.home, name="home"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='core/password/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="core/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='core/password/password_reset_complete.html'), name='password_reset_complete'), 
    path('login/', core_views.login, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', core_views.signup, name = "signup"),
    path('results/', core_views.results, name="results"),
    path('dogs/', core_views.dog_list, name="dog_list"),
    path('dogs/edit_dog/', core_views.edit_dog, name="edit_dog"),
    path('dogs/add_dog/', core_views.add_dog, name="add_dog"),
    path('walker_profile/', core_views.edit_walker, name="edit_walker"),
    path('walker_signup/', core_views.walker_signup, name="walker_signup"),
    url(r'^ajax/validate_username/$', forms.validate_username, name='validate_username'),
    url(r'^ajax/validate_password1/$', forms.validate_password1, name='validate_password1'),
    url(r'^ajax/validate_password2/$', forms.validate_password2, name='validate_password2'),
    url('dog_gallery/', core_views.dog_gallery, name="dog_gallery"),
    path('', core_views.home, name="home"),
    path('s3direct/', include('s3direct.urls')),
    path('match/', core_views.match, name="match")
    
]
