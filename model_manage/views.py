from django.shortcuts import render  # type: ignore
from utils.data_utils import DataUtils
from utils.plots_utils import PlotsUtils
from utils.model.supportVectorMachine import ModelSupportVectorMachine
from django.http import JsonResponse  # type: ignore
# Create your views here.


def page_training(request):
    list_data=DataUtils.get_data_model_training()
    plot_heat_map=PlotsUtils.get_heat_map(list_data[0]['matrix'])
    return render(request, 'model/page_training.html', context={'list_data':list_data,
                                                                'plot_heat_map':plot_heat_map})


def trainig_model(request):

    parameter_c = request.POST.get('parameter_c', None)
    parameter_gamma = request.POST.get('parameter_gamma', None)
    parameter_random = request.POST.get('parameter_random', None)
    count_comments = request.POST.get('count_comments', None)
    kernel = request.POST.get('kernel', None)
    ModelSupportVectorMachine.train_model_with_parameters(count_comments,parameter_c,parameter_gamma,parameter_random, kernel)
    return JsonResponse({'mensaje':'Proceso exitos'})


    