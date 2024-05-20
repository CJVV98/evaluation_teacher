from django.test import TestCase
from model_manage.models import ModelSupportVectorMachine
from  utils.data_utils import DataUtils
# Create your tests here.

class  ModelManage(TestCase):
    def valid_training(self):
       list_data=DataUtils.get_data_model_training()
       self.assertTrue(list_data.count()>0)


       