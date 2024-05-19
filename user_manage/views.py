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
