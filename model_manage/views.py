from django.shortcuts import render  # type: ignore
from utils.data_utils import DataUtils
from utils.plots_utils import PlotsUtils
# Create your views here.


def page_training(request):
    list_data=DataUtils.get_data_model_training()
    plot_heat_map=PlotsUtils.get_heat_map(list_data[0]['matrix'])
    return render(request, 'model/page_training.html', context={'list_data':list_data,
                                                                'plot_heat_map':plot_heat_map})
