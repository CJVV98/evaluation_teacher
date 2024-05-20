import io
import pandas as pd # type: ignore
from pages_visualization.models import Teacher
from pages_visualization.models import Evaluation
from pages_visualization.models import Calification
from pages_visualization.models import Comment
from pages_visualization.models import Control
from utils.text_utils import separate_paragraph
from utils.model.supportVectorMachine import load_model, proc_text, proc_vectorizer

def load_xls_evaluations():
    """Cargar evaluaciones desde archivo excel"""
    i=0
    df_sheet=pd.read_excel('/Users/corinviracacha/Documents/Proyectos/ProyectoEvaluacionDocente/evaluation_teacher/utils/resources/evaluaciones.xls', index_col=0, sheet_name=0)
    for _, row in df_sheet.iterrows():
        _id = row['ID']
        name = 'Nombre'+str(i+1)+' Apellido'+str(i)
   
        calification={
                'num_clase': row['Nº Clase'],
                'cod': row['Cód.'],
                'ciclo':row['Ciclo'],
                'criterio': row['Críterio'],
                'total_encuestas': row['Total Encuestas'],
                'total_clases_encuestadas': row['Total Clases Encuestadas'],
                'num_estudiantes_inscritos': row['# Estudiantes Inscritos'],
                'total_enc_respondidas': row['Total Enc. Respondidas'],
                'prom_criterio': row['Prom. Críterio'],
                'porc_consolidado_crit_1': "0" if "row['%Consolidado Calif.1']" is None or row['genero'] == '' else row['%Consolidado Calif.1'],
                'porc_consolidado_crit_2': "0" if "row['%Consolidado Calif.2']" is None or row['genero'] == '' else row['%Consolidado Calif.2'],
                'porc_consolidado_crit_3': "0" if "row['%Consolidado Calif.3']" is None or row['genero'] == '' else row['%Consolidado Calif.3'],
                'porc_consolidado_crit_4': "0" if "row['%Consolidado Calif.4']" is None or row['genero'] == '' else row['%Consolidado Calif.4'],
                'porc_consolidado_crit_5': "0" if "row['%Consolidado Calif.5']" is None or row['genero'] == '' else row['%Consolidado Calif.5'],
                'porc_consolidado_crit_6': "0" if "row['%Consolidado Calif.6']" is None or row['genero'] == '' else row['%Consolidado Calif.6'],          
                'porc_consolidado_crit_n_s': "0" if row['%Consolidado Calif.N/S'] is None or row['genero'] == '' else row['%Consolidado Calif.N/S'] ,
                'cant_consolidado_crit_1': row['Consolidado_Criterio Calif.1'],
                'cant_consolidado_crit_2': row['Consolidado_Criterio Calif.2'],
                'cant_consolidado_crit_3': row['Consolidado_Criterio Calif.3'],
                'cant_consolidado_crit_4': row['Consolidado_Criterio Calif.4'],
                'cant_consolidado_crit_5': row['Consolidado_Criterio Calif.5'],
                'cant_consolidado_crit_6': row['Consolidado_Criterio Calif.6'],
                'cant_consolidado_crit_n_s': row['Consolidado_Criterio Calif.N/S'],
      
            }
        evaluation = [{
            'id_course': row['ID Curso'],
            'description':row['Descripción'],
            'id_teacher':row['ID'],
            'ciclo':row['Ciclo'],
            'num_clase':row['Nº Clase'],
            'comments':[],
            'califications':[calification]
        }]

        teacher = Teacher.objects.filter(id_teacher=_id).first()
        if not teacher:
            teacher=Teacher.objects.create(name=name, id_teacher=_id)


        evaluation_search=Evaluation.objects.filter(id_course= int(evaluation[0]['id_course']),id_teacher= int(evaluation[0]['id_teacher']), ciclo= int(evaluation[0]['ciclo']),
                                                    num_clase= int(evaluation[0]['num_clase'])).first()
        if not evaluation_search:    
            evaluation_search=Evaluation.objects.create(description=evaluation[0]['description'], id_course=int(evaluation[0]['id_course']),
               id_teacher= int(evaluation[0]['id_teacher']), ciclo= int(evaluation[0]['ciclo']), num_clase= int(evaluation[0]['num_clase']),     
               teacher=teacher)
            

        calification = Calification.objects.create(cod =int(calification['cod']),criterio =calification['criterio'], ciclo=calification['ciclo'],
                        total_encuestas=int(calification['total_encuestas']),  total_clases_encuestadas =int(calification['total_clases_encuestadas']),
                        num_estudiantes_inscritos=int(calification['num_estudiantes_inscritos']), total_enc_respondidas =int(calification['total_enc_respondidas']),
                        prom_criterio =float(calification['prom_criterio']),porc_consolidado_crit_1=float(calification['porc_consolidado_crit_1']),
                        porc_consolidado_crit_2 =float(calification['porc_consolidado_crit_2']), porc_consolidado_crit_3 =float(calification['porc_consolidado_crit_3']),
                        porc_consolidado_crit_4 =float(calification['porc_consolidado_crit_4']),porc_consolidado_crit_5 =float(calification['porc_consolidado_crit_5']),
                        porc_consolidado_crit_6 =float(calification['porc_consolidado_crit_6']),porc_consolidado_crit_n_s =float(calification['porc_consolidado_crit_n_s']),
                        cant_consolidado_crit_1=float(calification['cant_consolidado_crit_1']),cant_consolidado_crit_2= float(calification['cant_consolidado_crit_2']),
                        cant_consolidado_crit_3=float(calification['cant_consolidado_crit_3']), cant_consolidado_crit_4= float(calification['cant_consolidado_crit_4']),
                        cant_consolidado_crit_5=float(calification['cant_consolidado_crit_5']),cant_consolidado_crit_6=float(calification['cant_consolidado_crit_6']),
                        cant_consolidado_crit_n_s= float(calification['cant_consolidado_crit_n_s']),
                        evaluation=evaluation_search)

     
        if float(calification['prom_criterio'])<4:
            Control.objects.create(id_teacher=int(evaluation[0]['id_teacher']), name=teacher.name,prom_criteria=float(calification['prom_criterio']),
                                            criteria=calification['criterio'],ciclo=calification['ciclo'],course=evaluation[0]['description'],
                                            evaluation=evaluation_search)
        i=i+1

def load_xls_comments():
    """Cargar comentarios desde archivo excel"""
    comments=[]
    df_sheet=pd.read_excel('/Users/corinviracacha/Documents/Proyectos/ProyectoEvaluacionDocente/evaluation_teacher/utils/resources/comentarios.xls', index_col=0, sheet_name=0)
    model_svm=load_model()
    course=""
    teacher=""
    num_class=""
    ciclo=""
    for _, row in df_sheet.iterrows():  
       if(len(str(row['Descripción']))>8):
        comments=separate_paragraph(row['Descripción'])
        if(len(str(row['ID Curso']))>=4):
            course=row['ID Curso']
            teacher=row['ID']
            num_class=row['Nº Clase']
            ciclo=row['Ciclo']
        id_course=course
        id_teacher=teacher
        num_clase=num_class
        evaluation_search=Evaluation.objects.filter(id_course=id_course,id_teacher=id_teacher, ciclo= ciclo,
                                                        num_clase=num_clase).first()
        for comment in comments:
                new_comment=proc_text(str(comment))
                new_comment_tfidf = proc_vectorizer(new_comment)
                emotion = model_svm.predict(new_comment_tfidf)
    
                comment=Comment.objects.create(comment=str(comment), comment_base=str(row['Descripción']), emotion=str(emotion),
                                               ciclo=ciclo, evaluation=evaluation_search)
        
            
