from django.shortcuts import render # type: ignore
from django.views.generic.edit import CreateView # type: ignore
from django.urls import reverse # type: ignore
from .forms import UserForm
from django.contrib.auth import authenticate  # type: ignore
from utils.plots_utils import PlotsUtils
from user_manage.models import User
from django.shortcuts import redirect # type: ignore

from django.contrib import messages  # type: ignore
from django.utils.crypto import get_random_string  # type: ignore
from user_manage.forms import UserData
def login(request):
   
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user=form.cleaned_data['user']
            password=form.cleaned_data['password']
            user_valid = User.validate_user(user, password)          
            if user_valid is not None:
                #load_file('/Users/corinviracacha/Documents/Proyectos/ProyectoEvaluacionDocente/evaluation_teacher/utils/resources/dataset_test.csv')
                UserData.set_user_data(user_valid)
                return redirect(reverse('core:main') + '?module_data=' + get_random_string(16))
        form = UserForm(request.POST)
        messages.error(request, 'Usuario y/o contraseña incorrecta')
        return render(request, 'core/login.html', {'form': form})
    form = UserForm()
    return render(request, 'core/login.html', {'form': form})


def main(request):
    plot_div_donut=PlotsUtils.generate_donut_emotions('2330')
    plot_bar_cal=PlotsUtils.generate_bar_calification('2330')
    plot_bar_table=PlotsUtils.generate_top_calification("5",'2330'),

    return render(request, 'core/main.html', context={'plot_div_donut': plot_div_donut,'plot_div_bar':plot_bar_cal,
                                                      'plot_div_table':plot_bar_table})


def page_alerts(request):
    list_alerts=PlotsUtils.generate_donut_emotions('2330')
    return render(request, 'pages/main.html', context={'list_alerts': list_alerts})

