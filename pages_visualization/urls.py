from django.urls import path # type: ignore
from pages_visualization.views import *


core_patterns_pages = ([
    path('home', home, name='home'),
    path('change_emotion', change_emotion, name='change_emotion'),
    path('list_options',change_filter , name='list_options'),
    path('plots_teacher', plots_teacher, name='plots_teacher'),
    path('plots_courses',plot_courses , name='plots_courses'),
    path('plots_course_filter',plot_courses_filter , name='plots_course_filter'),
    path('get_comparatives',get_comparatives , name='get_comparatives'),
    path('plots_general', plots_general, name='plots_general'),
    path('get_alerts', get_alerts, name='get_alerts'),
    path('get_list_alerts',get_list_alerts , name='get_list_alerts'),
    path('get_counts_general',get_counts_general , name='get_counts_general'),
    path('plots_emotions_criterias_teacher_bar',plots_emotions_criterias_teacher_bar,name='plots_emotions_criterias_teacher_bar'),
    path('get_comments',get_comments,name="get_comments"),
], "pages")
