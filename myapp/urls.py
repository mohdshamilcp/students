"""students_details URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [
    path('login/', views.login),
    path('login_post/', views.login_post),
    path('signup/',views.signup),
    path('signup_post/',views.signup_post),
    path('userhome/',views.userhome),
    path('adminhome/',views.adminhome),
    path('viewprofile/',views.viewprofile),
    path('addcontact/',views.addcontact),
    path('addcontact_post/',views.addcontact_post),
    path('viewcontact/',views.viewcontact),
    path('viewcontact_post/',views.viewcontact_post),
    path('changepassword/', views.changepassword),
    path('changepassword_post/', views.changepassword_post),
    path('viewuser/',views.viewuser),
    path('sendcomplaint/', views.sendcomplaint),
    path('sendcomplaint_post/', views.sendcomplaint_post),
    path('viewcomplaint/',views.viewcomplaint),
    path('viewcomplaint_post/',views.viewcomplaint_post),
    path('viewreply/',views.viewreply),
    path('viewreply_post/',views.viewreply_post),
    path('sendreply/<id>', views.sendreply),
    path('sendreply_post/', views.sendreply_post),
    path('editprofile/',views.editprofile),
    path('editprofile_post/',views.editprofile_post),
    path('editcontact/<id>',views.editcontact),
    path('editcontact_post/',views.editcontact_post),
    path('deletecontact/<id>',views.deletecontact)


]
