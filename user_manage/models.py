from mongoengine import Document, StringField, IntField
class User(Document):
    user = StringField(required=True, unique=True)
    password = StringField(required=True, unique=False)
    names = StringField(required=True, unique=False)
    last_names =StringField(required=False, unique=False)
    email =StringField(required=True, unique=True)
    profile= StringField(required=False, unique=False)
    state =IntField(required=True, unique=False)

    def validate_user(user_input, password_input):
        try:
            user_valid = User.objects.get(user=user_input)
            # Verificar si la autenticación fue exitosa
            if user_valid is not None:
                if user_valid.password == password_input:
                     print("is valido")
                     return user_valid
                else:
                     return None
            else:
                return None
        except User.DoesNotExist:
                return None

    def get_users(user):
        pipeline=[{   
            '$match':{
                "user": {"$ne": user} 
            }
            },{
            '$project': {
                '_id':0,
                'user':'$user',
                'names':'$names',
                'last_names':'$last_names',
                'email':'$email',
                'profile':'$profile',
                'password':'$password',
                'state':'$state'
                
            }
            }
        ]
        return pipeline