from django.urls import path
from .views import page_profile,get_list_users,create_or_modify_user,change_state_user


core_patterns_profile = ([
    path('page_profile', page_profile, name='page_profile'),
    path('get_list_users', get_list_users, name='get_list_users'),
    path('create_or_modify_user', create_or_modify_user, name='create_or_modify_user'),
    path('change_state_user', change_state_user, name='change_state_user'),
], "profile")