"""
URL configuration for evaluation_teacher project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from core.urls import core_patterns_core
from pages_visualization.urls import core_patterns_pages
from model_manage.urls import core_patterns_model
from user_manage.urls import core_patterns_profile
from django.urls import path, include # type: ignore
from django.contrib.auth import views as auth_views # type: ignore

app_name = 'evaluation'
urlpatterns = [
    path('core/', include(core_patterns_core)), 
    path('pages/', include(core_patterns_pages)), 
    path('model/', include(core_patterns_model)), 
    path('profile/',include(core_patterns_profile))
]
