from django.shortcuts import render
from .forms import UserData
from utils.data_utils import DataUtils
from django.http import JsonResponse
# Create your views here.


#Administración de usuarios
def page_profile(request):
    user=UserData.get_user_data()
    return render(request, 'profile/page_profile.html', context={'user': user})


def get_list_users(request):
    user = request.POST.get('user', None)
    list_users=DataUtils.get_data_list_users(str(user))
    return JsonResponse({'list_users': list_users})



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