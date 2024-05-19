from django.urls import path
from .views import page_profile,get_list_users


core_patterns_profile = ([
    path('page_profile', page_profile, name='page_profile'),
    path('get_list_users', get_list_users, name='get_list_users'),
], "profile")