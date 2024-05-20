from django.db import models
from mongoengine import Document, StringField, IntField, ReferenceField, ListField, FloatField,DateTimeField

# Create your models here.
        
class Model(Document):
    file =StringField(required=False, unique=False)
    count_register=IntField(required=False, unique=False)
    parameter_training=IntField(required=False, unique=False)
    precision =FloatField(required=True, unique=False)
    list_measurement=ListField(required=False, unique=False)
    matrix=ListField(required=False, unique=False)
    date_start=DateTimeField(required=False, unique=False)
    date_end=DateTimeField(required=False, unique=False)

    """
        Usado para obtener los datos de entrenamiento del modelo
    """
    def get_data_model():
        pipeline=[
            {
                '$project': {
                    '_id': 0
                }
            }, {
                '$sort': {
                    'date_start': 1
                }
            }, {
                '$limit': 1
            }
        ]
        return pipeline