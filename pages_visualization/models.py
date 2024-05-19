from mongoengine import Document, StringField, IntField, ReferenceField, ListField, FloatField


class Teacher(Document):
    id_teacher =IntField(required=True, unique=True)
    name =StringField(required=True, unique=False)

    def get_courses_by_teacher(id, ciclo):
        pipeline=[
            {
                '$lookup': {
                    'from': 'evaluation', 
                    'localField': 'id_teacher', 
                    'foreignField': 'id_teacher', 
                    'as': 'evaluations_group'
                }
            }, {
                '$unwind': '$evaluations_group'
            }, {
                '$addFields': {
                    'name_course': '$evaluations_group.description', 
                    'id_teacher': '$id_teacher', 
                    'num_clase': '$evaluations_group.num_clase', 
                    'id_course': '$evaluations_group.id_course', 
                    'name_teacher': '$name',
                    'ciclo': '$evaluations_group.ciclo', 
                }
            }, {
                '$match': {
                    'id_teacher': id,
                    'ciclo':ciclo
                }
            }, {
                '$group': {
                    '_id': { 'id_course': '$id_course',  'id_teacher': '$id_teacher',  'num_class': '$num_clase',  'name_course': '$evaluations_group.description'}, 
                    'count': {
                        '$sum': 1
                    }
                }
            }, {
                '$project': {'_id': 0, 'id': '$_id.id_course', 'description': '$_id.name_course', 'num_course': '$_id.num_class'}
            }
        ]      
        return pipeline


class Evaluation(Document):
    id_course =IntField(required=True, unique=False)
    id_teacher =IntField(required=True, unique=False)
    ciclo=IntField(required=True, unique=False)
    num_clase =IntField(required=True, unique=False)
    description =StringField(required=True, unique=False)
    teacher= ReferenceField(Teacher)

    def get_top_emotion(emotion, ciclo):
        pipeline_top_emotions_class=[
                {
                    '$lookup': {'from': 'comment', 'localField': '_id',  'foreignField': 'evaluation',  'as': 'comments_student' }
                }, {
                    '$unwind': '$comments_student'
                }, {
                    '$addFields': { 'emotion': '$comments_student.emotion',  'id_course': '$id_course','num_clase': '$num_clase',  'name_clase': '$description'
                    }
                }, {
                    '$match': {
                        'emotion':emotion,
                        'ciclo':ciclo
                    }
                },{
                    '$group': {
                        '_id': {
                            'name_class': '$name_clase','emotion': '$emotion', 'id_course': '$id_course'
                        }, 
                        'count': {
                            '$sum': 1
                        }
                    }
                }, {
                    '$sort': {
                        'count': -1
                    }
                }, {
                    '$limit': 5
                }
        ]
        return pipeline_top_emotions_class

    def get_courses(ciclo):
        pipeline_teachers=[
            {
                '$match': {
                    'ciclo': ciclo
                }
            },
            {
                '$group': {
                    '_id': {
                        'id': '$id_course', 
                        'description': '$description'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'id': '$_id.id', 
                    'description': '$_id.description'
                }
            }
        ]
        return pipeline_teachers
    
    def get_emotions_by_teacher(id,name,ciclo):

        pipeline_emotions=[
            {
                '$match': {
                    'id_teacher': id, 
                    'ciclo': ciclo
                }
            }, {
                '$lookup': {
                    'from': 'comment', 
                    'localField': '_id', 
                    'foreignField': 'evaluation', 
                    'as': 'comments_student'
                }
            }, {
                '$unwind': '$comments_student'
            }, {
                '$addFields': {
                    'emotion': '$comments_student.emotion', 
                    'id_course': '$id_course', 
                    'num_clase': '$num_clase', 
                    'name_clase': '$description'
                }
            }, {
                '$group': {
                    '_id': {
                        'name_class': '$name_clase', 
                        'emotion': '$emotion', 
                        'id_course': '$id_course'
                    }, 
                    'cantidad': {
                        '$sum': 1
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'name_class': '$_id.name_clase', 
                        'id_course': '$_id.id_course'
                    }, 
                    'emotions': {
                        '$push': {
                            'name_class': '$_id.name_class', 
                            'emotion': '$_id.emotion', 
                            'cantidad': '$cantidad'
                        }
                    }, 
                    'total_course': {
                        '$sum': '$cantidad'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'id_teacher': name, 
                    'class_val': 'Emociones', 
                    'values': {
                        '$map': {
                            'input': '$emotions', 
                            'as': 'emotion', 
                            'in': {
                                'emotion': '$$emotion.emotion', 
                                'name_class': '$$emotion.name_class', 
                                'count_emotions':'$$emotion.cantidad', 
                                'media': {
                                    '$multiply': [
                                        {
                                            '$divide': [
                                                '$$emotion.cantidad', '$total_course'
                                            ]
                                        }, 100
                                    ]
                                }
                            }
                        }
                    }
                }
            }, {
                '$unwind': '$values'
            }, {
                '$project': {
                    '_id': 0, 
                    'id_teacher': name, 
                    'class_val': 'Emociones', 
                    'name_class': '$values.name_class', 
                    'value_class': '$values.emotion', 
                    'value_total': '$values.media',
                    'count_emotions': '$values.count_emotions',
                }
            }
        ]
        return pipeline_emotions
    
    def get_group_emotions_by_teacher(id,name,ciclo):
        pipeline_emotions=[
            {
                '$match': {
                    'id_teacher': int(id),
                    'ciclo':ciclo
                }
            }, {
                '$lookup': {
                    'from': 'comment', 
                    'localField': '_id', 
                    'foreignField': 'evaluation', 
                    'as': 'comments_student'
                }
            }, {
                '$unwind': '$comments_student'
            }, {
                '$addFields': {
                    'emotion': '$comments_student.emotion'
                }
            }, {
                '$group': {
                    '_id': {
                        'emotion': '$emotion'
                    }, 
                    'cantidad': {
                        '$sum': 1
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'value_class': '$_id.emotion', 
                    'value_total': '$cantidad'
                }
            }
            ]
        return pipeline_emotions
    
    def get_criterias_by_teacher(id,name,ciclo):
        pipeline_calification= [
            {
                '$match': {
                    'id_teacher': int(id),
                    'ciclo':ciclo
                }
            }, {
                '$lookup': {
                    'from': 'calification', 
                    'localField': '_id', 
                    'foreignField': 'evaluation', 
                    'as': 'califications_teacher'
                }
            }, {
                '$unwind': '$califications_teacher'
            }, {
                '$addFields': {
                    'prom_criteria': '$califications_teacher.prom_criterio', 
                    'criteria': '$califications_teacher.criterio', 
                    'id_course': '$id_course', 
                    'num_clase': '$num_clase', 
                    'name_clase': '$description'
                }
            }, {
                '$group': {
                    '_id': {
                        'name_class': '$name_clase', 
                        'criteria': '$criteria', 
                        'id_course': '$id_course'
                    }, 
                    'prom_criteria': {
                        '$avg': '$prom_criteria'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'id_teacher': name, 
                    'class_val': 'Criterios cuantitativos', 
                    'name_class': '$_id.name_class', 
                    'id_course': '$_id.id_course', 
                    'value_class': '$_id.criteria', 
                    'value_total': '$prom_criteria'
                }
            }
        ]
        return pipeline_calification
    
    def get_group_criterias_by_teacher(id,name, ciclo):
        pipeline_calification= [
            {
                '$match': {
                    'id_teacher': int(id),
                    'ciclo':ciclo
                }
            }, {
                '$lookup': {
                    'from': 'calification', 
                    'localField': '_id', 
                    'foreignField': 'evaluation', 
                    'as': 'califications_teacher'
                }
            }, {
                '$unwind': '$califications_teacher'
            }, {
                '$addFields': {
                    'prom_criteria': '$califications_teacher.prom_criterio', 
                    'criteria': '$califications_teacher.criterio'
                }
            }, {
                '$group': {
                    '_id': {
                        'criteria': '$criteria'
                    }, 
                    'prom_criteria': {
                        '$avg': '$prom_criteria'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'value_class': '$_id.criteria', 
                    'value_total': '$prom_criteria'
                }
            }
        ]
        return pipeline_calification

    def get_teachers_by_course(id, name, ciclo):
        pipeline=[
            {
                '$match': {
                    'id_course': id, 
                    'ciclo': ciclo
                }
            }, {
                '$lookup': {
                    'from': 'comment', 
                    'localField': '_id', 
                    'foreignField': 'evaluation', 
                    'as': 'comments_student'
                }
            }, {
                '$unwind': '$comments_student'
            }, {
                '$lookup': {
                    'from': 'teacher', 
                    'localField': 'id_teacher', 
                    'foreignField': 'id_teacher', 
                    'as': 'teacher_data'
                }
            }, {
                '$unwind': '$teacher_data'
            }, {
                '$addFields': {
                    'emotion': '$comments_student.emotion', 
                    'id_course': '$id_course', 
                    'id_teacher': '$teacher_data.name',
                    'cod_teacher': '$teacher_data.id_teacher'
                }
            }, {
                '$group': {
                    '_id': {
                        'emotion': '$emotion', 
                        'id_teacher': '$id_teacher',
                        'cod_teacher':'$cod_teacher'
                    }, 
                    'count_emotion': {
                        '$sum': 1
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'id_teacher': '$_id.id_teacher',
                        'cod_teacher': '$_id.cod_teacher'
                    }, 
                    'emotions': {
                        '$push': {
                            'emotion': '$_id.emotion', 
                            'count_emotion': '$count_emotion'
                        }
                    }, 
                    'count_total_emotion': {
                        '$sum': '$count_emotion'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'id_teacher': '$_id.id_teacher', 
                    'cod_teacher': '$_id.cod_teacher',
                    'values': {
                        '$map': {
                            'input': '$emotions', 
                            'as': 'emotion', 
                            'in': {
                                'emotion': '$$emotion.emotion', 
                                'count': '$$emotion.count_emotion', 
                                'media': {
                                    '$multiply': [
                                        {
                                            '$divide': [
                                                '$$emotion.count_emotion', '$count_total_emotion'
                                            ]
                                        }, 100
                                    ]
                                }
                            }
                        }
                    }
                }
            }, {
                '$unwind': '$values'
            }, {
                '$project': {
                    '_id': 0, 
                    'name_class': name, 
                    'id_teacher': '$id_teacher', 
                    'cod_teacher': '$cod_teacher', 
                    'emotion': '$values.emotion', 
                    'avg_emotion': '$values.media', 
                    'count': '$values.count'
                }
            }
        ]
        return pipeline
    
    def get_comments_by_teacher(id, ciclo, emotion):
        pipeline=[
            {
                '$match': {
                    'id_teacher': id, 
                    'ciclo': ciclo
                }
            }, {
                '$lookup': {
                    'from': 'comment', 
                    'localField': '_id', 
                    'foreignField': 'evaluation', 
                    'as': 'comments_student'
                }
            }, {
                '$unwind': '$comments_student'
            }, {
                '$addFields': {
                    'emotion': '$comments_student.emotion', 
                    'description': '$description', 
                    'comment': '$comments_student.comment', 
                    'name_clase': '$description'
                }
            }, {
                '$match': {
                    'emotion': emotion
                }
            }, {
                '$project': {
                    '_id':0,
                    'comment': '$comment', 
                    'emotion': '$emotion', 
                    'course': '$description'
                }
            }
        ]
        return pipeline

    def get_emotions_group_ciclo(id):
        pipeline=[
            {
                '$match': {
                    'id_teacher': id
                }
            }, {
                '$lookup': {
                    'from': 'comment', 
                    'localField': '_id', 
                    'foreignField': 'evaluation', 
                    'as': 'comments_student'
                }
            }, {
                '$unwind': '$comments_student'
            }, {
                '$addFields': {
                    'emotion': '$comments_student.emotion', 
                    'description': '$description', 
                    'ciclo': '$ciclo'
                }
            }, {
                '$group': {
                    '_id': {
                        'ciclo': '$ciclo', 
                        'emotion': '$emotion'
                    }, 
                    'count_emotion': {
                        '$sum': 1
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'ciclo': '$_id.ciclo'
                    }, 
                    'emotions': {
                        '$push': {
                            'emotion': '$_id.emotion', 
                            'count_emotion': '$count_emotion'
                        }
                    }, 
                    'count_total_emotion': {
                        '$sum': '$count_emotion'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'ciclo': '$_id.ciclo', 
                    'values': {
                        '$map': {
                            'input': '$emotions', 
                            'as': 'emotion', 
                            'in': {
                                'emotion': '$$emotion.emotion', 
                                'count':'$$emotion.count_emotion',
                                'media': {
                                    '$multiply': [
                                        {
                                            '$divide': [
                                                '$$emotion.count_emotion', '$count_total_emotion'
                                            ]
                                        }, 100
                                    ]
                                }
                            }
                        }
                    }
                }
            }, {
                '$unwind': '$values'
            }, {
                '$project': {
                    '_id': 0, 
                    'ciclo': '$ciclo', 
                    'emotion': '$values.emotion', 
                    'avg_emotion': '$values.media',
                    'count':'$values.count'
                }
            }
        ]
        return pipeline

    def get_criteria_group_ciclo(id):

        pipeline=[
            {
                '$match': {
                    'id_teacher': id
                }
            }, {
                '$lookup': {
                    'from': 'calification', 
                    'localField': '_id', 
                    'foreignField': 'evaluation', 
                    'as': 'calification_student'
                }
            }, {
                '$unwind': '$calification_student'
            }, {
                '$addFields': {
                    'criterio': '$calification_student.criterio', 
                    'description': '$description', 
                    'ciclo': '$ciclo', 
                    'avg_criteria': '$calification_student.prom_criterio'
                }
            }, {
                '$group': {
                    '_id': {
                        'criteria': '$criterio', 
                        'ciclo': '$ciclo'
                    }, 
                    'prom_criterio': {
                        '$avg': '$avg_criteria'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'criteria': '$_id.criteria', 
                    'ciclo': '$_id.ciclo', 
                    'prom_criterio': '$prom_criterio'
                }
            },
            {
                '$sort': {
                    'ciclo': 1
                }
            }
        ]   
        return pipeline

    def get_criteria_group_course_and_cycle(id, cycle):
        pipeline=[
            {
                '$lookup': {
                    'from': 'calification', 
                    'localField': '_id', 
                    'foreignField': 'evaluation', 
                    'as': 'cal_student'
                }
            }, {
                '$unwind': '$cal_student'
            }, {
                '$lookup': {
                    'from': 'teacher', 
                    'localField': 'id_teacher', 
                    'foreignField': 'id_teacher', 
                    'as': 'teacher_data'
                }
            }, {
                '$unwind': '$teacher_data'
            }, {
                '$addFields': {
                    'criteria': '$cal_student.criterio', 
                    'prom_cal_criteria': '$cal_student.prom_criterio', 
                    'id_course': '$id_course', 
                    'cod_teacher': '$teacher_data.id_teacher',
                    'id_teacher': '$teacher_data.name'
                }
            }, {
                '$match': {
                    'ciclo': cycle
                }
            }, {
                '$group': {
                    '_id': {
                        'criteria': '$criteria', 
                        'id_course': '$id_course', 
                        'id_teacher': '$id_teacher',
                         'cod_teacher':'$cod_teacher',
                    }, 
                    'prom_cal': {
                        '$avg': '$prom_cal_criteria'
                    }
                }
            }, {
                '$match': {
                    '_id.id_course': id
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'id_teacher': '$_id.id_teacher', 
                    'cod_teacher': '$_id.cod_teacher', 
                    'criteria': '$_id.criteria', 
                    'prom_cal': '$prom_cal'
                }
            }, {
                '$sort': {
                    'criteria': -1, 
                    'id_teacher':-1,
                    'count_emotion': -1
                }
            }
        ]
        return pipeline

    def count_evaluations(cycle):
        pipeline=[
            {
                '$match': {
                    'ciclo': cycle
                }
            }, {
                '$group': {
                    '_id': None, 
                    'total': {
                        '$sum': 1
                    }
                }
            }
        ]
        return pipeline
    
    def count_teachers(cycle):
        pipeline=[
            {
                '$match': {
                    'ciclo': cycle
                }
            }, {
                '$group': {
                    '_id': '$id_course', 
                    'total': {
                        '$sum': 1
                    }
                }
            }, {
                '$group': {
                    '_id': None, 
                    'total': {
                        '$sum': 1
                    }
                }
            }
        ]
        return pipeline
    
    def count_courses(cycle):
        pipeline=[
            {
                '$match': {
                    'ciclo': 2330
                }
            }, {
                '$group': {
                    '_id': '$id_teacher', 
                    'total': {
                        '$sum': 1
                    }
                }
            },
 							 {
                '$group': {
                    '_id': None, 
                    'total': {
                        '$sum': 1
                    }
                }
            }	
        ]
        return pipeline

    def get_general_data(cycle,id_teacher):
        pipeline=[
            {
                '$match': {
                    'id_teacher': id_teacher, 
                    'ciclo': cycle
                }
            }, {
                '$lookup': {
                    'from': 'calification', 
                    'localField': '_id', 
                    'foreignField': 'evaluation', 
                    'as': 'califications_teacher'
                }
            }, {
                '$unwind': '$califications_teacher'
            }, {
                '$addFields': {
                    'num_students': '$califications_teacher.total_encuestas', 
                    'num_students_resp': '$califications_teacher.total_enc_respondidas', 
                    'id_course': '$id_course', 
                    'num_clase': '$num_clase', 
                    'name_clase': '$description', 
                    'id_teacher': '$id_teacher', 
                    'prom_criterio': '$califications_teacher.prom_criterio'
                }
            }, {
                '$group': {
                    '_id': {
                        'id_teacher': '$id_teacher', 
                        'id_course': '$id_course', 
                        'num_clase': '$num_clase'
                    }, 
                    'sum_students': {
                        '$avg': '$num_students'
                    }, 
                    'sum_students_resp': {
                        '$avg': '$num_students_resp'
                    }, 
                    'max_prom': {
                        '$max': '$prom_criterio'
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'id_teacher': '$_id.id_teacher'
                    }, 
                    'sum_students': {
                        '$sum': '$sum_students'
                    }, 
                    'sum_students_resp': {
                        '$sum': '$sum_students_resp'
                    }, 
                    'max_prom': {
                        '$max': '$max_prom'
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'id_teacher': 'name', 
                    'id_course': '$_id.id_teacher', 
                    'sum_students': '$sum_students', 
                    'sum_students_resp': '$sum_students_resp', 
                    'max_prom': '$max_prom'
                }
            }
        ]
        return pipeline

    def get_count_comments(id_teacher, cycle):
        pipeline=[
            {
                '$match': {
                    'id_teacher': id_teacher, 
                    'ciclo': cycle
                }
            }, {
                '$lookup': {
                    'from': 'comment', 
                    'localField': '_id', 
                    'foreignField': 'evaluation', 
                    'as': 'comment_student'
                }
            }, {
                '$unwind': '$comment_student'
            }, {
                '$addFields': {
                    'id_teacher': '$id_teacher'
                }
            }, {
                '$group': {
                    '_id': {
                        'id_teacher': '$id_teacher'
                    }, 
                    'sum_comments': {
                        '$sum': 1
                    }
                }
            }, {
                '$project': {
                    '_id': 0, 
                    'sum_comments': '$sum_comments'
                }
            }
        ]
        return pipeline
class Comment(Document):
    comment =StringField(required=True, unique=False)
    comment_base =StringField(required=True, unique=False)
    emotion=StringField(required=True, unique=False)
    ciclo=IntField(required=True, unique=False)
    evaluation= ReferenceField(Evaluation)

    def get_emotion_count(ciclo):
        print(ciclo)
        pipeline_get_emotion_count = [
            {
                '$match': {
                    'ciclo':ciclo
                }
            },
            {
                '$group': {
                    '_id': '$emotion', 
                    'cantidad': {
                        '$sum': 1
                    }
                }
            }
        ]
        return pipeline_get_emotion_count

class Calification(Document):
    cod =IntField(required=True, unique=False)
    criterio =StringField(required=True, unique=False)
    ciclo=IntField(required=True, unique=False)
    total_encuestas =IntField(required=False, unique=False)
    total_clases_encuestadas =IntField(required=False, unique=False)
    num_estudiantes_inscritos =IntField(required=False, unique=False)
    total_enc_respondidas =IntField(required=False, unique=False)
    prom_criterio =FloatField(required=False, unique=False)
    porc_consolidado_crit_1 =FloatField(required=False, unique=False)
    porc_consolidado_crit_2 =FloatField(required=False, unique=False)
    porc_consolidado_crit_3 =FloatField(required=False, unique=False)
    porc_consolidado_crit_4 =FloatField(required=False, unique=False)
    porc_consolidado_crit_5 =FloatField(required=False, unique=False)
    porc_consolidado_crit_6 =FloatField(required=False, unique=False)
    porc_consolidado_crit_n_s =FloatField(required=False, unique=False)  
    cant_consolidado_crit_1= FloatField(required=False, unique=False) 
    cant_consolidado_crit_2= FloatField(required=False, unique=False)
    cant_consolidado_crit_3= FloatField(required=False, unique=False) 
    cant_consolidado_crit_4= FloatField(required=False, unique=False) 
    cant_consolidado_crit_5= FloatField(required=False, unique=False)
    cant_consolidado_crit_6= FloatField(required=False, unique=False) 
    cant_consolidado_crit_n_s= FloatField(required=False, unique=False) 
    evaluation= ReferenceField(Evaluation)
    def get_criteria(ciclo):
        pipeline=[
            {
                '$match': {
                    'ciclo':ciclo
                }
            },
            {
                '$group': {
                    '_id': '$criterio'
                }
            },
             {
                '$project': {
                    '_id': 0, 
                    'id': '$_id', 
                    'description': '$_id'
                }
            }
        ]
        return pipeline

    def get_calification_group(ciclo):
        pipeline_get_calification_count = [
            {
                '$match': {
                    'porc_consolidado_crit_1': {'$type': 'double', '$exists': True, '$ne': None,'$ne': float('nan')}, 
                    'porc_consolidado_crit_2': {'$type': 'double', '$exists': True, '$ne': None,'$ne': float('nan')}, 
                    'porc_consolidado_crit_3': {'$type': 'double', '$exists': True, '$ne': None,'$ne': float('nan')}, 
                    'porc_consolidado_crit_4': {'$type': 'double', '$exists': True, '$ne': None,'$ne': float('nan')}, 
                    'porc_consolidado_crit_5': {'$type': 'double', '$exists': True, '$ne': None,'$ne': float('nan')}, 
                    'porc_consolidado_crit_6': {'$type': 'double', '$exists': True, '$ne': None,'$ne': float('nan')}, 
                    'porc_consolidado_crit_n_s': {'$type': 'double', '$exists': True, '$ne': None,'$ne': float('nan')}, 
                    'ciclo': ciclo
                }
            },{
                '$group': {
                    '_id': '$criterio', 
                    'sum_criterio_1': { '$avg': '$cant_consolidado_crit_1' }, 
                    'sum_criterio_2': { '$avg': '$cant_consolidado_crit_2'}, 
                    'sum_criterio_3': { '$avg': '$cant_consolidado_crit_3' }, 
                    'sum_criterio_4': { '$avg': '$cant_consolidado_crit_4'}, 
                    'sum_criterio_5': { '$avg': '$cant_consolidado_crit_5' }, 
                    'sum_criterio_6': { '$avg': '$cant_consolidado_crit_6' }, 
                    'sum_criterio_7': { '$avg': '$cant_consolidado_crit_n_s'}
                }
            },
            {
                '$addFields': {
                    'suma_total': {
                        '$sum': [
                            '$sum_criterio_1', '$sum_criterio_2', '$sum_criterio_3', '$sum_criterio_4', '$sum_criterio_5', '$sum_criterio_6', '$sum_criterio_7'
                        ]
                    }
                }
            }
        ]
        return pipeline_get_calification_count
        
class Control(Document):
    id_teacher =IntField(required=True, unique=False)
    name =StringField(required=True, unique=False)
    prom_criteria=FloatField(required=False, unique=False)
    criteria=StringField(required=True, unique=False)
    ciclo=IntField(required=True, unique=False)
    course=StringField(required=True, unique=False)
    evaluation= ReferenceField(Evaluation)

    def get_control(ciclo):
        pipeline=[
            {
                '$match': {
                'ciclo':ciclo
                }
            },{
                '$project': {
                    '_id': 0, 
                    'id_teacher': '$id_teacher', 
                    'name': '$name',
                    'prom_criteria': '$prom_criteria', 
                    'criteria': '$criteria',
                    'ciclo': '$ciclo',
                    'course': '$course'
                }
            },
            {
                '$sort': {
                'prom_criteria': 1
                }
            }
        ]
        return pipeline
    
    