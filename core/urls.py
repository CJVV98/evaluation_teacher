from django.urls import path,include # type: ignore
from . import views
from pages_visualization.urls import core_patterns_pages
from user_manage.urls import core_patterns_profile
from model_manage.urls import core_patterns_model

core_patterns_core = ([
    path('login', views.login, name='login'),
    path('main', views.main, name='main'),
    # Pages
    path('pages/', include(core_patterns_pages)),
    # User_Manage
    path('profile/', include(core_patterns_profile)),
    path('model/', include(core_patterns_model)),
], "core")
