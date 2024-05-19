from django.urls import path
from model_manage.views import *
core_patterns_model = ([
    path('page_training', page_training, name='page_training'),
], "model")