from . settings import *
import mongoengine

# Conectarse a MongoDB al importar la aplicación
mongoengine.connect(host="mongodb://localhost:27017/db_evaluation_teacher")