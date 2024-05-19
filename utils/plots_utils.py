import plotly.graph_objects as go # type: ignore
import numpy as np # type: ignore
import pandas as pd # type: ignore
import plotly.express as px # type: ignore
from plotly.offline import plot # type: ignore
from pages_visualization.models import Comment
from pages_visualization.models import Calification
from pages_visualization.models import Evaluation
from pages_visualization.models import Teacher
import random
from bokeh.embed import components




class PlotsUtils():
    BG_COLOR_WHITE='rgb(255, 255, 255)'

    def generate_donut_emotions(ciclo):
        list_emotion_count=list(Comment.objects.aggregate(Comment.get_emotion_count(int(ciclo))))

        list_emotions={ 0:"Miedo",1:"Enojo",2:"Tristeza",3:"Sorpresa",4:"Alegria",5:"Confianza",6:"others"}
        name_emotions =[list_emotions[int(d['_id'][1:-1])] for d in list_emotion_count]
    
        count_emotion = [d['cantidad'] for d in list_emotion_count]

        fig = px.pie(names=name_emotions, values=count_emotion,   
                                    color = name_emotions,
                                    color_discrete_map = {'Alegria': '#f39c12', 'Enojo': '#cb4335',
                                    'Confianza': '#3498db',  'Tristeza': '#2ba1cf','Miedo': '#90a4ae', 
                                    'Sorpresa': '#69a4cd',})
        fig.update_layout(
            width=410,
            height=410,
            autosize=True,
            margin=dict(l=10, r=0, t=10, b=0),
        )

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    def generate_bar_calification(ciclo):
        list_calification=list(Calification.objects.aggregate(Calification.get_calification_group(int(ciclo))))
        _id = [obj['_id'] for obj in list_calification]
        items_calification=[i for i in range(1,8)]
        cal_lists = [[] for _ in range(8)] 


        for obj in list_calification:
            for i in items_calification:
                cal_lists[i].append((float(obj[f"sum_criterio_{i}"])/float(obj['suma_total'])*100))


        fig = go.Figure()
        for i in items_calification:
            fig.add_trace(go.Bar(x=_id, y=cal_lists[i], name=f"Calificación {i}" if i != 7 else "Calificación N_S"))


        fig.update_layout(
            barmode='group',  # Agrupar las barras
            xaxis_title="Criterio",
            yaxis_title="Calificación",
            width=1100,
            height=500,
            autosize=True,
            margin=dict(l=5, r=0, t=5, b=0)
        )

        fig.update_xaxes(title_text="Criterios")
        fig.update_yaxes(title_text="Promedio de estudiantes")

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    def generate_top_calification(value_data,ciclo):
        top_courses=list(Evaluation.objects.aggregate(Evaluation.get_top_emotion("["+value_data+"]",int(ciclo))))
        name_courses = [elemento["_id"]["name_class"] for elemento in top_courses]
        count_emotion= [elemento["count"] for elemento in top_courses]
        colors = {'0':'rgba(144, 164, 174)','1':'rgba(203, 67, 53)','2':'rgba(43, 161, 207)','3':'rgba(105, 164, 205)','4':'rgba(243, 156, 18)',
                '5':'rgba(52, 152, 219)'}
        color=colors[str(value_data)]
        data_colors= {'Color' : [color.replace(')',', 1)'),color.replace(')',', 0.7)'),
                                color.replace(')',', 0.5)'),color.replace(')',', 0.3)'),
                                color.replace(')',', 0.1)') ]}  

       
        df_ = pd.DataFrame({"name": name_courses, "count": count_emotion,'color':data_colors['Color']})
        fig = px.funnel(df_, x='count', y='name')
        fig.update_traces(marker=dict(color=data_colors['Color']))

        fig.update_layout(
                width=450,
                height=400,
                xaxis_title="Cantidad de comentarios",
                plot_bgcolor=plots.BG_COLOR_WHITE,
                paper_bgcolor=plots.BG_COLOR_WHITE,
                yaxis_title="Asignatura",
                autosize=True,
                margin=dict(l=10, r=0, t=10, b=0)
        )

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div


    def generate_subburt_emotions(id,name, ciclo):
        
        list_emotions=list(Evaluation.objects.aggregate(Evaluation.get_emotions_by_teacher(id,name,ciclo)))
        df_emotions = pd.DataFrame(list_emotions)   

        if(len(list_emotions)>0):
            df_emotions['value_class'] = df_emotions['value_class'].replace({ '[0]':"Miedo",'[1]':"Enojo",'[2]':"Tristeza",'[3]':"Sorpresa",'[4]':"Alegria",'[5]':"Confianza",'[6]':"Otras"})


        color_mapping = {'Alegria': '#f39c12', 'Enojo': '#cb4335',
                        'Confianza': '#3498db',  'Tristeza': '#2ba1cf','Miedo': '#90a4ae', 
                        'Sorpresa': '#69a4cd'}

        assign_color = lambda label: next((color_mapping[key] for key in color_mapping if key in label), '#d6dbdf')
        df_emotions['color'] = df_emotions['value_class'].map(assign_color)
        df_emotions['text_value'] = df_emotions['value_total'].apply(lambda x: f"{x:.2f}%")
        number_class = df_emotions.groupby('name_class').ngroups
        space=plots.value_spacing(number_class)
        fig = px.bar(df_emotions, x="name_class", y="value_total", color="value_class",text="text_value", hover_name='count_emotions',
                pattern_shape="value_class",width=10,  color_discrete_map=color_mapping)
        fig.update_traces(textfont_color="white",hovertemplate='%{hovertext}')
        fig.update_layout(
                width=500,
                height=470,
                autosize=True,
                margin=dict(l=15, r=5, t=60, b=5),
                xaxis_title="Asignatura",
                yaxis_title="Cantidad de comentarios",
                legend_title="Emociones",
                bargap=space,
                paper_bgcolor=plots.BG_COLOR_WHITE,
                plot_bgcolor='rgb(209, 224, 238)',
                xaxis_tickangle=0,
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=1.1,
                    xanchor="right",
                    x=1
                )
                
        )
        fig.update_yaxes(showline=False, showgrid=False, zeroline=False, visible=False)
        tick_text = [text.replace(' ', '<br>') for text in df_emotions['name_class']]
        # Actualizar el layout del gráfico para usar los nuevos textos de los ticks del eje x
        fig.update_xaxes(tickvals=df_emotions['name_class'], ticktext=tick_text)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    def generate_subburt_criterias(id,name, ciclo):    
        list_criterias=list(Evaluation.objects.aggregate(Evaluation.get_criterias_by_teacher(id,name,ciclo)))
        df_criterias=pd.DataFrame(list_criterias)
        color_mapping = { 'Estrategias Pedagógicas':'#19d3f3','Evaluación':'#00cc96',
                        'Relación con los Estudiantes':'#ffa15a','Manejo de Contenidos':'#636efa'
                        }

        assign_color = lambda label: next((color_mapping[key] for key in color_mapping if key in label), '#d6dbdf')
        df_criterias['color'] = df_criterias['value_class'].map(assign_color)
        number_class = df_criterias.groupby('name_class').ngroups
        space=plots.value_spacing(number_class)
        df_criterias['text_value'] = df_criterias['value_total'].apply(lambda x: f"{x:.2f}")
        fig = px.bar(df_criterias, x="name_class", y="value_total", color="value_class", text='text_value',hover_name='text_value',
                pattern_shape="value_class",width=10,  color_discrete_map=color_mapping)
        fig.update_traces(textfont_color="white",hovertemplate='%{hovertext}')
        fig.update_layout(
                width=540,
                height=500,
                autosize=True,
                margin=dict(l=5, r=1, t=110, b=5),
                xaxis_title="Asignatura",
                yaxis_title="Promedio de criterio (0 a 26)",
                legend_title="Criterio",
                uniformtext=dict(minsize=8, mode='hide'),
                xaxis_tickangle=0,
                paper_bgcolor=plots.BG_COLOR_WHITE,
                plot_bgcolor='rgb(209, 224, 238)',
                bargap=space,
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=1.3,
                    xanchor="right",
                    x=1
                )
            )
        
        tick_text = [text.replace(' ', '<br>') for text in df_criterias['name_class']]
        # Actualizar el layout del gráfico para usar los nuevos textos de los ticks del eje x
        fig.update_xaxes(tickvals=df_criterias['name_class'], ticktext=tick_text)

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div


    def generate_bar_groups_courses_emotions(id,name, ciclo,list_id_teacher_):
        list_teachers=list(Evaluation.objects.aggregate(Evaluation.get_teachers_by_course(id,name,int(ciclo))))
        list_id_teacher = list(map(int, list_id_teacher_))
        df_teachers = pd.DataFrame(list_teachers)
        df_teachers['emotion'] = df_teachers['emotion'].replace({ '[0]':"Miedo",'[1]':"Enojo",'[2]':"Tristeza",'[3]':"Sorpresa",'[4]':"Alegria",'[5]':"Confianza",'[6]':"Otras"})

        color_mapping = {'Alegria': '#f39c12', 'Enojo': '#cb4335',
                        'Confianza': '#3498db',  'Tristeza': '#2ba1cf','Miedo': '#e8f6f3'
                        }
        
        number_class = df_teachers.groupby('id_teacher').ngroups
        space=plots.value_spacing(number_class)
        df_teachers['avg_emotion_text'] = df_teachers['avg_emotion'].apply(lambda x: f"{x:.2f}%") 
        if(list_id_teacher != []):
            df_teachers = df_teachers[df_teachers['cod_teacher'].isin(list_id_teacher)]
        fig = px.bar(df_teachers, x="avg_emotion", y="id_teacher", color='emotion', orientation='h',
                    hover_name='count', 
                    color_discrete_map=color_mapping, text='avg_emotion_text')
        fig.update_traces(textfont_color="white",hovertemplate='%{hovertext}')
        fig.update_layout(
                width=850,
                height=400,
                autosize=True,
                bargap=space,
                xaxis_title="Porcentaje de comentarios",
                yaxis_title="Docente",
                legend_title="Emociones",
                margin=dict(l=10, r=10, t=25, b=10),
                paper_bgcolor=plots.BG_COLOR_WHITE,
                plot_bgcolor='rgba(3, 49, 97, 0.19)'
        )
        
        sum_by_emotions_course = df_teachers['count'].sum()
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div,sum_by_emotions_course

    def generate_bubble_emotions(id):
        list_emotions=list(Evaluation.objects.aggregate(Evaluation.get_emotions_group_ciclo(id)))
        df_emotions = pd.DataFrame(list_emotions)
        df_emotions['emotion'] = df_emotions['emotion'].replace({ '[0]':"Miedo",'[1]':"Enojo",'[2]':"Tristeza",'[3]':"Sorpresa",'[4]':"Alegria",'[5]':"Confianza",'[6]':"Otras"})  
        df_emotions['ciclo'] = df_emotions['ciclo'].astype(str)
        df_emotions['ciclo'] = df_emotions['ciclo'].apply(lambda c: ' - '.join([c[:2], c[2:]]))
        df_emotions['avg_emotion_text'] = df_emotions['avg_emotion'].apply(lambda x: f"{x:.2f}%")

        color_mapping = {'Alegria': '#f39c12', 'Enojo': '#cb4335',
                        'Confianza': '#3498db',  'Tristeza': '#2ba1cf','Miedo': '#e8f6f3'
                        }
        sum_by_cycle = df_emotions.groupby('ciclo')['count'].sum()
        fig = px.bar(df_emotions, y="avg_emotion", x="ciclo", color="emotion",color_discrete_map=color_mapping,text='avg_emotion_text',hover_name='count')
        fig.update_traces(textfont_color="white",hovertemplate='%{hovertext}')
        fig.update_layout(
                width=500,
                height=510,
                autosize=True,
                margin=dict(l=10, r=0, t=10, b=0),
                xaxis_title="Cantidad de estudiantes",
                yaxis_title="Porcentaje",
                legend_title="Emociones",
                legend=dict(
                    orientation='h',  
                    yanchor='bottom', 
                    y=-0.25, 
                    xanchor='right',  
                    x=1  
                ),
                barmode='group'
            
            )

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div,sum_by_cycle


    def generate_bubble_criterias(id):
        list_criterias=list(Evaluation.objects.aggregate(Evaluation.get_criteria_group_ciclo(id)))
        df_criterias = pd.DataFrame(list_criterias)
        df_criterias['ciclo'] = df_criterias['ciclo'].astype(str)
        df_criterias['ciclo'] = df_criterias['ciclo'].apply(lambda c: ' - '.join([c[:2], c[2:]]))
        colors = ['#37536d', '#1a76ff']
        df_criterias['prom_criterio_text'] = df_criterias['prom_criterio'].apply(lambda x: f"{x:.2f}")
        median_by_cycle = df_criterias.groupby('ciclo')['prom_criterio'].mean()
        median_by_cycle=median_by_cycle.round(2)
        fig = px.bar(df_criterias, y="prom_criterio", x="criteria",  
                    labels={'prom_criterio': 'Promedio', 'ciclo': 'Periodo academico', 'criteria': 'Criterio'},
                    color='ciclo',color_discrete_sequence=colors, text='prom_criterio_text',hover_name='prom_criterio_text',)
        fig.update_traces(textfont_color="white",hovertemplate='%{hovertext}')
        fig.update_layout(
                width=500,
                height=510,
                autosize=True,
                barmode='group',
                xaxis_title="Criterio",
                yaxis_title="Promedio",
                legend_title="Periodo",
                margin=dict(l=10, r=0, t=10, b=0),
                xaxis_tickangle=-45
            
            )

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div,median_by_cycle


    def generate_bar_groups_courses_criterias(id, ciclo,list_id_teacher_):
        list_teachers=list(Evaluation.objects.aggregate(Evaluation.get_criteria_group_course_and_cycle(id,int(ciclo))))  
        df_teachers = pd.DataFrame(list_teachers)
        list_id_teacher = list(map(int, list_id_teacher_))
        color_mapping = { 'Estrategias Pedagógicas':'#19d3f3','Evaluación':'#00cc96',
                        'Relación con los Estudiantes':'#ffa15a','Manejo de Contenidos':'#636efa'
                        }
        df_info_teacher=df_teachers.groupby(['id_teacher','cod_teacher']).count().reset_index()
        number_class = df_teachers.groupby('id_teacher').ngroups
        space=plots.value_spacing(number_class)
        df_teachers['prom_cal_text'] = df_teachers['prom_cal'].apply(lambda x: f"{x:.2f}")
   
        if(list_id_teacher != []):
            df_teachers = df_teachers[df_teachers['cod_teacher'].isin(list_id_teacher)]
        fig = px.bar(df_teachers, x="prom_cal", y="id_teacher", color='criteria', orientation='h',
                hover_data=["criteria", "prom_cal"],  color_discrete_map=color_mapping, text="prom_cal_text",
                hover_name="prom_cal_text")
    
        fig.update_traces(textfont_color="white",hovertemplate='%{hovertext}')
        fig.update_layout(
                width=850,
                height=400,
                autosize=True,
                bargap=space,
                xaxis_title="Calificación promedio por criterio",
                yaxis_title="Docente",
                legend_title="Criterios",
                margin=dict(l=10, r=10, t=25, b=10),
                paper_bgcolor=plots.BG_COLOR_WHITE,
                plot_bgcolor='rgba(3, 49, 97, 0.19)'
        )
       
        mean_by_criteria_course = df_teachers['prom_cal'].mean()
        mean_by_criteria_course=mean_by_criteria_course.round(2)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div,mean_by_criteria_course,number_class,df_info_teacher


    def value_spacing(self,number_class):
        space=0.2
        if(number_class==1):
            space=0.7
        if(number_class<=3 and number_class>1 ):
            space=0.6
        if(number_class>=4 and number_class<8):
            space=0.5
        if(number_class>=8):
            space=0.2
        return space

    def get_general_info(cycle, id_teacher):
        list_teachers=list(Evaluation.objects.aggregate(Evaluation.get_general_data(int(cycle),int(id_teacher))))
        total=int(list_teachers[0]['sum_students'])
        total_answered=int(list_teachers[0]['sum_students_resp'])
        total_no_answered=total-total_answered
        colors=['#033161','rgb(164, 205, 247)']
        fig = go.Figure(data=[go.Pie(labels=['Respondidas','No respondidas'],
                                    values=[total_answered,total_no_answered], hole=.3)])
        fig.update_traces(hoverinfo='label+percent', 
                        textinfo='value',
                        textfont_size=12,
                        marker=dict(colors=colors),
                        )
        fig.update_layout(
            width=110,
            height=110,
            autosize=True,
            margin=dict(l=2, r=0, t=2, b=0),
            showlegend=False
        )
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div, total

    def get_heat_map(list_map):
        fig = px.imshow(list_map,
                    labels=dict(x="Emociones", y="Emociones"),
                    x=['Miedo', 'Enojo', 'Tristeza', 'Sorpresa', 'Alegria','Confianza'],
                    y=['Miedo', 'Enojo', 'Tristeza', 'Sorpresa', 'Alegria','Confianza'],
                    color_continuous_scale='YlGnBu',
                )
        fig.update_layout(
            width=500,
            height=510,
            autosize=True,
            margin=dict(l=10, r=0, t=10, b=0),
        )
    
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

plots=PlotsUtils()