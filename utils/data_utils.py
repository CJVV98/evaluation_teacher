
from pages_visualization.models import Teacher
from pages_visualization.models import Evaluation
from pages_visualization.models import Calification
from pages_visualization.models import Control
from user_manage.models import User
from model_manage.models import Model
from mongoengine.queryset.visitor import Q # type: ignore
import functools


class DataUtils():
   
    def return_list_select(option, ciclo):
        list_select=[]
        if option=='1':  
            list_select_teacher=Teacher.objects().all().values_list('id_teacher', 'name')
            list_select = [{'id': teacher[0], 'description': teacher[1]} for teacher in list_select_teacher]
        if option=='2':
            list_select= list(Evaluation.objects.aggregate(Evaluation.get_courses(int(ciclo))))
        if option=='3':
            list_select= list(Calification.objects.aggregate(Calification.get_criteria(int(ciclo))))
        if option=='4':
            list_select=[
                {"id":0,"description":"Miedo"},
                {"id":1,"description":"Enojo"},
                {"id":2,"description":"Tristeza"},
                {"id":3,"description":"Sorpresa"},
                {"id":4,"description":"Alegria"},
                {"id":5,"description":"Confianza"},
                {"id":6,"description":"others"},
            ] 
        return list_select

    def get_courses_by_teacher(id_teacher,ciclo):
        courses=list(Teacher.objects.aggregate(Teacher.get_courses_by_teacher(id_teacher,ciclo)))
        return courses


    def get_info_teacher(id,name, ciclo): 
        emotions={ '[0]':"Miedo",'[1]':"Enojo",'[2]':"Tristeza",'[3]':"Sorpresa",'[4]':"Alegria",'[5]':"Confianza",'[6]':"Otras"}
        list_criterias=list(Evaluation.objects.aggregate(Evaluation.get_group_criterias_by_teacher(id,name,ciclo)))
        list_emotions=list(Evaluation.objects.aggregate(Evaluation.get_group_emotions_by_teacher(id,name,ciclo)))
        list_emotions_= [{'value_total': emotion['value_total'], 'value_class': emotions[emotion['value_class']]} for emotion in list_emotions]

        return list_emotions_,list_criterias

    def get_comments_by_teacher(id,ciclo,emotion):
        emotions={ "Miedo":'[0]',"Enojo":'[1]',"Tristeza":'[2]',"Sorpresa":'[3]',"Alegria":'[4]',"Confianza":'[5]',"Otras":'[6]'}
        name_emotion = emotions.get(emotion, 'Desconocido')
        print(name_emotion)
        list_comments=list(Evaluation.objects.aggregate(Evaluation.get_comments_by_teacher(int(id),int(ciclo),name_emotion)))
        return list_comments

    def get_list_alerts_criteria(ciclo):
        list_alerts=list(Control.objects.aggregate(Control.get_control(int(ciclo))))
        return list_alerts


    def get_data_list_users(user):
        list_users=list(User.objects.aggregate(User.get_users(user)))
        return list_users


    def get_data_model_training():
        list_training=list(Model.objects.aggregate(Model.get_data_model()))
        return list_training

    def counts_general(cycle):
        courses=list(Evaluation.objects.aggregate(Evaluation.count_courses(int(cycle))))
        teachers=list(Evaluation.objects.aggregate(Evaluation.count_teachers(int(cycle))))
        evaluations=list(Evaluation.objects.aggregate(Evaluation.count_evaluations(int(cycle))))
        return courses, teachers, evaluations


    def get_data_user(email_form, user_form):
        user= User.objects(Q(email=email_form) | Q(user=user_form))
        return user

    def create_modify_user(user_form):
        user=User.objects.filter(user=str(user_form['user'])).first()
        if user:
            user.names=str(user_form['names'])
            user.last_names=str(user_form['last_names'])
            user.password=str(user_form['password'])
        else:
            user=User(user=str(user_form['user']), password=str(user_form['password']), names=str(user_form['names']), 
                    last_names=user_form['last_names'], email=user_form['email'], profile=user_form['profile'], state=int(user_form['state']) )
        user.save()


    def modify_state(user,state):
        user=User.objects.filter(user=str(user)).first()
        user.state=state
        user.save()

    def get_list_data_count(cycle,id_teacher):
        list_data=list(Evaluation.objects.aggregate(Evaluation.get_general_data(int(cycle),int(id_teacher))))
        return list_data

    def get_count_comments(cycle,id_teacher):
        list_data=list(Evaluation.objects.aggregate(Evaluation.get_count_comments(int(id_teacher),int(cycle))))
        print(list_data)
        return list_data[0]['sum_comments']