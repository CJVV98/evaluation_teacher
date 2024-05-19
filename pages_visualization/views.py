from django.shortcuts import render  # type: ignore
from utils.plots_utils import PlotsUtils
from utils.data_utils import DataUtils
from django.http import JsonResponse  # type: ignore




# Create your views here.
def home(request):
    plot_div_donut=PlotsUtils.generate_donut_emotions('2330')
    plot_div_bar=PlotsUtils.generate_bar_calification('2330')
    plot_div_table=PlotsUtils.generate_top_calification("5",'2330')
 
    return render(request, 'pages/home_page.html', context={'plot_div_donut': plot_div_donut,
                                                            'plot_div_bar':plot_div_bar,
                                                            'plot_div_table':plot_div_table})

def change_filter(request):
    option = request.POST.get('option', None)
    ciclo = request.POST.get('ciclo', None)
    list_options = DataUtils.return_list_select(option,ciclo)     
    return JsonResponse({'list_options': list_options})

def plots_teacher(request):
    id_teacher = request.POST.get('id_teacher', None)
    name = request.POST.get('name', None)
    ciclo = request.POST.get('ciclo', None)

    list_courses=DataUtils.get_courses_by_teacher(int(id_teacher),int(ciclo))
    list_emotions, list_criterias=DataUtils.get_info_teacher(int(id_teacher),name,int(ciclo))
    plot_bar=PlotsUtils.generate_subburt_emotions(int(id_teacher),name, int(ciclo))
    plot_donut_data,total_student=PlotsUtils.get_general_info(ciclo,id_teacher)
    total_comments=DataUtils.get_count_comments(ciclo,id_teacher)
    return render(request, 'pages/plots_teacher.html',context={'list_courses': list_courses,
                                                                'name_teacher':name,
                                                                'total_student':total_student,
                                                                'total_comments':total_comments,
                                                                'id_teacher':id_teacher,
                                                                'plot_sunburst':plot_bar,
                                                                'list_emotions':list_emotions,
                                                                'list_criterias':list_criterias,
                                                                'plot_donut_data': plot_donut_data})

def plot_courses (request):
    id_course = request.POST.get('id_course', None)
    name = request.POST.get('name', None)
    ciclo = request.POST.get('ciclo', None) 
    plot_bar_course_emotions, sum_emotion_by_cycle=PlotsUtils.generate_bar_groups_courses_emotions(int(id_course),name, ciclo)
    plot_bar_course_criterias,mean_by_criteria_course, count_teacher=PlotsUtils.generate_bar_groups_courses_criterias(int(id_course), ciclo)

    return render(request, 'pages/plots_courses.html',context={'plot_bar_course_emotions': plot_bar_course_emotions,
                                                               'name':name,
                                                               'count_teacher':count_teacher,
                                                               'sum_emotion_by_cycle':sum_emotion_by_cycle,
                                                               'mean_by_criteria_course':mean_by_criteria_course,
                                                               'plot_bar_course_criterias': plot_bar_course_criterias})


def plots_general(request):
    ciclo = request.POST.get('ciclo', None) 
    plot_div_donut=PlotsUtils.generate_donut_emotions(ciclo)
    plot_div_bar=PlotsUtils.generate_bar_calification(ciclo)
    plot_div_table=PlotsUtils.generate_top_calification("5",ciclo)
    return render(request, 'pages/plots_general.html', context={'plot_div_donut': plot_div_donut,
                                                            'plot_div_bar':plot_div_bar,
                                                            'plot_div_table':plot_div_table})

def get_comparatives(request):
    id_teacher = request.POST.get('id_teacher', None)
    name_teacher= request.POST.get('name_teacher', None)
    plot_criterias,mean_by_cycle = PlotsUtils.generate_bubble_criterias(int(id_teacher)) 
    plot_emotions,sum_by_cycle = PlotsUtils.generate_bubble_emotions(int(id_teacher))
    list_emotions_by_cycle = [(grupo, suma) for grupo, suma in sum_by_cycle.items()]
    list_survey_by_cycle = [(grupo, suma) for grupo, suma in mean_by_cycle.items()]

    print(type(sum_by_cycle))
    return render(request, 'pages/pages_comparative.html', context={'plot_criterias': plot_criterias,
                                                            'plot_emotions':plot_emotions, 'name_teacher':name_teacher,
                                                            'sum_by_cycle':list_emotions_by_cycle,
                                                             'median_by_cycle':list_survey_by_cycle})

def get_alerts(request):
    return render(request, 'pages/home_alerts.html')

def change_emotion(request):
    option= request.POST.get('option', None)
    ciclo= request.POST.get('ciclo', None)
    plot_div_bar=PlotsUtils.generate_top_calification(option,ciclo)
    return JsonResponse({'plot_div_bar': plot_div_bar})

def get_comments(request):
    emotion = request.POST.get('emotion', None)
    ciclo = request.POST.get('ciclo', None)
    id_teacher = request.POST.get('id_teacher', None)
    list_options = DataUtils.get_comments_by_teacher(id_teacher,ciclo,emotion)    
    return JsonResponse({'list_comments': list_options})

def get_list_alerts(request):
    ciclo = request.POST.get('ciclo', None)
    list_alerts=DataUtils.get_list_alerts_criteria(int(ciclo))
    return JsonResponse({'list_alerts': list_alerts})

def plots_emotions_criterias_teacher_bar(request):
    id_teacher = request.POST.get('id_teacher', None)
    name = request.POST.get('name', None)
    ciclo = request.POST.get('ciclo', None)
    is_emotion = request.POST.get('is_emotion', None)
    if(is_emotion=='true'):
        plot_bar=PlotsUtils.generate_subburt_emotions(int(id_teacher),name, int(ciclo))
    else:
       plot_bar=PlotsUtils.generate_subburt_criterias(int(id_teacher),name, int(ciclo)) 
    return JsonResponse({'plot_bar':plot_bar})
   
def get_counts_general(request):
    cycle = request.POST.get('cycle', None)
    print(int(cycle))
    courses,teachers,evaluations=DataUtils.counts_general(int(cycle))
    print(courses,teachers,evaluations)
    return JsonResponse({'courses':courses,'teachers':teachers,'evaluations':evaluations})


def create_or_modify_user(request):
    user_form = request.POST.get('user')
    is_edit = bool(request.POST.get('create'))
    email_form = request.POST.get('email')
    user=DataUtils.get_data_user(email_form, user_form)
    if(user and not(is_edit)):
        data = {'error': 'El usuario o correo ya se encuentra en uso'}
        return JsonResponse(data, status=400)
    else:
        names_form= request.POST.get('names')
        last_names_form= request.POST.get('lastNames')
        password_form= request.POST.get('password')
        user={'names':names_form, 
              'password':password_form,
              'user':user_form,
              'last_names':last_names_form,
              'email':email_form,
              'profile':"Docente",
              'state':1}
        DataUtils.create_modify_user(user)
        data = {'error': 'Registro exitoso'}
        return JsonResponse(data, status=200)
    
def change_state_user(request):
    user_form = request.POST.get('user')
    state = int(request.POST.get('state'))
    state= 0 if state==1 else 1
    DataUtils.modify_state(user_form, state)
    return JsonResponse( {'error': 'Cambio exitoso'}, status=200)