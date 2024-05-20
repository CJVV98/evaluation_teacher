from  utils.data_utils import DataUtils

# Create your tests here.
class PagesVisualization(TestCase):

    def valid_emotions_teacher(self):
       list_data= DataUtils.get_comments_by_teacher(10048060,2330,'Miedo') 
       self.assertTrue(list_data.count()>0)

    def valid_alerts(self):
       list_data=DataUtils.get_list_alerts_criteria(2310)
       self.assertTrue(list_data.count()>0)

    def valid_options(self):
       #Teacher
       list_data=DataUtils.return_list_select('1',2310)   
       self.assertTrue(list_data.count()>0)
